from pydub import AudioSegment
import os
import subprocess


def remove_silence(sound, silence_threshold=-40.0, chunk_size=150):
    '''
    sound is a pydub.AudioSegment
    silence_threshold in dB
    chunk_size in ms

    iterate over chunks until you find the first one with sound
    '''
    trim_ms = chunk_size # ms

    assert chunk_size > 0 # to avoid infinite loop

    trimmed_sound = sound[0:chunk_size]

    init_chunk_size = 200
    init_silence_threshold = -40

    good = False
    numgood = 0
    first = True
    while trim_ms < len(sound):
        if(sound[trim_ms:trim_ms + chunk_size].dBFS > silence_threshold):
            if first:
                trimmed_sound += sound[min(0, trim_ms - chunk_size):trim_ms]
                first = False
            trimmed_sound += sound[trim_ms:trim_ms + chunk_size]
            good = True
            numgood = 3

        elif good == True:
            trimmed_sound += sound[trim_ms:trim_ms + chunk_size]
            numgood -= 1
            if numgood == 0:
                good = False
        trim_ms += chunk_size

    return trimmed_sound

#os.chdir('data/css10/english/VCTK-Corpus/wavs')
os.chdir('/mnt/c/Users/william.xi/Desktop/es_co_female')


wavs = str(subprocess.check_output(['ls']))
wavs = wavs[2:-3].split('\\n')
for wav in wavs:
    print("Trimming: ", wav)
    sound = AudioSegment.from_file(os.path.join(os.getcwd(),wav), format="wav")
    trimmed_sound = remove_silence(sound)
    trimmed_sound.export(os.path.join(os.path.dirname(os.getcwd()), 'wavsfemale2', wav), format="wav")
    print(len(sound), len(trimmed_sound))

# speakers = str(subprocess.check_output(['ls']))
# speakers = speakers[2:-3].split('\\n')
# for speaker in speakers:
#     os.chdir(speaker)
#     wavs = str(subprocess.check_output(['ls']))
#     wavs = wavs[2:-3].split('\\n')
#     for wav in wavs:
#         print("Trimming: ", wav)
#         sound = AudioSegment.from_file(wav, format="wav")
#         trimmed_sound = remove_silence(sound)
#         trimmed_sound.export(os.path.join(os.getcwd(), wav), format="wav")
#     os.chdir(os.path.dirname(os.getcwd()))


