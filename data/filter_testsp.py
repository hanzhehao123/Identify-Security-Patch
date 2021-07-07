import csv

hashlist = []
with open('sp_hash.txt') as f:
    for line in f:
        hashlist.append(line.strip())

with open('testdata\\filtered\qemu3_cr.csv','r',encoding='utf-8') as f:
    train_csv = csv.reader(f)

    label_list = []
    patch_list = []
    for line in train_csv:
        if line[0]=='hash id':
            continue
        for word in hashlist:
            if line[2] == word:
                label_list.append(line[0])
                patch_list.append(line[1])

with open('testdata\\filtered\qemu3_sp.csv','w',encoding='utf-8',newline='') as f:
    csv_writer = csv.writer(f)
    csv_writer.writerow(['label','content'])
    for i in range(len(label_list)):
        csv_writer.writerow(['1',patch_list[i]])
