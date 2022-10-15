import io

from pdfminer.high_level import extract_text
import requests


def get_pdf_text(pdf_data):
    resp = requests.get(pdf_data)
    resp_bytes = io.BytesIO(resp.content)
    data = extract_text(resp_bytes)
    return data

if __name__=="__main__":
    pdf = get_pdf_text('http://faculty.cs.tamu.edu/stoleru/papers/won12re2mr.pdf')

    print(pdf)