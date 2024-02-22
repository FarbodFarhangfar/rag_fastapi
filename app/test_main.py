import io
import pytest
from fastapi.testclient import TestClient
from main import app
import os

client = TestClient(app)

@pytest.fixture
def pdf_file():
    # Create a sample PDF file in memory
    pdf_content = b"Sample PDF content"
    return io.BytesIO(pdf_content)

def test_index():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to Jarvic.ai"}



def test_upload_pdf(pdf_file):
    # Save the sample PDF file to a temporary file
    file = "E:/WORK/interview/Copy_of_Foods.pdf"

    # Send a POST request with the temporary PDF file
    files = {"file": (file, open(file, "rb"), "application/pdf")}
    response = client.post("/uploadpdf", files=files)

    # Assert that the response status code is 200
    assert response.status_code == 200

    # Assert that the response message indicates successful upload
    assert response.json() == {"message": "File uploaded successfully"}


def test_process_text_endpoint_valid_data():
    # Sending a valid question
    payload = {"text": "tell me five Iranian dishes?"}
    response = client.post("http://127.0.0.1:8000/question", json=payload)

    # Checking if the response is successful
    assert response.status_code == 200

    # Assuming your endpoint returns a JSON response



def test_process_text_endpoint_with_no_data():
    # Sending no data
    response = client.post("/question", json={})

    # Checking if the response status code is 422 Unprocessable Entity
    assert response.status_code == 422

    # Checking if the response contains the expected error message
