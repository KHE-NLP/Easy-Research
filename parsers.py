import io

from pdfminer.high_level import extract_text
import requests
from pptx import Presentation
from PIL import Image


def get_pdf_text(pdf_data):
    resp = requests.get(pdf_data)
    resp_bytes = io.BytesIO(resp.content)
    data = extract_text(resp_bytes)
    return data


def get_pdf_paragraphs(pdf_data, min_par=40):
    data = get_pdf_text(pdf_data).split("\n\n")
    to_rem = []
    for i in data:
        if len(i) < min_par:
            to_rem.append(i)
    for i in to_rem:
        data.remove(i)
    return data


def get_pptx_slides(pptx_data, ask_desc=True):
    resp = requests.get(pptx_data)
    resp_bytes = io.BytesIO(resp.content)
    ppt = Presentation(resp_bytes)

    slides = []
    for slide in ppt.slides:
        slide_text = ""
        for shape in slide.shapes:
            if hasattr(shape, "text"):
                slide_text += shape.text + "\n"
            if hasattr(shape, "image"):
                Image.open(io.BytesIO(shape.image.blob)).show()
                if ask_desc:
                    desc = input("What is this? >")
                    slide_text += "[IMAGE " + desc + "]"
        slides.append(slide_text)
    return slides


if __name__ == "__main__":
    # pdf = get_pdf_paragraphs('http://faculty.cs.tamu.edu/stoleru/papers/won12re2mr.pdf')
    # print(*pdf, sep="\nPAR:\n")
    pptx = get_pptx_slides(
        "http://antares.cs.kent.edu/~seminar/Presentations/Minimum-Latency%20Broadcast%20Scheduling%20in%20Wireless%20Ad%20Hoc%20Networks.pptx")
    print(*pptx, sep="\n")
