#%%
f = open("arb_data.txt")
#%%
inp = f.read()
#%%
f.close()
#%%
inp2 = inp[:-1].split("\n")
#%%
n = len(inp2)-1
#%%
inp3 = [i.split(' ') for i in inp2]
#%%
seqlen = inp3[0][-1]
#%%
power = len(seqlen)
#%%
from math import ceil
#%%
seqlen = ceil(int(seqlen)/(10**(power-1))) * 10**(power-1)
#%%
output = ["{%d, %d}" % (seqlen,n)]
#%%
for i in range(len(inp3[0])):
    col = '{' + inp3[0][i] + ", {"
    for j in range(n):
        col += inp3[j+1][i] + ", "
    col = col[:-2] + "}, {0.5, 0.5}}"
    output.append(col)
#%%
txt = "\n".join(output)
#%%
f = open("try.txt", "w")
f.write(txt)
f.close()
#%%

#%%

#%%

#%%

#%%
#%%

#%%

#%%

#%%

#%%

#%%