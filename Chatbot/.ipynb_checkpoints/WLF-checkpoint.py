import chainlit as cl
import os
import re
import asyncio
from PIL import Image
from transformers import CLIPProcessor, CLIPModel
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.chains import RetrievalQA
from langchain_core.prompts import PromptTemplate
from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain.embeddings.base import Embeddings
import torch
import base64

FAISS_TEXT_DB_PATH = 'FAISS Database/'
FAISS_IMAGE_DB_PATH = 'FAISS_Image_DB/'

# A custom Embeddings class that wraps the CLIP model for LangChain
class CLIPEmbeddings(Embeddings):
    def __init__(self, model, processor):
        self.model = model
        self.processor = processor
    
    def embed_documents(self, texts):
        pil_images = [Image.open(path) for path in texts]
        inputs = self.processor(images=pil_images, return_tensors="pt", padding=True)
        with torch.no_grad():
            image_features = self.model.get_image_features(**inputs)
        return image_features.cpu().numpy().tolist()

    def embed_query(self, text):
        inputs = self.processor(text=text, return_tensors="pt", padding=True)
        with torch.no_grad():
            text_features = self.model.get_text_features(**inputs)
        return text_features.cpu().numpy().tolist()[0]

def load_llm_multimodal(huggingface_repo_id, HF_TOKEN):
    llm = HuggingFaceEndpoint(
        repo_id=huggingface_repo_id,
        temperature=0.5,
        huggingfacehub_api_token=HF_TOKEN,
        task='text-generation' # Change task for multi-modal model
    )
    return llm

@cl.on_chat_start
async def start():
    try:
        intro_text = """
### ℹ️ Important Notice

This assistant is a fan-made, non-official resource based on **The Last of Us Part 2** game guide. It is intended for informational and entertainment purposes only and may contain **spoilers**.

All game assets, characters, and concepts are the intellectual property of Naughty Dog and Sony Interactive Entertainment. This project is not affiliated with or endorsed by Naughty Dog or Sony.
"""
        sidebar_info = cl.Text(name="important_notice", content=intro_text, display="side")

        # Load both text and image vector databases and models
        text_embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L12-v2")
        text_vectorstore = FAISS.load_local(FAISS_TEXT_DB_PATH, text_embedding_model, allow_dangerous_deserialization=True)

        clip_model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
        clip_processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")
        clip_embeddings = CLIPEmbeddings(model=clip_model, processor=clip_processor)
        image_vectorstore = FAISS.load_local(FAISS_IMAGE_DB_PATH, clip_embeddings, allow_dangerous_deserialization=True)
        
        # Load multi-modal LLM
        huggingface_repo_id = "llava-hf/llava-1.5-7b-hf"
        HF_TOKEN = os.getenv("HF_TOKEN")
        if not HF_TOKEN:
            await cl.Message(content="❌ **Error**: HuggingFace token not found. Please set HF_TOKEN environment variable and restart.").send()
            return
        
        chat_model = ChatHuggingFace(llm=load_llm_multimodal(huggingface_repo_id=huggingface_repo_id, HF_TOKEN=HF_TOKEN))
        
        cl.user_session.set("text_vectorstore", text_vectorstore)
        cl.user_session.set("image_vectorstore", image_vectorstore)
        cl.user_session.set("chat_model", chat_model)
        cl.user_session.set("ready", True)
        
        welcome_message = cl.Message(
            content="""
🎮 Welcome to WLF, your The Last of Us Part 2 assistant!

You can now ask me anything about:
- Characters and storylines
- Weapons and items 
- Safe codes and collectibles
- Chapter guides
- Enemy information
- And much more!

💬 Type your question below to get started!""",
            elements=[sidebar_info]
        )
        await welcome_message.send()
        
    except Exception as e:
        await cl.Message(content=f"❌ **Error initializing system:**\n\n{str(e)}\n\nPlease check your configuration and try again.").send()

@cl.on_message
async def main(message: cl.Message):
    if not cl.user_session.get("ready", False):
        await cl.Message(content="⏳ System is still loading. Please wait for initialization to complete.").send()
        return
    
    try:
        await cl.Message(content="Processing...").send()
        
        text_vectorstore = cl.user_session.get("text_vectorstore")
        image_vectorstore = cl.user_session.get("image_vectorstore")
        chat_model = cl.user_session.get("chat_model")
        
        # Step 1: Text Retrieval
        text_retriever = text_vectorstore.as_retriever(search_kwargs={'k': 3})
        text_documents = text_retriever.invoke(message.content)
        text_context = "\n".join([doc.page_content for doc in text_documents])

        # Step 2: Image Retrieval
        image_retriever = image_vectorstore.as_retriever(search_kwargs={'k': 2})
        image_documents = image_retriever.invoke(message.content)

        # Step 3: Prepare images for multi-modal LLM input
        image_elements = []
        for doc in image_documents:
            image_path = doc.page_content
            if os.path.exists(image_path):
                # Chainlit's image element can pass the image data directly to the LLM
                image_elements.append(cl.Image(path=image_path, name=os.path.basename(image_path)))

        # Step 4: Combine text and image context and pass to the LLM
        # The prompt is now simpler as the LLM understands images directly.
        prompt_template = f"""
        You are a The Last of Us Part 2 expert assistant. Use the provided text and images to answer the user's question accurately and comprehensively.

        IMPORTANT GUIDELINES:
        - Answer directly and concisely - no small talk or greetings
        - If the context contains spoiler warnings (⚠️), include them in your response before revealing spoilers
        - If you don't know the answer from the given context, state "I don't have that information in the provided context"
        - Stick strictly to the provided context - do not add external knowledge
        - For weapon/item locations, include the specific chapter and area mentioned
        - For safe codes, provide both the code and the method to find it
        - You may refer to the images to help answer the question.

        Context: {text_context}

        Question: {message.content}
        
        Answer:"""

        # Create a Message with text and image elements
        msg = cl.Message(content="")
        msg.elements = image_elements
        
        # Use a single, simplified LLM call
        response_stream = await chat_model.astream(
            prompt_template,
            elements=image_elements
        )
        
        # Stream the response
        async for chunk in response_stream:
            await msg.stream_token(chunk)
            
        await msg.send()
            
    except Exception as e:
        await cl.Message(content=f"❌ **Error processing your question:**\n\n{str(e)}\n\nPlease try rephrasing your question or try again.").send()

if __name__ == "__main__":
    cl.run()