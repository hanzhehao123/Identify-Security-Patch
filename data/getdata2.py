from os import write
from git import Repo
import csv
import re

N = 1000

content = []
keywordslist = []

with open('keywordslist.txt','r',encoding='utf-8') as f:
    for line in f:
        keywordslist.append(line.strip())

with open('hash.txt') as f:
    for line in f:
        content.append(line.strip())

for i in range(10):
    print(content[i])

repo = Repo('qemu')
git = repo.git

with open('testdata\qemu3_cm.csv','w',encoding='utf-8',newline='') as f:
    csv_writer = csv.writer(f)
    csv_writer.writerow(['label','content','hash'])
    for i in range(N):
        result1 = git.log(content[i],'-1')
        csv_writer.writerow(['0',result1,content[i]])

with open('testdata\qemu3_cr.csv','w',encoding='utf-8',newline='') as f:
    csv_writer = csv.writer(f)
    csv_writer.writerow(['label','content','hash'])
    for i in range(N):
        result2 = git.diff(content[i],content[i+1])
        if (len(result2) > 150000):
            result2 = result2[0:15000]
        csv_writer.writerow(['0',result2,content[i]])

with open('testdata\qemu3.csv','w',encoding='utf-8',newline='') as f:
    hashes = []
    cms = []
    crs = []

    csv_writer = csv.writer(f)
    csv_writer.writerow(['hash id','commit message','code revision'])
    for i in range(N):
        result1 = git.log(content[i],'-1')
        result2 = git.diff(content[i],content[i+1])
        if (len(result2) > 150000):
            result2 = result2[0:15000]
        csv_writer.writerow([content[i],result1,result2])
        hashes.append(content[i])
        cms.append(result1)
        crs.append(result2)

    with open('testdata\\filtered\qemu3_cr.csv','w',encoding='utf-8',newline='') as fr:
        cr_writer = csv.writer(fr)
        cr_writer.writerow(['label','content','hash'])
        with open('testdata\\filtered\qemu3_cm.csv','w',encoding='utf-8',newline='') as fm:
            cm_writer = csv.writer(fm)
            cm_writer.writerow(['label','content','hash'])
            for i in range(N):
                for word in keywordslist:
                    result = re.search(word, cms[i])
                    if(result):
                        cm_writer.writerow(['0', cms[i], hashes[i]])
                        cr_writer.writerow(['0', crs[i], hashes[i]])
                        break

