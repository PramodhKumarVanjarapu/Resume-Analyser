import requests
import pdfplumber
from io import BytesIO

def extract_text_from_pdf(url: str) -> str:
    try:
        response = requests.get(url, timeout=10)
        file = BytesIO(response.content)

        text = ""
        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ""

        return text.lower()

    except Exception as e:
        print(f"Error processing PDF: {e}")
        return ""