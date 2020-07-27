from pydub import AudioSegment
import os
import subprocess


def remove_silence(sound, silence_threshold=-50.0, chunk_size=50):
    '''
    sound is a pydub.AudioSegment
    silence_threshold in dB
    chunk_size in ms

    iterate over chunks until you find the first one with sound
    '''
    trim_ms = 0 # ms

    assert chunk_size > 0 # to avoid infinite loop

    trimmed_sound = sound[0:chunk_size]

    init_chunk_size = 200
    init_silence_threshold = -40

    while trim_ms < len(sound):
        if(sound[trim_ms:trim_ms + chunk_size].dBFS > silence_threshold):
            trimmed_sound += sound[trim_ms:trim_ms + chunk_size]
        trim_ms += chunk_size

    return trimmed_sound

os.chdir('data/css10/spanish/slr72/wavsfemaleuntrimmed')
wavs = str(subprocess.check_output(['ls']))
wavs = wavs[2:-3].split('\\n')
for wav in wavs:
    print("Trimming: ", wav)
    sound = AudioSegment.from_file(wav, format="wav")
    trimmed_sound = remove_silence(sound)
    trimmed_sound.export(os.path.join(os.path.dirname(os.getcwd()), "wavsfemale", wav), format="wav")


os.chdir('data/css10/spanish/slr72/wavsmaleuntrimmed')
wavs = str(subprocess.check_output(['ls']))
wavs = wavs[2:-3].split('\\n')
for wav in wavs:
    print("Trimming: ", wav)
    sound = AudioSegment.from_file(wav, format="wav")
    trimmed_sound = remove_silence(sound)
    trimmed_sound.export(os.path.join(os.path.dirname(os.getcwd()), "wavsmale", wav), format="wav")

