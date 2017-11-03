from __future__ import absolute_import
from origin_data.riedel import Document_pb2
import os
import timex
import pdb


# Now we need to process wikipedia text for timex extraction
def main():
    data_path = "./origin_data/riedel/nyt-2005-2006.backup/"
    output_path = "./data/"
    with open(output_path + "processed.txt", "wb") as fout:
        outputs = []
        for item in os.listdir(data_path):
            with open(data_path + item, "rb") as fin:
                if item[-3:] != ".pb":
                    continue
                # pdb.set_trace()
                doc = Document_pb2.Document()
                doc.ParseFromString(fin.read())
                # whole_doc is for time extraction
                whole_doc = []
                valid_set = []
                for sentence in doc.sentences:
                    s = []
                    m = []
                    t = []
                    # extract the token words into one sentence.
                    for token in sentence.tokens:
                        s.append(token.word)
                    # extract mentions
                    for mention in sentence.mentions:
                        # mention got entity_name, mform, to
                        m.append(["_".join(s[int(mention.mfrom):int(mention.to+1)]), mention.mfrom, mention.to])
                    # if mentions is smaller than 2, means this may not in my train-test set.
                    # in this case, the mention could be bigger than 2, so we may need iterations for further processing.
                    if len(m) < 2:
                        valid_set.append([m, s])
                    whole_doc.append(s)
                # tagging op should appear in each doc iter
                # since we need the whole doc to set base-time
                timex_found, whole_doc = timex.tag(" ".join(whole_doc))
                if len(timex_found) > 0:
                    # set base-time tobe the last time found.
                    base_t = timex.retrieve_Date_time(timex_found)

                pdb.set_trace()











if __name__ == "__main__":
    main()