import cohere
import re
from parsers import get_pdf_paragraphs


def NOR(a, b):
    if a == 0 and b == 0:
        return True
    return False


if __name__ == "__main__":
    paragraphs = get_pdf_paragraphs("https://arxiv.org/pdf/2210.06929.pdf")

    to_rem = []

    for p in paragraphs:
        if p != (re.match()):
            to_rem.append(p)
            continue
        if (len(p) < 100) and (NOR(p != paragraphs[0], p != paragraphs[1])) or p[0].islower():
            to_rem.append(p)
            continue
        if p.find("Fig.") != -1 or p.find("doi.org") != -1:
            to_rem.append(p)

    for r in to_rem:
        paragraphs.remove(r)

    co = cohere.Client('hpaaYCC1MGPwyigl9JhSQg3NCZaLzDkSrYM6Iy6U')
    prompt = "Summarize the following passage for a presentation: \n ${fPassage} \n\n  Summary:"
    responses = []
    for p in paragraphs:
        stopsequences = ['\n\n', '\t']
        response = co.generate(prompt=prompt.format(fPassage=p), max_tokens=150, temperature=0.9, k=10)
        responses.append(response)
        print("Completed paragraph")

    for e in responses:
        print(e.generations[0].text)
