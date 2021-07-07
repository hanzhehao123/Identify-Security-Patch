import csv
import re
import nltk
from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords




train_f = open("data\\traindata\coderevision_new\\train\\qemu2_addsub.csv", "r", encoding="utf-8")
evaluate_f = open("data\\traindata\coderevision_new\evaluate\\qemu2_addsub.csv", "r", encoding="utf-8")
train_csv = csv.reader(train_f)
evaluate_csv = csv.reader(evaluate_f)
csvlist=[train_csv, evaluate_csv]

dic0={}
dic1={}

porter_stemmer=PorterStemmer()# 词干提取
mystop = ['{','}','(',')',';',',','>','<','=','&','#',':','[',']','\'\'','``','/*','*/','\\\\']

for i in range(len(csvlist)):
    input_rows = []
    for line in csvlist[i]:
        input_rows.append(line)

    for line, row in enumerate(input_rows):
        # print(line)
        if line==0 or len(row)!=2:
            continue
        else:
            txt = re.sub('-----', "", row[1])
            txt = re.sub('\+\+\+\+\+', "", txt)
            txt = porter_stemmer.stem(txt.lower())  #小写、词干提取
            words = nltk.word_tokenize(txt)   #分词
            keys = list(set(words))
            for key in keys:
                if (key not in stopwords.words('english')) and (key not in mystop): #除去停用词
                    if row[0]=='0':
                        if key in dic0.keys():
                            dic0[key] = dic0[key] + 1
                        else:
                            dic0[key] = 1
                    else:
                        if key in dic1.keys():
                            dic1[key] = dic1[key] + 1
                        else:
                            dic1[key] = 1




dstf = open(".\\word_frequece.csv", "w", encoding='utf-8', newline='')
dstcsv = csv.writer(dstf)


dstcsv.writerow(['token','0','1','sub'])
for key in dic1.keys():
    sub = dic1[key]
    if key in dic0.keys():
        sub = sub - dic0[key]
        print('token:' + str(key) + '  0:' + str(dic1[key]-sub) + '  1:' + str(dic1[key]) + '  sub:' + str(sub))
        dstcsv.writerow([key, dic1[key]-sub, dic1[key], sub])