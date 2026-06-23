import requests
import pdfplumber
from io import BytesIO
import fitz  # PyMuPDF


import requests

def download_file(url):
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    if "drive.google.com" in url:
        file_id = None

        if "id=" in url:
            file_id = url.split("id=")[1].split("&")[0]
        elif "/d/" in url:
            file_id = url.split("/d/")[1].split("/")[0]

        if not file_id:
            raise Exception("Invalid Google Drive URL")

        download_url = f"https://drive.google.com/uc?export=download&id={file_id}"

        session = requests.Session()
        response = session.get(download_url, headers=headers)

        for key, value in response.cookies.items():
            if key.startswith("download_warning"):
                params = {"id": file_id, "confirm": value}
                response = session.get(download_url, params=params, headers=headers)

        return response.content

    else:
        response = requests.get(url, headers=headers, timeout=15)
        return response.content


def extract_clickable_links(file):
    links = []
    try:
        doc = fitz.open(stream=file.read(), filetype="pdf")
        for page in doc:
            for link in page.get_links():
                if link.get("uri"):
                    links.append(link["uri"])
        doc.close()
        file.seek(0)  # reset pointer
    except:
        pass
    return links


def extract_text_and_links_from_pdf(url: str):
    try:
        file_bytes = download_file(url)
        file = BytesIO(file_bytes)
        text = ""
        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ""

        file.seek(0)

        clickable_links = extract_clickable_links(file)

        return text.lower(), clickable_links

    except Exception as e:
        print(f"Error processing PDF: {e}")
        return "", []