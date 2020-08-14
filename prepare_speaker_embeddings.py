from resemblyzer import VoiceEncoder, preprocess_wav
import os
import numpy as np
import torch

def getSpeakerEmbeddings(speaker_ids):
    print("Obtaining Embeddings")
    if os.path.exists('speakerEmbeddings.npy'):
        print("Loading Pre-existing Embeddings")
        speakerEmbeddings = np.load('speakerEmbeddings.npy')
        speakerEmbeddings = torch.tensor(speakerEmbeddings, dtype = torch.float)
        return speakerEmbeddings

    numSpeakers = len(speaker_ids)
    speakerEmbeddings = [np.zeros(256) for i in range(numSpeakers)]
    speakerUtterances = [[] for i in range(numSpeakers)]
    with open(os.path.join("data/css10", "train.txt"), 'r', encoding='utf-8') as f:
        for line in f:
            line = line.rstrip().split("|")
            speaker = line[1]
            if speaker in speaker_ids:
                speaker_index = speaker_ids.index(speaker)
                if len(speakerUtterances[speaker_index]) < 50:
                    wavpath = line[3]
                    speakerUtterances[speaker_index].append(wavpath)

    wavs = [[] for i in range(numSpeakers)]
    for i, speaker in enumerate(speaker_ids):
        for utterance in speakerUtterances[i]:
            print("Preprocessing ", utterance)
            wavs[i].append(preprocess_wav(os.path.join(os.path.join(os.getcwd(), "data/css10"), utterance)))

    encoder = VoiceEncoder()

    for i, speaker_wavs in enumerate(wavs):
        for j, wav in enumerate(speaker_wavs):
            print("Embedding ", i, j)
            speakerEmbeddings[i] += np.asarray(encoder.embed_utterance(wav))
        speakerEmbeddings[i] /= len(speaker_wavs)
    speakerEmbeddings = np.asarray(speakerEmbeddings)
    speakerEmbeddings = torch.tensor(speakerEmbeddings, dtype = torch.float)
    np.save('speakerEmbeddings.npy', speakerEmbeddings)
    return speakerEmbeddings


if __name__ == '__main__':
    #speaker_ids = ["00-zh", "00-en", "00-fr", "00-sp"]
    #speakerEmbeddings = getSpeakerEmbeddings(speaker_ids)
    # np.set_printoptions(suppress=True)
    #speakerEmbeddings = np.asarray(speakerEmbeddings)
    # for embedding in speakerEmbeddings:
    #     print(len(embedding))
    # np.save('speakerEmbeddings.npy', speakerEmbeddings)
    #print(speakerEmbeddings[4])

    print(os.path.dirname(os.getcwd()))
    wav1 = preprocess_wav(os.path.join(os.path.dirname(os.getcwd()), "audiodata/penelope.wav"))
    encoder = VoiceEncoder()
    speakerEmbeddings1 = encoder.embed_utterance(wav1)
    np.save('speaker_embeds/penelope.npy', speakerEmbeddings1)



