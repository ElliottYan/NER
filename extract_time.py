import origin_data.riedel.Document_pb2 as Document_pb
import os
import timex

def main():
    data_path = "./origin_data/riedel/"
    output_path = "./data/"
    with open(output_path + "processed.txt") as fout:
        for item in os.listdir(data_path):
            with open(data_path + item) as fin:
                doc = Document_pb.Document()
                doc.parseFromString(fin.read())
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

                    s = " ".join(s)
                    # if mentions is smaller than 2, means this may not in my train-test set.
                    if len(m) < 2:
                        valid_set.append(s)
                    whole_doc.append(s)
                timex_found ,whole_doc = timex.tag(" ".join(whole_doc))











if __name__ == "__main__":
    main()