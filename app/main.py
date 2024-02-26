from fastapi import FastAPI, UploadFile, File, HTTPException, Request
from fastapi.responses import JSONResponse
import shutil
from typing import Optional

from RAG import processing_document, question_answering, create_document
from utils import extract_text_with_style, parse_data

app = FastAPI()


@app.get("/")
def index():
    return {"message": "Welcome to Jarvic.ai"}


def process_pdf(file, custom_style):
    text = extract_text_with_style(file)
    text = parse_data(text, custom_style)
    text = create_document(text)
    pipline_model = processing_document(text)
    return pipline_model


class PDFModelHandler:
    def __init__(self):
        pass

    def process_pdf(self, pdf_file: bytes, custom_style: bool):
        self.pdf_file = pdf_file
        self.model_pipline = process_pdf(pdf_file, custom_style)

    def generate_answer(self, data):
        # Use your model to generate something
        try:
            answer = question_answering(data, self.model_pipline)
            return answer
        except AttributeError as e:
            return "please upload a pdf file first"


pdf_handler = PDFModelHandler()


# Dependency to get or create the model instance for a PDF file


@app.post("/uploadpdf")
def upload_pdf(file: UploadFile = File(...), custom_style: bool = False):
    if not file.filename.endswith(".pdf"):
        return JSONResponse(status_code=400, content={"message": "Only PDF files are allowed"})

        # Save the uploaded file
    with open(file.filename, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    pdf_handler.process_pdf(file.filename, custom_style)
    return JSONResponse(status_code=200, content={"message": "File uploaded successfully"})


from pydantic import BaseModel

class Question(BaseModel):
    text: str

@app.post("/question")
def process_text_endpoint(data: Question):
    data = data.text

    if not data:
        raise HTTPException(status_code=400, detail="No data provided")

    answer = pdf_handler.generate_answer(data)
    return answer
