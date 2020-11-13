import sys 

n = len(sys.argv) 
print(sys.argv)
#Checker

#%%

f = open("try.sites",'r')

l1 = f.readline()
l2 = f.readline()

sites = []
seqs = []
for x in f:
    temp = x.split("\t")
    sites.append(temp[0])
    d = {}
    for ch in temp[1][:-1]:
        if ch in d.keys():
            d[ch] += 1
        else:
            d[ch] = 1
    mx = max(d.values())
    mnuc = ''
    for x in d.keys():
        if d[x] == mx:
            mnuc = x
            break
    seq = ''
    for ch in temp[1][:-1]:
        if ch == mnuc:
            seq += '0'
        else:
            seq += '1'
    seqs.append(seq)
f.close()
#%%
lines = ['' for i in range(len(seqs[0]))]
for seq in seqs:
    for i in range(len(seqs[0])):
        lines[i] = lines[i] + seq[i] + ' '
lines = [line[:-1]+'\n' for line in lines]    
#%%
f = open("try1.txt",'w')
f.write(' '.join(sites) + '\n')
for line in lines:
    f.write(line)
f.close()
