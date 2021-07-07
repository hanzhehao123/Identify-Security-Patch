import re
import os
import shutil

keywordslist = []
with open('keywordslist.txt','r',encoding='utf-8') as f:
    for line in f:
        keywordslist.append(line.strip())

listdir = os.listdir('testdata\commitmessage')

for name in listdir:
    with open('testdata\commitmessage\\'+name,'r',encoding='utf-8') as fm:
        content = fm.read().lower()
        result = 0
        flag = 0
        for word in keywordslist:
            result = re.search(word, content)
            if result:
                flag = 1
                shutil.copyfile('testdata\commitmessage\\'+name,'testdata\\filtered\commitmessage\\'+name)
                shutil.copyfile('testdata\coderevision\\'+name,'testdata\\filtered\coderevision\\'+name)
                break
        if flag == 0 :
            shutil.copyfile('testdata\commitmessage\\'+name,'testdata\\filtered\commitmessage_D\\'+name)
            shutil.copyfile('testdata\coderevision\\'+name,'testdata\\filtered\coderevision_D\\'+name)
