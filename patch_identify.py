import csv
import re

import nltk
from nltk.stem.porter import PorterStemmer

porter_stemmer=PorterStemmer()# 词干提取

permissionslist = []
with open('permission.txt','r',encoding='utf-8') as f:
    for line in f:
        permissionslist.append(line.strip())
    f.close()

def memory_leak_check(content):
    flag = 0
    new_content = ''.join(content)
    content_list = list(new_content.lower().split('\n'))

    for text in content_list:
        if not flag:
            if re.search('\+\+\+\+\+.*free\s*[(]', text) or re.search('\+\+\+\+\+.*delete', text):
                flag = 1
                break

    return flag

def locks_check(content):
    flag = 0
    new_content = ''.join(content)
    content_list = list(new_content.lower().split('\n'))

    for text in content_list:
        if not flag:
            if re.search('\+\+\+\+\+.*lock\s*[(]', text) or re.search('\+\+\+\+\+.*\s*mutex', text):
                flag = 1
                break

    return flag

def permission_check(content):
    flag = 0
    # content = []
    # with open('example.txt','r',encoding='utf-8') as f:
    #     content = f.read().split('\n')
    # print(content[0])
    new_content = ''.join(content)
    content_list = list(new_content.lower().split('\n'))

    for text in content_list:
        if not flag:
            for word in permissionslist:
                if re.search('\+\+\+\+\+.*if\s*[(]',text) or re.search('\+\+\+\+\+.*while\s*[(]',text) or re.search('\+\+\+\+\+.*switch\s*[(]',text) or re.search('\+\+\+\+\+.*else\s*[(]',text):
                    result = re.search('[(].*'+word+'.*[)]', text)
                    if result:
                        flag = 1
                        # print(text)
                        break
    
    return flag

def initial_check(content):
    new_content = ''.join(content)
    content_list = list(new_content.lower().split('\n'))

    index = []
    val = []
    for i in range(len(content_list)):
        text = content_list[i]
        if re.search('\+\+\+\+\+[0-9a-z]*=\s*0', text):
            index.append(i)
            val.append(re.findall("\+\+\+\+\+([0-9a-z]*)=\s*0", text)[0].strip())
        elif re.search('\+\+\+\+\+[0-9a-z]*=\s*null', text):
            index.append(i)
            val.append(re.findall("\+\+\+\+\+([0-9a-z]*)=\s*null", text)[0].strip())

    for i in range(len(index)):
        tmp = 0
        for j in range(index[i]):
            add_text = content_list[j][0:5]
            if add_text != '+++++':
                if re.search(val[i], content_list[j]) != None:
                    tmp = 1
        if tmp == 0:
            for j in range(index[i],len(content_list),1):
                add_text = content_list[j][0:5]
                if add_text != '+++++':
                    if re.search(val[i], content_list[j]) != None:
                        return 1

    for text in content_list:
        if re.search('\+\+\+\+\+.*memset[(].*,\s*0[)]', text):
            return 1

    return 0

def pointer_check(content):
    new_content = ''.join(content)
    content_list = list(new_content.lower().split('\n'))

    freeindex = []
    freeval = []
    for i in range(len(content_list)):
        text = content_list[i]
        if re.search(".*free\s*\(\s*([0-9a-z]*)\s*\)", text) != None:
            freeindex.append(i)
            freeval.append(re.findall(".*free\s*\(\s*([0-9a-z]*)\s*\)", text)[0].strip())

    for i in range(len(freeindex)):
        for j in range(freeindex[i], len(content_list), 1):
            text = content_list[j]
            if re.search('\+\+\+\+\+.*memset[(]\s*'+ freeval[i] +'\s*,\s*0\s*,.*[)]', text):
                return 1
            elif re.search('\+\+\+\+\+\s*'+ freeval[i] +'\s*=\s*0', text):
                return 1
            elif re.search('\+\+\+\+\+\s*'+ freeval[i] +'\s*=\s*null', text):
                return 1

    return 0


