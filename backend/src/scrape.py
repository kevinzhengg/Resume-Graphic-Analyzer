from PyPDF2 import PdfReader
# import chromadb
# from langchain.embeddings.sentence_transformer import SentenceTransformerEmbeddings
from langchain.text_splitter import CharacterTextSplitter
# from langchain.vectorstores import Chroma

# chroma_client = chromadb.Client()
# collection = chroma_client.create_collection(name="my_collection")

# encode this so it comes from an api req, db, or something else later
pdf_file_path = './src/resume.pdf'

def extract_text_from_pdf():
    reader = PdfReader(pdf_file_path)

    page = reader.pages[0]

    text = page.extract_text()
    return text

# load the document and split it into chunks

raw_text = extract_text_from_pdf()

text_splitter = CharacterTextSplitter(        
    separator = "\n",
    chunk_size = 30,
    chunk_overlap  = 4, #striding over the text
    length_function = len,
)
texts = text_splitter.split_text(raw_text)




# # split it into chunks
# text_splitter = TokenTextSplitter(chunk_size=12, chunk_overlap=0)
# splited_text = text_splitter.split_text(text)

# # create the open-source embedding function
# embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

# # load it into Chroma
# db = Chroma.from_documents(splited_text, embedding_function)

# # print(db)