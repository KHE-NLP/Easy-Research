import cohere
from parsers import get_pdf_paragraphs

paragraphs = get_pdf_paragraphs("https://arxiv.org/pdf/2210.06929.pdf")


to_rem = []

for p in paragraphs:
	if((paragraphs.count(p)>1) or (p[0] == "[") or (len(p)<20)):
		to.remove(p)
	

	

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


