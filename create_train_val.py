import os
import sys
import random
import pinyin

sys.path.insert(0, "../")

lj_speech = [
    ("data/css10", "metadata.txt")
]

comvoi = [
    ("data/comvoi_clean", "all.txt")
]

css10 = [
    ("data/css10", "train.txt"),
    ("data/css10", "val.txt"),
]

slr72 = [
    ("data/css10", "line_index_female.tsv"),
    ("data/css10", "line_index_male.tsv")
]

zhtranscript = [
    ("data/css10", "zhtranscript.txt")
]

entranscript = [
    ("data/css10", "entranscript.txt")
]

metadata = [["data/css10", "train.txt", []], ["data/css10", "val.txt", []]]
valid_lang = ["chinese", "english", "spanish", "french", "zh", "fr"]
lang_to_id = {"chinese" : "zh", "english" : "en", "spanish" : "es", "french" : "fr"}
id_to_lang = {"zh" : "chinese", "en" : "english", "es" : "spanish", "fr" : "french"}


for d, fs in css10:
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
                line[3] = id_to_lang[line[2]] + "/" + line[3]
                new_stuff = [line[0], line[1] + "-" + line[2], line[2], line[3], "", "", line[4], ""]
                if(cntr % 100 == 0):
                    metadata[1][2].append(new_stuff)
                else:
                    metadata[0][2].append(new_stuff)

en_speakers = {}
speaker_id = 0

for d, fs in entranscript:
    with open(os.path.join(d,fs), 'r', encoding='utf-8') as f:
        cntr = 0
        for line in f:
            cntr += 1
            line = line.rstrip().split('|')
            speaker = line[0].split('_')[0]
            if speaker not in en_speakers:
                speaker_id += 1
                en_speakers[speaker] = str(speaker_id).zfill(2)
            new_stuff = [0, en_speakers[speaker] + "-en", "en", "english/VCTK-Corpus/wavs/" + speaker + \
                         "/" + line[0].split('.')[0] + "r.wav", "", "", line[1], ""]
            if cntr % 100 == 0:
                metadata[1][2].append(new_stuff)
            else:
                metadata[0][2].append(new_stuff)


zh_speakers = {}
speaker_id = 7
for d, fs in zhtranscript:
    with open(os.path.join(d, fs), 'r', encoding='utf-8') as f:
        cntr = 0
        for line in f:
            cntr += 1
            line = line.rstrip().split('|')
            speaker = line[0].split('_')[0][1:]
            if speaker not in zh_speakers:
                speaker_id += 1
                zh_speakers[speaker] = str(speaker_id).zfill(2)
            new_stuff = [0, zh_speakers[speaker] + "-zh", "zh", "chinese/data_thchs30/data" + "/" + line[0] + "r.wav", "", "", pinyin.get(line[1]), ""]
            if cntr % 100 == 0:
                metadata[1][2].append(new_stuff)
            else:
                metadata[0][2].append(new_stuff)

slr_speakers = {}
speaker_id = 0
for d, fs in slr72:
    cntr = 0
    sorted_lines = []
    gender = fs.split('_')[2].split(".")[0]
    with open(os.path.join(d, fs), 'r', encoding='utf-8') as f:
        for line in f:
            line = line.rstrip().split('\t')
            file_info = line[0].split('_')
            sorted_lines.append((file_info[0], file_info[1], file_info[2], line[1].rstrip()))

        sorted_lines = sorted(sorted_lines, key=lambda line: line[1])


    for line in sorted_lines:
        if line[0] + line[1] not in slr_speakers:
            speaker_id += 1
            slr_speakers[line[0] + line[1]] = str(speaker_id).zfill(2)
        #print(slr_speakers[line[0] + line[1]] + '|' + line[0] + "_" + line[1] + "_" +line[2] + "|" + line[3])
        cntr += 1
        wav_path = "spanish/slr72/wavs" + gender + "/" + line[0] + "_" + line[1] + "_" + line[2] + "r.wav"
        new_stuff = [0,   slr_speakers[line[0] + line[1]] + "-es", "es", wav_path, "", "", line[3], ""]
        if cntr % 100 == 0:
            metadata[1][2].append(new_stuff)
        else:
            metadata[0][2].append(new_stuff)

chinese_speakers = {}



metadata[0][2].sort(key=lambda data: (data[2], data[1]))
metadata[1][2].sort(key=lambda data: (data[2], data[1]))
#random.shuffle(metadata[1][2])


cntr = 0
for d, fs, m in metadata:
    valid_data = []
    with open(os.path.join(d, "new"+fs), 'w', encoding='utf-8') as f:
        for i in m:
            idx, s, l, a, _, _, raw_text, ph = i
            if(cntr % 7 < 4 or (l != "en")):
                print(f'{str(cntr).zfill(6)}|{s}|{l}|{a}|||{raw_text}|{ph}', file=f)
            cntr += 1

