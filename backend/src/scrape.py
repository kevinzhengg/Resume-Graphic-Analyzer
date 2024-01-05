import PyPDF2
from typing import Sequence
from langchain.prompts import (
    PromptTemplate,
    ChatPromptTemplate,
    HumanMessagePromptTemplate
)
from langchain.chains import create_tagging_chain
from langchain_experimental.llms import ChatLlamaAPI


class Person(BaseModel):
    person_name: str
    person_skills: [str]
    person_experiences: Optional[str]
    person_education: str

class People(BaseModel):
    people: Sequence[Person]
    

# encode this so it comes from an api req, db, or something else later
pdf_file_path = './src/resume.pdf'

def extract_text_from_pdf():
    reader = PyPDF2.PdfReader(pdf_file_path)

    page = reader.pages[0]

    text = page.extract_text()
    return text

# load the document and split it into chunks
raw_text = extract_text_from_pdf()
print(raw_text)

query = raw_text

model = ChatLlamaAPI(client=llama)

schema = {
    "properties": {
        "sentiment": {"type": "string", 'description': 'the sentiment encountered in the passage'},
        "aggressiveness": {"type": "integer", 'description': 'a 0-10 score of how aggressive the passage is'},
        "language": {"type": "string", 'description': 'the language of the passage'},
    }
}

chain = create_tagging_chain(schema, model)

chain.run("give me your money")
