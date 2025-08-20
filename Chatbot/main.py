from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
from langchain_huggingface import HuggingFaceEndpoint, HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from dotenv import load_dotenv, find_dotenv
from fastapi.staticfiles import StaticFiles
import re
from fastapi.middleware.cors import CORSMiddleware





load_dotenv(find_dotenv())


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.mount("/images", StaticFiles(directory='Data/Images/'), name="images")



class Query(BaseModel):
    text: str

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




llm = HuggingFaceEndpoint(
    repo_id="mistralai/Mistral-7B-Instruct-v0.2",
    max_length=128,
    temperature=0.5,
    token=os.getenv("HUGGINGFACEHUB_API_TOKEN")
)


embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")


db = FAISS.load_local('FAISS Database/', embeddings, allow_dangerous_deserialization=True)
retriever = db.as_retriever(search_kwargs={'k': 3})


qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=retriever,
    return_source_documents=True,
)



@app.post("/ask")
async def ask_question(query: Query):
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

        base_url = "http://127.0.0.1:8000/images/"
        image_urls = [base_url + filename for filename in extracted_image_filenames]

        return {
            "answer": cleaned_response,
            "images": image_urls
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))