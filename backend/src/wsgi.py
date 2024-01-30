from io import BufferedReader, BytesIO, FileIO, TextIOWrapper
from flask import Flask
from flask import request, redirect, url_for
from flask_cors import CORS
import train
import os

app = Flask(__name__)
CORS(app, origins=["http://localhost:5173"])
# app.config['UPLOAD_FOLDER'] = '/home/vincent/Documents/hack-the-north-project/uploads';

@app.route("/api/upload", methods=['POST'])
def receive_upload():
    f = request.files['file-upload']
    filename = f.filename;
    # path = os.path.join(app.config['UPLOAD_FOLDER'], filename);
    stream = BytesIO(f.read());

    (text, imgs) = train.get_pdf_bytes(stream)
    chunks = train.get_text_chunks(text)
    vectorstore = train.create_embeddings(chunks)
    
    chain = train.get_conversation_chain(vectorstore)

    resp = chain({'question': 'What are some of the key skills this person has? Please output the skills in the format of a comma seperated list'})

    return redirect(url_for('download_file', name=filename))
