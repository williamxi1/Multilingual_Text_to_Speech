import os
import subprocess

os.chdir('data/css10/spanish/slr72/wavsfemale')

print("REMOVING")
# subprocess.run(['find . -name "*.bak" -type f -delete'])
for i in range(10):
    subprocess.run(['find', '.', '-name', '*' + str(i) + '.wav', '-type', 'f', '-delete'])
os.chdir('../wavsmale')

for i in range(10):
    subprocess.run(['find', '.', '-name', '*' + str(i) + '.wav', '-type', 'f', '-delete'])
