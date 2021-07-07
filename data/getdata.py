from git import Repo

content = []

with open('hash.txt') as f:
    for line in f:
        content.append(line.strip())

for i in range(10):
    print(content[i])

repo = Repo('qemu')
git = repo.git

for i in range(1000):
    result1 = git.log(content[i],'-1')
    result2 = git.diff(content[i],content[i+1])
    with open('testdata\commitmessage\\'+content[i]+'.txt','w',encoding='utf-8') as f:
        f.write(result1)
    with open('testdata\coderevision\\'+content[i]+'.txt','w',encoding='utf-8') as f:
        f.write(result2)  
