# from origin_data.riedel import Document_pb2
import os
import pdb
import timex
import re

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


# we first need to seperate the document separately.
# each file end with a </doc>
def parse_wiki():
    data_path = "../wiki-data/"
    out_path = "../wiki-tagged-data/"
    dirs = os.listdir(data_path)
    count = 0
    for dir in dirs:
        path = data_path + dir + "/"
        for files in os.listdir(path):
            count += 1
            with open(path + files, "r") as f:
                lines = f.readlines()
                index = 0
                # for each doc
                while index < len(lines):
                    # denoting the starting line of a document
                    start = index
                    title = "_".join(re.split(r'[^a-z|0-9]', lines[index+1].strip().lower()))
                    while lines[index].strip() != "</doc>":
                        index += 1
                    end = index
                    # next line is the next start
                    index += 1

                    text = " ".join(lines[start:end])
                    # call the modified ground func
                    text = timex.ground(text)
                    with open(out_path + title, 'a') as fout:
                        fout.write(text)
                    # if count >= 5:
                    #     return


if __name__ == "__main__":
    # main()
    parse_wiki()