import cohere
import re
from parsers import get_pdf_paragraphs

def NOR(a, b):
	if a == 0 or b == 0:
		return False
	return True

def cleanData(paragraphs):
	to_rem = []
	emailPattern = r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+'
	urlPattern = r'[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)'
	citationPattern = r'(\[\0-9{1,256}\])'
	
	for p in paragraphs:
		if ((len(p)<100) and (NOR(p != paragraphs[0], p != paragraphs[1]))):
			to_rem.append(p)
			continue
		elif(re.search(emailPattern, p)):
			to_rem.append(p)
			continue
		elif(re.search(urlPattern, p)):
			to_rem.append(p)
			continue
		elif(re.search(citationPattern, p)):
			to_rem.append(p)
			continue
		elif(p.find("Fig.")!=-1):
			to_rem.append(p)

	for r in to_rem:
		paragraphs.remove(r)
	return paragraphs
		

paragraphs = get_pdf_paragraphs("https://arxiv.org/pdf/2210.06929.pdf")


cleanData(paragraphs)


co = cohere.Client('hpaaYCC1MGPwyigl9JhSQg3NCZaLzDkSrYM6Iy6U')
responses = "Format: Title:, Author(s): Summarize the following passage for a presentation: \n ${} \n\n  Summary:"

stopsequences = ['\n\n', '\t']
response = co.generate(prompt=responses[0], max_tokens=150, temperature=0.9, k=10)
print(response.generations[0].text)
