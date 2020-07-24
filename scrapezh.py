import os
import subprocess

os.chdir('data/css10')

with open('zhtranscript.txt', 'w', encoding='utf-8') as f:
    os.chdir('chinese/data_thchs30/data')
    files = str(subprocess.check_output(['ls']))
    files = files[2:-3].split('\\n')
    for file in files:
        if file.split('.')[-1] == 'trn':
            with open(file, 'r', encoding='utf-8') as rf:
                for line in rf:
                    print((file.split('.')[0] + '|' + line).rstrip(), file=f)
                    break