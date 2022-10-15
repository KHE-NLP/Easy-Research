import cohere
import re
from parsers import get_pdf_paragraphs


def NOR(a, b):
    if a == 0 and b == 0:
        return True
    return False


def get_generation(prompts_):
    co = cohere.Client('hpaaYCC1MGPwyigl9JhSQg3NCZaLzDkSrYM6Iy6U')
    for prompt_ in prompts_:
        yield co.generate(prompt=prompt_, max_tokens=150, temperature=0.9, k=10)
        print("Completed paragraph")


if __name__ == "__main__":
    paragraphs = get_pdf_paragraphs("https://arxiv.org/pdf/2210.06929.pdf")

    to_rem = []

    for p in paragraphs:
        if p != p:
            to_rem.append(p)
            continue
        if (len(p) < 100) and (NOR(p != paragraphs[0], p != paragraphs[1])) or p[0].islower():
            to_rem.append(p)
            continue
        if p.find("Fig.") != -1 or p.find("doi.org") != -1:
            to_rem.append(p)

    for r in to_rem:
        paragraphs.remove(r)

    prompt = "Summarize the following passage for a presentation: \n ${fPassage} \n\n  Summary:"
    print(len(paragraphs))
    prompts = [prompt.format(fPassage=p) for p in paragraphs[:3]]
    responses = list(get_generation(prompts))

    for e in responses:
        print("START:\n", e.generations[0].text)
