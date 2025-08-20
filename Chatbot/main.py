import os
import gcsfs
import re
import tempfile
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from langchain_huggingface import HuggingFaceEndpoint, HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from dotenv import load_dotenv, find_dotenv


load_dotenv(find_dotenv())


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


HUGGINGFACEHUB_API_TOKEN = os.getenv("HUGGINGFACEHUB_API_TOKEN")
GCS_BUCKET_NAME = os.getenv("GCS_BUCKET_NAME") 

# --- Helper Functions ---
def extract_image_paths(text):
    patterns = [
        r'Image:\s*([^\s]+\.(?:jpeg|jpg|png|gif|bmp|webp))',
        r'\(Image:\s*([^\s]+\.(?:jpeg|jpg|png|gif|bmp|webp))\)',
    ]
    all_extracted_paths = []
    for pattern in patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        all_extracted_paths.extend([os.path.basename(path) for path in matches])
    return list(set(all_extracted_paths))

def clean_response_text(text):
    cleaned_text = re.sub(r'\s*\(?Image:\s*[^)]+\)?', '', text, flags=re.IGNORECASE)
    cleaned_text = re.sub(r'\s+', ' ', cleaned_text)
    return cleaned_text.strip()


def load_faiss_db():

    

    fs = gcsfs.GCSFileSystem(project=os.getenv("FIREBASE_PROJECT_ID"))
    

    temp_dir = tempfile.mkdtemp()
    
  
    gcs_faiss_path = f"{GCS_BUCKET_NAME}/FAISS Database/"
    
    try:

        fs.get(gcs_faiss_path, temp_dir, recursive=True)
        print(f"Downloaded FAISS files to local temporary directory: {temp_dir}")

        embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        db = FAISS.load_local(temp_dir, embeddings, allow_dangerous_deserialization=True)
        print("FAISS database loaded successfully from Cloud Storage.")
        return db
    except Exception as e:
        print(f"Error loading FAISS database from GCS: {e}")

        return None
    finally:

        pass


llm = HuggingFaceEndpoint(
    repo_id="mistralai/Mistral-7B-Instruct-v0.2",
    max_length=128,
    temperature=0.5,
    token=HUGGINGFACEHUB_API_TOKEN
)


db = load_faiss_db()
if db:
    retriever = db.as_retriever(search_kwargs={'k': 3})
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=True,
    )
else:
    qa_chain = None 


class Query(BaseModel):
    text: str

@app.post("/ask")
async def ask_question(query: Query):
    if not qa_chain:
        raise HTTPException(
            status_code=503,
            detail="Chatbot service is not ready. The FAISS database could not be loaded."
        )
    
    try:
        prompt_template = f"""
You are a The Last of Us Part 2 expert assistant. Use the provided text and images to answer the user's question accurately and comprehensively.

IMPORTANT GUIDELINES:
- Answer directly and concisely - no small talk or greetings.
- If the text contains spoiler warnings (⚠️), include them in your response before revealing spoilers.
- If you don't have that information, state "I don't have that information in the provided context."
- Stick strictly to the provided context - do not add external knowledge.
- For weapon/item locations, include the specific chapter and area mentioned.
- For safe codes, provide both the code and the method to find it.
- For image queries, you must display the images.
- When an image is relevant, include the actual image in the response.

Context: {{context}}
Question: {query.text}

Answer:"""
        
        response = qa_chain.invoke({"query": prompt_template})
        result = response.get("result", "I don't have that information in the provided context.")
    
        extracted_image_filenames = extract_image_paths(result)
        cleaned_response = clean_response_text(result)


        gcs_base_url = f"https://storage.googleapis.com/{GCS_BUCKET_NAME}/Images"
        image_urls = [gcs_base_url + filename for filename in extracted_image_filenames]

        return {
            "answer": cleaned_response,
            "images": image_urls
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
