import os
import sys
import random
import pinyin
import jieba
from xpinyin import Pinyin
import re

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

slr = [
    ("data/css10", "line_index_female_co.tsv"),
    ("data/css10", "line_index_male_co.tsv"),
    ("data/css10", "line_index_female_pe.tsv"),
    ("data/css10", "line_index_male_pe.tsv"),
    ("data/css10", "line_index_female_ve.tsv"),
    ("data/css10", "line_index_male_ve.tsv")
]


zhtranscript = [
    ("data/css10", "zhtranscript.txt")
]

entranscript = [
    ("data/css10", "entranscript.txt")
]

STCMDS = [
    ("data/css10", "STCMDStrans.txt")
]

siwis = [
    ("data/css10", "all_prompts_part1.txt"),
    ("data/css10", "all_prompts_part2.txt")
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
                info[1] = "000-" + info[2]
                if fs == "train.txt":
                    metadata[0][2].append(info)
                else:
                    metadata[1][2].append(info)




for d, fs in lj_speech:
    with open(os.path.join(d, fs), 'r', encoding='utf-8') as f:
        cntr = 0
        for line in f:
            line = line.rstrip().split('|')
            new_stuff = ["0" + str(70000+cntr), "000-en", "en", "english/wavs/" + line[0] + ".wav", "", "", line[2], ""]
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
                new_stuff = [line[0], "0" + line[1] + "-" + line[2], line[2], line[3], "", "", line[4], ""]
                if(cntr % 100 == 0):
                    metadata[1][2].append(new_stuff)
                else:
                    metadata[0][2].append(new_stuff)
part = 0
for d, fs in siwis:
    part += 1
    with open(os.path.join(d, fs), 'r', encoding='utf-8') as f:
        cntr = 0
        for line in f:
            line = line.rstrip().split('\t')
            cntr += 1
            bad = '«»–'
            for char in bad:
                line[1] = line[1].replace(char, "")
            trans = line[1].strip()
            new_stuff = [0, "027-fr", "fr", "french/siwis/wavs/part" + str(part) + "/" + line[0].split('.')[0] + ".wav", "", "", trans, ""]
            if (cntr % 100 == 0):
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
                en_speakers[speaker] = str(speaker_id).zfill(3)
            new_stuff = [0, en_speakers[speaker] + "-en", "en", "english/VCTK-Corpus/wavs/" + speaker + \
                         "/" + line[0].split('.')[0] + "r.wav", "", "", line[1], ""]
            if cntr % 100 == 0:
                metadata[1][2].append(new_stuff)
            else:
                metadata[0][2].append(new_stuff)


zh_speakers = {}
speaker_id = 7
py = Pinyin()
for d, fs in zhtranscript:
    with open(os.path.join(d, fs), 'r', encoding='utf-8') as f:
        cntr = 0
        for line in f:
            cntr += 1
            line = line.rstrip().split('|')
            speaker = line[0].split('_')[0][1:]
            if speaker not in zh_speakers:
                speaker_id += 1
                zh_speakers[speaker] = str(speaker_id).zfill(3)
            new_stuff = [0, zh_speakers[speaker] + "-zh", "zh", "chinese/data_thchs30/data" + "/" + line[0] + "r.wav", "", "", pinyin.get(line[1]) + "。", ""]
            if cntr % 100 == 0:
                metadata[1][2].append(new_stuff)
            else:
                metadata[0][2].append(new_stuff)

zh_speakers = {}
for d, fs in STCMDS:
    with open(os.path.join(d, fs), 'r', encoding='utf-8') as f:
        cntr = 0
        for line in f:
            cntr += 1
            line = line.rstrip().split('|')
            speaker = line[0][8:14]
            if speaker not in zh_speakers:
                speaker_id += 1
                zh_speakers[speaker] = str(speaker_id).zfill(3)
            seglist = jieba.cut(line[1])
            trans = ""
            for seg in seglist:
                trans += pinyin.get(seg)
                trans += " "
            new_stuff = [0, zh_speakers[speaker] + "-zh", "zh", "chinese/STCMDS" + "/" + line[0] + "r.wav", "", "", trans[:-1] +  "。", ""]
            if cntr % 100 == 0:
                metadata[1][2].append(new_stuff)
            else:
                metadata[0][2].append(new_stuff)

slr_speakers = {}
speaker_id = 0
country_to_slr = {"co" : "72", "pe" : "73", "ve": "75"}
for d, fs in slr:
    cntr = 0
    sorted_lines = []
    gender = fs.split('_')[2]
    slrver = country_to_slr[fs.split('_')[3].split(".")[0]]
    with open(os.path.join(d, fs), 'r', encoding='utf-8') as f:
        for line in f:
            line = line.rstrip().split('\t')
            file_info = line[0].split('_')
            sorted_lines.append((file_info[0] + "_" + file_info[1], file_info[2], line[1].rstrip()))

        sorted_lines = sorted(sorted_lines, key=lambda line: line[0])


    for line in sorted_lines:
        if line[0] not in slr_speakers:
            speaker_id += 1
            slr_speakers[line[0]] = str(speaker_id).zfill(3)
        #print(slr_speakers[line[0] + line[1]] + '|' + line[0] + "_" + line[1] + "_" +line[2] + "|" + line[3])
        cntr += 1
        wav_path = "spanish/" + "slr" + slrver + "/wavs" + gender + "/" + line[0] + "_" + line[1]  + "r.wav"
        new_stuff = [0,   slr_speakers[line[0]] + "-es", "es", wav_path, "", "", line[2], ""]
        if cntr % 100 == 0:
            metadata[1][2].append(new_stuff)
        else:
            metadata[0][2].append(new_stuff)




metadata[0][2].sort(key=lambda data: (data[2], data[1]))
metadata[1][2].sort(key=lambda data: (data[2], data[1]))
#random.shuffle(metadata[1][2])


cntr = 0
lang_max = {'zh' : 50, 'fr': 100, 'es': 100, 'en': 100}
for d, fs, m in metadata:
    valid_data = []
    with open(os.path.join(d, "new"+fs), 'w', encoding='utf-8') as f:
        speaker_cnt = {}
        good_speakers = ['000-en', '000-fr', '027-fr', '000-es', '000-zh']
        for i in m:
            idx, s, l, a, _, _, raw_text, ph = i
            if s not in speaker_cnt:
                speaker_cnt[s] = 0
            if s in good_speakers:
                if speaker_cnt[s] < 4000:
                    speaker_cnt[s] += 1
                    print(f'{str(cntr).zfill(6)}|{s}|{l}|{a}|||{raw_text}|{ph}', file=f)
            else:
                if speaker_cnt[s] < lang_max[l]:
                    speaker_cnt[s] += 1
                    print(f'{str(cntr).zfill(6)}|{s}|{l}|{a}|||{raw_text}|{ph}', file=f)
            # if(s[0:2] == '00' and cntr % 7 < 4 and l != 'zh' and l != 'en'):
            #     print(f'{str(cntr).zfill(6)}|{s}|{l}|{a}|||{raw_text}|{ph}', file=f)
            # elif((s[0:2] != '00' and l != 'en') or (l == 'zh' and cntr % 7 < 5)):
            #     print(f'{str(cntr).zfill(6)}|{s}|{l}|{a}|||{raw_text}|{ph}', file=f)
            # elif(l == 'en' and cntr % 7 < 4):
            #     print(f'{str(cntr).zfill(6)}|{s}|{l}|{a}|||{raw_text}|{ph}', file=f)
            cntr += 1

