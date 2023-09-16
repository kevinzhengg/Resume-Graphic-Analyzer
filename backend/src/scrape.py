from PyPDF2 import PdfReader


# encode this so it comes from an api req, db, or something else later
pdf_file_path = './src/resume.pdf'

reader = PdfReader(pdf_file_path)

page = reader.pages[0]

print(page.extract_text())