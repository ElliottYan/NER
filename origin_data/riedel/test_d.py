import Document_pb2
import os
import pdb

path = "./nyt-2005-2006.backup/"
f = open(path+os.listdir(path)[0],"rb")
doc = Document_pb2.Document()

doc.ParseFromString(f.read())

for sentence in doc.sentences:
    s = []
    m = []
    for token in sentence.tokens:
        s.append(token.word)
    for mention in sentence.mentions:
        pdb.set_trace()
        m.append(mention)
    print(s)
    print(m)


