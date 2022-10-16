import cohere
import re
from parsers import get_pdf_paragraphs


def NOR(a, b):
	if a == 0 or b == 0:
		return False
	return True

def removeFromList(paragraphs, removals):
	for r in removals:
		paragraphs.remove(r)

def removeNonAscii(paragraphs):
	to_rem = []

	emailPattern = r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+'
	urlPattern = r'[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)'
	citationPattern = r'(\[\0-9{1,256}\])'
  
	for p in paragraphs:
		if(not p[0].isascii()):
			to_rem.append(p)
	removeFromList(paragraphs, to_rem)

def removeFiguresAndTables(paragraphs):
	figurePattern = r'(^Fi\w+[\.]*[\.\s]*[0-9]+):\s'
	figurePatternWhiteSpace = r'\s(^Fi\w+[\.]*[\.\s]*[0-9]+):\s'
	tablePattern = r'(^Ta\w+[\.]*[\.\s]*[0-9]+):\s'
	tablePatternWhiteSpace = r'\s(^Ta\w+[\.]*[\.\s]*[0-9]+):\s'
	figureDashPattern = r'(^Fi\w+[\.]*[\.\s]*[0-9]+)-\s'
	figureDashWhiteSpace = r'\s(^Fi\w+[\.]*[\.\s]*[0-9]+)-\s'
	tableDashPattern = r'(^Ta\w+[\.]*[\.\s]*[0-9]+)-\s'
	tableDashWhiteSpace = r'\s(^Ta\w+[\.]*[\.\s]*[0-9]+)-\s'
	to_rem = []
	for p in paragraphs:
		if(re.search(figurePattern, p) or re.search(figurePatternWhiteSpace, p)):
			to_rem.append(p)
			continue
		elif(re.search(tablePattern, p) or re.search(tablePatternWhiteSpace, p)):
			to_rem.append(p)
			continue
		elif(re.search(tableDashPattern, p) or re.search(tableDashWhiteSpace, p)):
			to_rem.append(p)
			continue
		elif(re.search(figureDashPattern, p) or re.search(figureDashWhiteSpace, p)):
			to_rem.append(p)
			continue
	removeFromList(paragraphs, to_rem)
	
def removeUrls(paragraphs):
	egiePattern = r'(\w(?=\.))(\.(?=\w))(\w(?=\.))(\.(?=[\b\s.,!?:;]))'
	urlPattern = r'[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)'
	to_rem = []
	for p in paragraphs:
		if(re.search(urlPattern, p) and not re.search(egiePattern, p)):
			to_rem.append(p)
	removeFromList(paragraphs, to_rem)
		
def removeArxiv(paragraphs):
	arXivPattern = r'(ar[xX]iv):([0-9]{1,6}).([0-9]{1-6})'
	to_rem = []
	for p in paragraphs:
		if(re.search(arXivPattern, p)):
			to_rem.append(p)
	removeFromList(paragraphs, to_rem)

def removeEmails(paragraphs):
	emailPattern = r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+'
	to_rem = []
	for p in paragraphs:
		if(re.search(emailPattern, p)):
			to_rem.append(p)
	removeFromList(paragraphs, to_rem)

def removeNonSpaces(paragraphs):
	to_rem = []
	for p in paragraphs:
		if (p.find(' ')== -1):
			to_rem.append(p)
	removeFromList(paragraphs, to_rem)

def removeCitations(paragraphs):
	citationPattern = r'(\[[0-9]{1,4}\]\s)*(([^\.\?\!]*)[\.\?\!])(\s)([0-9]{4}.)\s(\w+)'
	to_rem = []
	for p in paragraphs:
		if(re.search(citationPattern, p)):
			to_rem.append(p)
	removeFromList(paragraphs, to_rem)
	
def removeShort(paragraphs):
	to_rem = []
	for p in paragraphs:
		if ((len(p)<100) and (NOR(p != paragraphs[0], p != paragraphs[1]))):
			to_rem.append(p)
	removeFromList(paragraphs, to_rem)
	
def stripWhitespace(paragraphs):
	loop = 0
	for p in paragraphs:
		paragraphs[loop] = p.strip()
		loop = loop + 1
			
def cleanData(paragraphs):
	stripWhitespace(paragraphs)
	removeNonAscii(paragraphs)
	removeFiguresAndTables(paragraphs)
	removeArxiv(paragraphs)
	removeCitations(paragraphs)
	removeShort(paragraphs)
	removeNonSpaces(paragraphs)
	removeEmails(paragraphs)

<<<<<<< Updated upstream
def cleanData(paragraphs_):
=======

def removeFromList(paragraphs_, removals):
    for r in removals:
        paragraphs_.remove(r)


def removeNonAscii(paragraphs_):
    to_rem = []
    for p in paragraphs_:
        if not p[0].isascii():
            to_rem.append(p)
    removeFromList(paragraphs_, to_rem)


