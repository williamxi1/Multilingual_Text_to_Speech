import os
import subprocess

os.chdir('../../Desktop/es_co_female')

print("REMOVING")
# subprocess.run(['find . -name "*.bak" -type f -delete'])
for i in range(10):
    subprocess.run(['find', '.', '-name', '*' + str(i) + '.wav', '-type', 'f', '-delete'])

