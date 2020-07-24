import os
import subprocess

os.chdir('data/css10')

wanted_speakers = ['p225', 'p226', 'p227', 'p232', 'p233', 'p236', 'p243', 'p244', 'p252', 'p254',
                   'p255', 'p257', 'p262', 'p263', 'p267', 'p268', 'p269', 'p270', 'p273', 'p275',
                   'p276', 'p267', 'p279', 'p282', 'p285', 'p287', 'p294', 'p297', 'p299', 'p300',
                   'p301', 'p302', 'p303', 'p305', 'p306', 'p307', 'p308', 'p310', 'p311', 'p312',
                   'p315', 'p316', 'p329', 'p330', 'p333', 'p334', 'p339', 'p341', 'p343', 'p345',
                   'p360', 'p361', 'p362', 'p363']

with open('entranscript.txt', 'w', encoding='utf-8') as f:
    os.chdir('english/VCTK-Corpus/txt')
    speakers = str(subprocess.check_output(['ls']))
    speakers = speakers[2:-3].split('\\n')
    for speaker in speakers:
        if speaker in wanted_speakers:
            os.chdir(speaker)
            files = str(subprocess.check_output(['ls']))
            files = files[2:-3].split('\\n')
            for file in files:
                with open(file, 'r', encoding='utf-8') as rf:
                    for line in rf:
                        print((file + '|' + line).rstrip(), file=f)
            os.chdir('..')
        else:
            subprocess.call(['rm', '-rf', speaker])

os.chdir('../wavs')

speakers = str(subprocess.check_output(['ls']))
speakers = speakers[2:-3].split('\\n')
for speaker in speakers:
    if speaker not in wanted_speakers:
        subprocess.call(['rm', '-rf', speaker])

