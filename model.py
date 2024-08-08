from langchain.text_splitter import CharacterTextSplitter
from langchain_community.embeddings import SentenceTransformerEmbeddings, HuggingFaceEmbeddings, HuggingFaceInstructEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain_community.llms import HuggingFacePipeline, HuggingFaceHub
from langchain_community.chat_models import ChatOpenAI
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from transformers import pipeline
from dotenv import load_dotenv
import torch



def load_llm_pipeline():
    base_model = "LaMini-T5-738M"
    tokenizer = AutoTokenizer.from_pretrained(base_model)
    llm = AutoModelForSeq2SeqLM.from_pretrained(base_model, device_map='cpu', torch_dtype=torch.float32)
    pipe = pipeline('text2text-generation', model=llm, tokenizer=tokenizer, max_length=1024, do_sample=True, temperature=0.2, 
                    top_p=0.95)
    llm_pipeline = HuggingFacePipeline(pipeline=pipe)
    return llm_pipeline


def chatbot(vector_database, model): 
    load_dotenv()
    llm_models = {
        'OpenAI': ChatOpenAI(),
        'HuggingFace': HuggingFaceHub(repo_id="google/flan-t5-xxl", model_kwargs={"temperature":0.5, "max_length":512}),
        'LaMini': load_llm_pipeline()
    }
    llm = llm_models.get(model)
    memory = ConversationBufferMemory(memory_key='chat_history', output_key='answer', return_messages=True)
    conversation_chain = ConversationalRetrievalChain.from_llm(llm=llm, chain_type="stuff", 
                                                               retriever=vector_database.as_retriever(), 
                                                               return_source_documents=True, memory=memory
                                                               )
    return conversation_chain