def bound_check(content):
    new_content = ''.join(content)
    content_list = list(new_content.lower().split('\n'))

    ifindex = []
    for i in range(len(content_list)):
        # 找到if的判断语句 if(变量<><=>=整数)
        text = content_list[i]
        if re.search('\+\+\+\+\+\s*if\s*[(]\s*[a-zA-Z0-9_]+\s*[<>=]+\s*[a-zA-Z0-9_]*max[a-zA-Z0-9_]*\s*[)]', text) == None:
            if re.search('\+\+\+\+\+\s*if\s*[(]\s*[a-zA-Z0-9_]*max[a-zA-Z0-9_]*\s*[<>=]+\s*[a-zA-Z0-9_]+\s*[)]', text) == None:
                if re.search('\+\+\+\+\+\s*if\s*[(]\s*[a-zA-Z0-9_]*min[a-zA-Z0-9_]*\s*[<>=]+\s*[a-zA-Z0-9_]+\s*[)]', text) == None:
                    if re.search('\+\+\+\+\+\s*if\s*[(]\s*[a-zA-Z0-9_]+\s*[<>=]+\s*[a-zA-Z0-9_]*min[a-zA-Z0-9_]*\s*[)]', text) == None:
                        if re.search('\+\+\+\+\+\s*if\s*[(]\s*[a-zA-Z0-9_]+\s*[<>=]+\s*\d\s*[)]', text) == None:
                            if re.search('\+\+\+\+\+\s*if\s*[(]\s*\d\s*[<>=]+\s*[a-zA-Z0-9_]+\s*[)]', text) != None:
                                ifindex.append(i)
                        else:
                            ifindex.append(i)
                    else:
                        ifindex.append(i)
                else:
                    ifindex.append(i)
            else:
                ifindex.append(i)
        else:
            ifindex.append(i)


    for i in range(len(ifindex)):
        # 找到if判断为true后，是否有报错和返回
        kuohao = 0
        check = 0
        for j in range(i, len(content_list)):
            text = content_list[j]
            kuohao = kuohao + text.count('{') - text.count('}')
            if kuohao == 1:  # 在if{里或else{里
                returnflag = re.search('\+\+\+\+\+\s*return', text)
                if returnflag == None:
                    returnflag = re.search('\+\+\+\+\+\s*exit', text)

                if returnflag != None:  # 有返回，查找报错信息
                    check = check + 1
                    for k in (i, j, 1):
                        if re.search('err', content_list[k]) != None:
                            return 1
            if check == 2:
                break
    return 0

code_keywords = [] # keywords in patch diff
with open('code_keywords.txt','r',encoding='utf-8') as fkey:
    for line in fkey:
        code_keywords.append(line.strip())

def keywords_filter(txt):
    txt = re.sub('-----', "", txt)
    txt = re.sub('\+\+\+\+\+', "", txt)
    txt = porter_stemmer.stem(txt.lower())  # 小写、词干提取
    words = nltk.word_tokenize(txt)  # 分词
    words = list(set(words))
    for word in words:
        if word in code_keywords:
            return 1
    return 0


if __name__ == "__main__":

    target_path = 'data\\traindata\coderevision_new\evaluate\qemu2.csv'

    target_f = open(target_path, "r", encoding="utf-8")
    train_csv = csv.reader(target_f)

    label_list = []
    patch_list = []
    for line in train_csv:
        if line[0]=='label':
            continue
        label_list.append(line[0])
        patch_list.append(line[1])
    N = len(label_list)

    with open('result\qemu2_score.csv','w',encoding='utf-8',newline='') as f:
        csv_writer = csv.writer(f)
        csv_writer.writerow(['level','code revision'])
        for i in range(N):
            #if  label_list[i] == [0]: # only analysis security patches
            #    break
            data = patch_list[i] # each patch diff
            score = 0

            key_flag = keywords_filter(data)
            op_flag = permission_check(data) + initial_check(data) + pointer_check(data) + bound_check(data) + memory_leak_check(data) + locks_check(data)

            if key_flag:
                score = score + 1
            
            if op_flag == 1:
                score = score + 1
            elif op_flag >= 2:
                score = score + 2
            
            if score == 0:
                level = 'C'
            elif score == 1:
                level = 'B'
            elif score >= 2:
                level = 'A'
            
            if label_list[i] == '0':
                level = 'D'
            
            csv_writer.writerow([level,data])

    
