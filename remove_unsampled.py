import os
import subprocess

os.chdir('data/css10/chinese/data_thchs30/data')

print("REMOVING")
# subprocess.run(['find . -name "*.bak" -type f -delete'])
for i in range(10):
    subprocess.run(['find', '.', '-name', '*' + str(i) + '.wav', '-type', 'f', '-delete'])

