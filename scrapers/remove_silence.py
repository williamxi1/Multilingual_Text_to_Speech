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
        #print(sound[trim_ms:trim_ms + chunk_size].dBFS)
        if(sound[trim_ms:trim_ms + chunk_size].dBFS > silence_threshold):
            if first:
                trimmed_sound += sound[max(0, trim_ms - 2*chunk_size):trim_ms]
                first = False

            trimmed_sound += sound[trim_ms:trim_ms + chunk_size]
            good = True
            numgood = 2

        elif good == True:
           trimmed_sound += sound[trim_ms:trim_ms + chunk_size]
           numgood -= 1
           if numgood == 0:
               good = False
        trim_ms += chunk_size

    return trimmed_sound


os.chdir('../data/css10/chinese/STCMDS')

wavs = str(subprocess.check_output(['ls']))
wavs = wavs[2:-3].split('\\n')
for wav in wavs:
    print("Trimming: ", wav)
    sound = AudioSegment.from_file(wav, format="wav")
    trimmed_sound = remove_silence(sound)
    trimmed_sound.export(wav, format="wav")
    print(len(sound), len(trimmed_sound))
os.chdir('..')



