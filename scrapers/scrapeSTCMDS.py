import os
import subprocess

os.chdir('../data/css10')

with open('STCMDStrans.txt', 'w', encoding='utf-8') as f:
    os.chdir('chinese/STCMDS')
    files = str(subprocess.check_output(['ls']))
    files = files[2:-3].split('\\n')
    for file in files:
        if file.split('.')[-1] == 'txt':
            with open(file, 'r', encoding='utf-8') as rf:
                for line in rf:
                    print((file.split('.')[0] + '|' + line).rstrip(), file=f)
                    break
            #subprocess.call(['rm', file])