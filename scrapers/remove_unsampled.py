import os
import subprocess


os.chdir('../data/css10/english/VCTK-Corpus/wavs')

speakers = str(subprocess.check_output(['ls']))
speakers = speakers[2:-3].split('\\n')
for speaker in speakers:
    os.chdir(speaker)
    subprocess.run('for i in *wav; do echo $i; sox $i -r 22050 ${i%%.wav}r.wav; done', shell=True)
    print("REMOVING")
    for i in range(10):
        subprocess.run(['find', '.', '-name', '*' + str(i) + '.wav', '-type', 'f', '-delete'])
    os.chdir('..')

