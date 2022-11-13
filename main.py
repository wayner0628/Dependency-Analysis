# Author: Wei-Yu Kao
# Student ID: 109550068
# HW ID: HW1
import spacy
import pandas as pd


nlp = spacy.load("en_core_web_sm")

df = pd.read_csv("./dataset.csv")
entry = df.shape[0]
text = []
S = []
V = []
OB = []
text.append(str(df.columns[1]))
S.append(str(df.columns[2]))
V.append(str(df.columns[3]))
OB.append(str(df.columns[4]))

for i in range(entry):
    text.append(str(df.iat[i, 1]))
    S.append(str(df.iat[i, 2]))
    V.append(str(df.iat[i, 3]))
    OB.append(str(df.iat[i, 4]))

entry += 1
ans = {"T/F": []}

for i in range(entry):
    print(i)
    doc = nlp(text[i])
    doc_s = nlp(S[i])
    doc_v = nlp(V[i])
    doc_o = nlp(OB[i])
    pred = False
    v = 0
    for token_v in doc_v:
        if token_v.pos_ == "VERB":
            v += 1
    if v > 1:
        ans["T/F"].append(0)
        continue
    for token_v in doc_v:
        if pred is True:
            break
        for token in doc:
            if token.text == token_v.text:
                if token.pos_ in ["VERB", "ADP", "AUX"]:
                    for token_s in doc_s:
                        if pred is True:
                            break
                        for token2 in doc:
                            if token2.text == token_s.text:
                                if (token.head == token2) or (token2.head == token):
                                    if token2.dep_ in ["nsubj", "nsubjpass", "pobj"]:
                                        for token_o in doc_o:
                                            if pred is True:
                                                break
                                            for token3 in doc:
                                                if token3.text == token_o.text:
                                                    for a in token3.ancestors:
                                                        if a == token:
                                                            pred = True
                                                        if a.pos_ == "VERB" or a.pos_ == "AUX":
                                                            break
    if pred is True:
        ans["T/F"].append(1)
    else:
        ans["T/F"].append(0)

DF = pd.DataFrame(ans)
DF.index.name = "index"
DF.to_csv("./output.csv")