def removeFiguresAndTables(paragraphs_):
    figurePattern = r'(^Fi\w+[\.]*[\.\s]*[0-9]+):[\s]*'
    figurePatternWhiteSpace = r'\s(^Fi\w+[\.]*[\.\s]*[0-9]+):[\s]*'
    tablePattern = r'(^Ta\w+[\.]*[\.\s]*[0-9]+):[\s]*'
    tablePatternWhiteSpace = r'\s(^Ta\w+[\.]*[\.\s]*[0-9]+):[\s]*'
    figureDashPattern = r'(^Fi\w+[\.]*[\.\s]*[0-9]+)-[\s]*'
    figureDashWhiteSpace = r'\s(^Fi\w+[\.]*[\.\s]*[0-9]+)-[\s]*'
    tableDashPattern = r'(^Ta\w+[\.]*[\.\s]*[0-9]+)-[\s]*'
    tableDashWhiteSpace = r'\s(^Ta\w+[\.]*[\.\s]*[0-9]+)-[\s]*'
>>>>>>> Stashed changes
    to_rem = []
    emailPattern = r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+'
    urlPattern = r'[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)'
    citationPattern = r'(\[\0-9{1,256}\])'

    for p in paragraphs_:
        if (len(p) < 100) and (NOR(p != paragraphs_[0], p != paragraphs_[1])):
            to_rem.append(p)
            continue
        elif re.search(emailPattern, p):
            to_rem.append(p)
            continue
        elif re.search(urlPattern, p):
            to_rem.append(p)
            continue
        elif re.search(citationPattern, p):
            to_rem.append(p)
            continue
<<<<<<< Updated upstream
        elif p.find("Fig.") != -1:
=======
    removeFromList(paragraphs_, to_rem)


def removeUrls(paragraphs_):
    egiePattern = r'(\w(?=\.))(\.(?=\w))(\w(?=\.))(\.(?=[\b\s.,!?:;]))'
    urlPattern = r'[-a-zA-Z0-9@:%._\+~#=]{1,75}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)'
    to_rem = []
    for p in paragraphs_:
        if re.search(urlPattern, p) and not re.search(egiePattern, p):
            to_rem.append(p)
    removeFromList(paragraphs_, to_rem)


def removeArxiv(paragraphs_):
    arXivPattern = r'(ar[xX]iv):([0-9]+).([0-9]+)'
    to_rem = []
    for p in paragraphs_:
        if re.search(arXivPattern, p):
            to_rem.append(p)
    removeFromList(paragraphs_, to_rem)


def removeEmails(paragraphs_):
    emailPattern = r'([A-Za-z0-9.-_]){,64}@[A-Za-z0-9]+(\.[A-Z|a-z]{2,})+'
    to_rem = []
    for p in paragraphs_:
        if re.search(emailPattern, p):
            to_rem.append(p)
    removeFromList(paragraphs_, to_rem)


def removeNonSpaces(paragraphs_):
    to_rem = []
    for p in paragraphs_:
        if p.find(' ') == -1:
            to_rem.append(p)
    removeFromList(paragraphs_, to_rem)


def removeCitations(paragraphs_):
    citationPattern = r'(\[[0-9]{1,4}\]\s)*(([^\.\?\!]*)[\.\?\!])(\s)([0-9]{4}.)\s(\w+)'
    to_rem = []
    for p in paragraphs_:
        if re.search(citationPattern, p) or p[0] == "[":
>>>>>>> Stashed changes
            to_rem.append(p)

<<<<<<< Updated upstream
    for r in to_rem:
        paragraphs_.remove(r)
    return paragraphs_

=======
def cleanData(paragraphs_):
    stripWhitespace(paragraphs_)
    removeNonAscii(paragraphs_)
    removeFiguresAndTables(paragraphs_)
    removeArxiv(paragraphs_)
    removeCitations(paragraphs_)
    removeShort(paragraphs_)
    removeNonSpaces(paragraphs_)
    removeEmails(paragraphs_)
>>>>>>> Stashed changes


def get_generation(prompts_):
    co = cohere.Client('hpaaYCC1MGPwyigl9JhSQg3NCZaLzDkSrYM6Iy6U')
    for prompt_ in prompts_:

        yield co.generate(prompt=prompt_, max_tokens=150, temperature=0.9, k=10)
        print("Completed paragraph")


if __name__ == "__main__":
    paragraphs = get_pdf_paragraphs("https://arxiv.org/pdf/2210.07024.pdf")

    paragraphs = cleanData(paragraphs)

    prompt = "Summarize the following passage for a presentation: \n ${fPassage} \n\n  Summary:"
    print(len(paragraphs))
    prompts = [prompt.format(fPassage=p) for p in paragraphs[:3]]
    responses = list(get_generation(prompts))

    for e in responses:
        print("START:\n", e.generations[0].text)
