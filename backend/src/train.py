from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import HuggingFaceInstructEmbeddings
from langchain.vectorstores import FAISS, VectorStore
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import AzureChatOpenAI, ChatCohere, ChatOpenAI

def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page  in pdf_reader.pages:
            text += page.extract_text()

    return text

l = get_pdf_text(["./src/resume.pdf"])


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


w = get_text_chunks(l)


# creats embeddings for text chunks represented as a vector store
def create_embeddings(text_chunks):
    embeddings = HuggingFaceInstructEmbeddings(model_name="hkunlp/instructor-large")

    vector_store = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
    return vector_store



def get_conversation_chain(vectorstore: VectorStore):
    llm = AzureChatOpenAI()
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    conversation_chain = ConversationalRetrievalChain.from_llm(
            llm=llm,
            retriever=vectorstore.as_retriever(),
            memory=memory
            )

    return conversation_chain


q = input("ask a q")
chain = get_conversation_chain(create_embeddings(w))
resp = chain({'question': q})
print(resp)
