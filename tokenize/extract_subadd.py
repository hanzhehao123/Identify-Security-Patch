import csv
import re

def filter_code(src):
    tmp = re.findall(r'\+\+\+\+\+.*\n|-----.*\n', src)
    ret = ""
    for i in tmp:
        ret = ret+i
    return ret

train_f = open("..\data\\traindata\coderevision_new\\train\\qemu2.csv", "r", encoding="utf-8")
evaluate_f = open("..\data\\traindata\coderevision_new\\evaluate\\qemu2.csv", "r", encoding="utf-8")
train_csv = csv.reader(train_f)
evaluate_csv = csv.reader(evaluate_f)
csvlist=[train_csv, evaluate_csv]

dst_train_f = open("..\data\\traindata\coderevision_new\\train\\qemu2_addsub.csv", "w", encoding='utf-8', newline='')
dst_evaluate_f = open("..\data\\traindata\coderevision_new\\evaluate\\qemu2_addsub.csv", "w", encoding='utf-8', newline='')
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
