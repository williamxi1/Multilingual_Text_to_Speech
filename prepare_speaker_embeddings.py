from resemblyzer import VoiceEncoder, preprocess_wav
import os
import numpy as np
import torch

def getSpeakerEmbeddings(speaker_ids):
    numSpeakers = len(speaker_ids)
    speakerEmbeddings = [None for i in range(numSpeakers)]
    speakerUtterances = [[] for i in range(numSpeakers)]
    with open(os.path.join("data/css10", "newtrain.txt"), 'r', encoding='utf-8') as f:
        for line in f:
            line = line.rstrip().split("|")
            speaker = line[1]
            if speaker in speaker_ids:
                speaker_index = speaker_ids.index(speaker)
                if len(speakerUtterances[speaker_index]) < 1:
                    wavpath = line[3]
                    speakerUtterances[speaker_index].append(wavpath)

    wavs = [[] for i in range(numSpeakers)]
    for i, speaker in enumerate(speaker_ids):

        for utterance in speakerUtterances[i]:
            wavs[i].append(preprocess_wav(os.path.join(os.path.join(os.getcwd(), "data/css10"), utterance)))

    encoder = VoiceEncoder()

    for i, speaker_wavs in enumerate(wavs):
        for wav in speaker_wavs:
            speakerEmbeddings[i] = encoder.embed_utterance(wav)

    return speakerEmbeddings


if __name__ == '__main__':
    speaker_ids = ["00-zh", "00-en", "00-fr", "00-sp"]
    speakerEmbeddings = getSpeakerEmbeddings(speaker_ids)
    np.set_printoptions(suppress=True)
    for embedding in speakerEmbeddings:
        print(embedding)


