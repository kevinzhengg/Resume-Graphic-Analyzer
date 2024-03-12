import os
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.embeddings import GPT4AllEmbeddings
from langchain_community.vectorstores import FAISS, VectorStore
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
# from langchain.llms import huggingface_hub
from langchain_community.llms import HuggingFaceHub
from langchain.llms.huggingface_pipeline import HuggingFacePipeline


def get_pdf_text(pdf_docs):
    text = ""
    images = []
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
            for image in page.images:
                images.append(image.data)

    return (text, images)

def get_pdf_bytes(bytestream):
    text = ""
    images = []
    pdf_reader = PdfReader(bytestream)
    for page in pdf_reader.pages:
        text += page.extract_text()
        for image in page.images:
            images.append(image.data)
            
    return (text, images)


# (l, _) = get_pdf_text(["./src/resume.pdf"])


def get_text_chunks(text):
    text_splitter = CharacterTextSplitter(
        separator = "\n",
        chunk_size = 1000, 
        chunk_overlap  = 200, # type: ignore
        length_function = len, # type: ignore
        is_separator_regex = False,
    )
    chunks = text_splitter.split_text(text)
    return chunks


# w = get_text_chunks(l)


# creats embeddings for text chunks represented as a vector store
def create_embeddings(text_chunks):
    load_dotenv()

    embeddings = GPT4AllEmbeddings(client="eeoo");
    vector_store = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
    return vector_store



def get_conversation_chain(vectorstore: VectorStore):
    hf = HuggingFacePipeline.from_model_id(
        model_id="mistralai/Mistral-7B-Instruct-v0.1", task="text-generation", pipeline_kwargs={"max_new_tokens": 200, "pad_token_id": 50256},
    )
    # llm = HuggingFaceHub(
    #         repo_id='mistralai/Mistral-7B-v0.1',
    #         task='text-generation',
    #         huggingfacehub_api_token=os.getenv("HUGGING_FACE_AUTH_TOKEN"),
    #         # client='eeoo',
    #         model_kwargs={'temperature': '0.2',  'max-size': 512},
    #         )
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    conversation_chain = ConversationalRetrievalChain.from_llm(
            llm=hf,
            retriever=vectorstore.as_retriever(),
            memory=memory
            )

    return conversation_chain



# q = input("ask a q: ")
# while q != "end":
#     chain = get_conversation_chain(create_embeddings(w))
#     resp = chain({'question': q})
#     print(resp)
#     q = input("ask a q: ") 
