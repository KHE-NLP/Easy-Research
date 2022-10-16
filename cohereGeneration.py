import cohere
import re
from parsers import get_pdf_paragraphs


def NOR(a, b):
    if a == 0 or b == 0:
        return False
    return True

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
    to_rem = []
    for p in paragraphs_:
        if re.search(figurePattern, p) or re.search(figurePatternWhiteSpace, p):
            to_rem.append(p)
            continue
        elif re.search(tablePattern, p) or re.search(tablePatternWhiteSpace, p):
            to_rem.append(p)
            continue
        elif re.search(tableDashPattern, p) or re.search(tableDashWhiteSpace, p):
            to_rem.append(p)
            continue
        elif re.search(figureDashPattern, p) or re.search(figureDashWhiteSpace, p):
            to_rem.append(p)
            continue
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
            to_rem.append(p)
    removeFromList(paragraphs_, to_rem)


def removeShort(paragraphs_):
    to_rem = []
    for p in paragraphs_:
        if (len(p) < 100) and (NOR(p != paragraphs_[0], p != paragraphs_[1])):
            to_rem.append(p)
    removeFromList(paragraphs_, to_rem)


def stripWhitespace(paragraphs_):
    loop = 0
    for p in paragraphs_:
        paragraphs_[loop] = p.strip()
        loop = loop + 1


def cleanData(paragraphs_):
    stripWhitespace(paragraphs_)
    removeNonAscii(paragraphs_)
    removeFiguresAndTables(paragraphs_)
    removeArxiv(paragraphs_)
    removeCitations(paragraphs_)
    removeShort(paragraphs_)
    removeNonSpaces(paragraphs_)
    removeEmails(paragraphs_)

def get_generation(prompts_):
    co = cohere.Client('hpaaYCC1MGPwyigl9JhSQg3NCZaLzDkSrYM6Iy6U')
    for prompt_ in prompts_:
        yield co.generate(prompt=prompt_, max_tokens=150, temperature=0.9, k=10, stop_sequences=["Passage:"])
        print("Completed paragraph")


if __name__ == "__main__":
    paragraphs = get_pdf_paragraphs("https://arxiv.org/pdf/2210.07024.pdf")

    cleanData(paragraphs)

    prefix = """Passage:
    We present SELOR, a framework for integrating self-explaining capabilities into a
given deep model to achieve both high prediction performance and human precision.
By “human precision”, we refer to the degree to which humans agree with the
reasons models provide for their predictions. Human precision affects user trust and
allows users to collaborate closely with the model. We demonstrate that logic rule
explanations naturally satisfy human precision with the expressive power required
for good predictive performance. We then illustrate how to enable a deep model
to predict and explain with logic rules. Our method does not require predeﬁned
logic rule sets or human annotations and can be learned efﬁciently and easily with
widely-used deep learning modules in a differentiable way. Extensive experiments
show that our method gives explanations closer to human decision logic than other
methods while maintaining the performance of deep learning models.

Summary:
SELOR is a framework to give predictions that are similar to what a human would give.
It does this while still using deep learning, which allows it to adapt.

Passage:
Datasets. We conduct experiments on three datasets. The ﬁrst two are textual, and the third is tabular.
Yelp classiﬁes reviews of local businesses into positive or negative sentiment [44], and Clickbait
News Detection from Kaggle labels whether a news article is a clickbait [45]. Adult from the UCI
machine learning repository [46], is an imbalanced tabular dataset that provides labels about whether
the annual income of an adult is more than $50K/yr or not. For Yelp, we use a down-sampled subset
(10%) for training, as per existing work [39]. More details about the datasets are in Appendix C.1.

Summary:
The article used datasets from Yelp, Clickbait News Detection, and a dataset of annual incomes.

Passage:
Complexity analysis. Time complexity is com-
pared in Table 1. The complexity for antecedent
generation corresponds to the time added for
generating the antecedents during model training
compared to the time required for training the
base deep model f . Here, N is the number of
training samples, and C is the time complexity
for computing the consequent of each antecedent.
As shown in the table, removing the recursive
antecedent generator (RG) or the neural conse-
quent estimator (NE) brings an additional linear
complexity with the number of feasible antecedents A, which is much larger than A(cid:48). For example,
in our experiment, setting A(cid:48) to 104 is good enough to train an accurate neural consequent estimator,
while the number of all possible antecedents is A = 6.25 × 1012. Here, we do not include the analysis
for sampling A(cid:48) rules before training the consequent estimator. See Appendix B.4 for more details.

Summary:
The time complexity of the training is linear with respect to A, which is pretty good.
"""
    
    prompt = "Passage: \n {fPassage} \n\n  Summary:"
    print(len(paragraphs))
    prompts = [prompt.format(fPassage=p) for p in paragraphs[12:13]]
    prompts_with_prefix = [prefix + p for p in prompts]
    responses = list(get_generation(prompts_with_prefix))

    for p, e in zip(prompts, responses):
        print("REAL:\n", p)
        print("SUMM:\n", e.generations[0].text)
