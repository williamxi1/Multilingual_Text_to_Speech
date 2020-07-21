import os
import sys
import random

sys.path.insert(0, "../")

lj_speech = [
    ("data/css10", "metadata.txt")
]

comvoi = [
    ("data/comvoi_clean", "all.txt")
]

files_to_solve = [
    ("data/css10", "train.txt"),
    ("data/css10", "val.txt"),
]

metadata = [["data/css10", "train.txt", []], ["data/css10", "val.txt", []]]
valid_lang = ["chinese", "english", "spanish", "french", "zh", "fr"]
lang_to_id = {"chinese" : "zh", "english" : "en", "spanish" : "sp", "french" : "fr"}
id_to_lang = {"zh" : "chinese", "en" : "english", "sp" : "spanish", "fr" : "french"}
for d, fs in files_to_solve:
    cntr = 0
    with open(os.path.join(d, fs), 'r', encoding='utf-8') as f:
        for line in f:
            info = line.rstrip().split('|')
            idnum, speaker, language, wavpath, _, _, transcript, _ = info
            if info[2] in valid_lang:
                cntr += 1
                info[2] = lang_to_id[info[2]]
                info[1] = "00-" + info[2]
                if fs == "train.txt":
                    metadata[0][2].append(info)
                else:
                    metadata[1][2].append(info)



for d, fs in lj_speech:
    with open(os.path.join(d, fs), 'r', encoding='utf-8') as f:
        cntr = 0
        for line in f:
            line = line.rstrip().split('|')
            new_stuff = ["0" + str(70000+cntr), "00-en", "en", "english/wavs/" + line[0] + ".wav", "", "", line[2], ""]
            cntr += 1
            if(cntr % 192 == 0):
                metadata[1][2].append(new_stuff)
            else:
                metadata[0][2].append(new_stuff)

for d, fs in comvoi:
    with open(os.path.join(d, fs), 'r', encoding='utf-8') as f:
        cntr = 0
        for line in f:
            line = line.rstrip().split('|')
            if line[2] in id_to_lang:
                cntr += 1
                wavpath = line[3].split('/')
                wavpath[0] = id_to_lang[wavpath[0]]
                wavpath = "/".join(wavpath)
                new_stuff = [line[0], line[1] + "-" + line[2], line[2], wavpath, "", "", line[4], ""]
                if(cntr % 100 == 0):
                    metadata[1][2].append(new_stuff)
                else:
                    metadata[0][2].append(new_stuff)

random.shuffle(metadata[0][2])
#random.shuffle(metadata[1][2])



for d, fs, m in metadata:
    valid_data = []
    with open(os.path.join(d, "new"+fs), 'w', encoding='utf-8') as f:
        for i in m:
            if len(i) != 8: print(i)
            idx, s, l, a, _, _, raw_text, ph = i
            print(f'{idx}|{s}|{l}|{a}|||{raw_text}|{ph}', file=f)

