import csv
import re

def filter_code(src):
    src = re.sub(r'@@ -[0-9]+,[0-9]+ \+[0-9]+,[0-9]+ @@', "", src)
    src = re.sub(r'index [a-z0-9]+..[a-z0-9]+ [0-9]+\n', "", src)
    src = re.sub(r'[\n]+', '\n', src)
    while(True):
        if re.search(r'\n-[^-]+', src)==None:
            break
        (begin, end) = re.search(r'\n-[^-]+', src).span()
        end = begin+2
        if src[end]!='-':
            src = src[0:end] + '----' + src[end:]
        if len(re.findall(r'\n-', src)) == len(re.findall(r'\n--', src)):
            break

    while(True):
        if re.search(r'\n\+[^+]+', src)==None:
            break
        (begin, end) = re.search(r'\n\+[^+]+', src).span()
        end = begin+2
        if src[end]!='+':
            src = src[0:end] + '++++' + src[end:]
        if len(re.findall(r'\n\+', src)) == len(re.findall(r'\n\+\+', src)):
            break
    return src
    # print(src)

    # lexer = CppLexer()
    # tokens = lexer.get_tokens(src)
    # ret = ""
    # for token_tuple in tokens:
    #     print(token_tuple)




train_f = open("..\data\\traindata\coderevision\\train\\qemu2.csv", "r", encoding="utf-8")
evaluate_f = open("..\data\\traindata\coderevision\\evaluate\\qemu2.csv", "r", encoding="utf-8")

train_csv = csv.reader(train_f)
evaluate_csv = csv.reader(evaluate_f)
csvlist=[train_csv, evaluate_csv]

dst_train_f = open("..\data\\traindata\coderevision_new\\train\\qemu2.csv", "w", encoding='utf-8', newline='')
dst_evaluate_f = open("..\data\\traindata\coderevision_new\\evaluate\\qemu2.csv", "w", encoding='utf-8', newline='')
dst_train_csv = csv.writer(dst_train_f)
dst_evaluate_csv = csv.writer(dst_evaluate_f)
dst_csvlist = [dst_train_csv, dst_evaluate_csv]



for i in range(len(csvlist)):
    input_rows = []
    for line in csvlist[i]:
        input_rows.append(line)

    for line, row in enumerate(input_rows):
        if line==0:
            dst_csvlist[i].writerow([row[0], row[1]])
        else:
            if len(row)!=2:
                continue
            tmp = filter_code(row[1])
            dst_csvlist[i].writerow([row[0], tmp])


