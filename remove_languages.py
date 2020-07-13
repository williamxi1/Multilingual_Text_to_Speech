import os
import sys
import random

sys.path.insert(0, "../")

files_to_append = [
    ("data/css10", "metadata.txt")
]

files_to_solve = [
    ("data/css10", "train.txt"),
    ("data/css10", "val.txt"),
]

metadata = []
for d, fs in files_to_solve:
    with open(os.path.join(d, fs), 'r', encoding='utf-8') as f:
        metadata.append([d, fs, [line.rstrip().split('|') for line in f]])

for d, fs in files_to_append:
    with open(os.path.join(d, fs), 'r', encoding='utf-8') as f:
        cntr = 0
        for line in f:
            line = line.rstrip().split('|')
            new_stuff = ["0" + str(70000+cntr), "english", "english", "english/wavs/" + line[0] + ".wav", "", "", line[2], ""]
            cntr += 1
            if(cntr % 204 == 0):
                metadata[1][2].append(new_stuff)
            else:
                metadata[0][2].append(new_stuff)
print(f'Please wait, this may take a very long time.')

random.shuffle(metadata[0][2])
#random.shuffle(metadata[1][2])

valid_lang = ["chinese", "english", "spanish", "french"]

for d, fs, m in metadata:
    print(f'Creating spectrograms for: {fs}')
    valid_data = []
    with open(os.path.join(d, "new"+fs), 'w', encoding='utf-8') as f:
        for i in m:
            idx, s, l, a, _, _, raw_text, ph = i
            if l in valid_lang:
                valid_data.append([idx, s, l, a, raw_text, ph])
        #valid_data.sort(key = lambda x:int(x[0]))
        cntr = 1
        for data in valid_data:
            idx, s, l, a, raw_text, ph = data
            if(cntr % 4 != 0 or (l == "chinese" and fs == "train.txt")):
                print(f'{idx}|{s}|{l}|{a}|||{raw_text}|{ph}', file=f)
            cntr += 1

