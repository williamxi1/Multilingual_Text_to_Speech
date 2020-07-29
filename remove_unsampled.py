import os
import subprocess

os.chdir('data/css10/english/VCTK-Corpus/wavs')

speakers = str(subprocess.check_output(['ls']))
speakers = speakers[2:-3].split('\\n')

print(speakers)

for speaker in speakers:
    os.chdir(speaker)
    print("REMOVING")
   # subprocess.run(['find . -name "*.bak" -type f -delete'])
    for i in range(10):
        subprocess.run(['find', '.', '-name', '*' + str(i) + '.wav', '-type', 'f', '-delete'])
    os.chdir('..')
