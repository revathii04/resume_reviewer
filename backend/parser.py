import os
import fitz  # PyMuPDF
import docx2txt
import re


def extract_resume_text(file):
    filename = file.filename
    ext = os.path.splitext(filename)[1].lower()

    if ext == ".pdf":
        text = extract_text_from_pdf(file)
    elif ext == ".docx":
        text = extract_text_from_docx(file)
    else:
        raise ValueError("Unsupported file format")

    # 🔧 Clean line breaks and extra spaces to ensure matching works correctly
    clean_text = text.replace('\r', '')
    return clean_text



def extract_text_from_pdf(file):
    text = ""
    with fitz.open(stream=file.read(), filetype="pdf") as doc:
        for page in doc:
            text += page.get_text()
    return text


def extract_text_from_docx(file):
    return docx2txt.process(file)
