import os
import subprocess

os.chdir('data/css10/spanish/slr72/wavsfemale')
speakers = str(subprocess.check_output(['ls']))
speakers = speakers[2:-3].split('\\n')
print("REMOVING")
# subprocess.run(['find . -name "*.bak" -type f -delete'])
for speaker in speakers:
    os.chdir(speaker)
    #ubprocess.run(['for', 'i', 'in', '*wav;','do', 'echo', '$i;', 'sox', '$i', '-r', '22050', '${i%%.wav}r.wav; done])
    for i in range(10):
        subprocess.run(['find', '.', '-name', '*' + str(i) + '.wav', '-type', 'f', '-delete'])
    os.chdir('..')
