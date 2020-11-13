latex = '\\documentclass{standalone}\n\n\\usepackage{tikz}\n\\usetikzlibrary{shapes,arrows,positioning,shapes.geometric}\n\\usepackage{ifthen}\n\n\\setlength{\\textwidth}{40cm}\n\n\\begin{document}\n\\begin{tikzpicture}\n\n\\def\\hstep{.5pt}\n\\def\\vstep{.25pt}\n\n\\def\\pone{%s}\n\\def\\ptwo{%s}\n\\def\\site{%d}\n\\def\\X{%s}\n\\def\\minx{%f}\n\\def\\maxx{%f}\n\\def\\T{%s}\n\\def\\Tnorm{%s}\n\\def\\LAB{%s}\n\\def\\coloring{-1}\n\\def\\globalindex{%s}\n\\def\\globalindiceson{-1}\n\\def\\regrafttime{%f}\n\\def\\regrafttimenorm{%f}\n\\def\\recombinationtime{%f}\n\\def\\recombinationtimenorm{%f}\n\\def\\NL{%d}\n\\def\\NN{%d}\n\\def\\prune{%d}\n\\def\\regraft{%d}\n\n\\def\\prpar{-1}\n\\def\\rgpar{-1}\n\n\\def\\newnode{-1}\n\n\\input{./phytree.tex}\n\n\\end{tikzpicture}\n\\end{document}\n'
#%%
def SMARTree_read_rawinput(filename): #The file should only contain the local trees in the final iteration
    # This function does not work with SMARTree_MCMCState file!
    f = open(filename)
    inp = f.read()
    f.close()
    delimeter = "CoalescentTree"
    inp = inp.split(delimeter)
    for i in range(1,len(inp)):   
        itembefore = inp[i-1]
        start = ''
        j = -1
        while itembefore[j] !=  '{':
            start = itembefore[j] + start
            j -= 1
        start = '{' + start + delimeter
        inp[i] = start + inp[i]
        inp[i-1] = itembefore[:(j-2)]
    return inp[1:] #Returns list of local trees - trees are in String format
#%%
trees = SMARTree_read_rawinput("SMARTree_FinalLocalTrees.txt")
#%%
class localtree: # An object that stores the local tree and its information
    
    def __init__(self, site, times, nodes):
        self.site = site
        self.times = times
        self.nodes = nodes
        self.recomb_exists = False
        count = 0
        for time in times:
            if time == 0:
                count += 1
        self.nseq = count
        self.spot = len(times)
        from math import sqrt
        # Think about this scaling? 
        self.scaled_time = [sqrt(i)*10 for i in self.times]
    
    def add_recomb(self,start,end,rectime,losttime):
        self.recomb_exists = True
        self.recomb_from = start
        self.recomb_to = end
        self.recomb_time = rectime
        self.lost_time = losttime
        
    def printinfo(self):
        print("Site: " + str(self.site))
        print("Times: " + str(self.times))
        print("Nodes: " + str(self.nodes))
        if self.recomb_exists:
            print("Recombination from %s to %s at time %s" % (self.recomb_from,self.recomb_to,self.recomb_time))
        else:
            print("No recombination")
    
    def getlatex(self):
        d = {i:-1 for i in range(self.spot)}
        currentmax = 0
        distance_between_bottom_two = 2
        nodes = self.nodes
        #Recheck the method, needs update, check site 8685-8816
        for node in nodes:
            if node == nodes[-1]:
                if d[node[0]] == -1:
                    d[node[0]] = currentmax
                    currentmax += distance_between_bottom_two
                d[node[2]] = (d[node[0]] + d[node[1]])/2
            if d[node[0]] == -1:
                if d[node[1]] == -1: #Additional checking for better visualization
                    d[node[0]] = currentmax
                    currentmax += distance_between_bottom_two
                else: #This is a naive solution - update this in future
                    d[node[0]] = d[node[1]] + 1.6                
            if d[node[1]] == -1:
                d[node[1]] = currentmax
                currentmax += distance_between_bottom_two
            d[node[2]] = (d[node[0]] + d[node[1]])/2
        xlist = list(d.values())
        pone =  '{' + str([tup[0] for tup in nodes])[1:-1] + '}'
        ptwo = '{' + str([tup[1] for tup in nodes])[1:-1] + '}'
        x = '{' + str(xlist)[1:-1] + '}'
        T = '{' + str(self.times)[1:-1] + '}'
        Tnorm = '{' + str(self.scaled_time)[1:-1] + '}'
        LAB = '{' + str(list(range(self.spot)))[1:-1] + '}'
        globalindex = '{' + str(list(range(self.spot-self.nseq)))[1:-1] + '}'
        rec_to_time = -1
        rec_to_time_norm = -1
        rec_from_time = -1
        rec_from_time_norm = -1
        rec_from = -1
        rec_to = -1
        if self.recomb_exists:
            rec_to_time = self.recomb_time
            from math import sqrt
            rec_to_time_norm = sqrt(rec_to_time)*10
            rec_from_time = self.lost_time
            rec_from_time_norm = sqrt(rec_from_time)*10
            rec_from = self.recomb_from
            rec_to = self.recomb_to
        out = latex % (pone,ptwo,self.site,x,min(xlist),max(xlist),T,Tnorm,LAB,globalindex, \
                       rec_to_time, rec_to_time_norm, rec_from_time, rec_from_time_norm, \
                       self.nseq,self.spot,rec_from, rec_to)
        #Update needed - Create a directory called trees 
        f = open("trees/Tree_Site%d_Rec%s.tex" % (self.site,self.recomb_exists), "w")
        f.write(out)
        f.close()
    
    def issame(self,tr):
        if self.nodes == tr.nodes:
            return True
        return False
        
#%%
def SMARTree_read_individual(t): #Reads a string of one Local Tree: returns localtree object
    lst = t.split("\n")
    for i in range(len(lst)):
        j = 0
        while lst[i][j] == ' ':
            j += 1
        lst[i] = lst[i][j:]
    t = ''.join(lst)
    site = ""
    i = 1
    while t[i] != ',':
        site += t[i]
        i += 1
    site = int(site)  
    t = t.split('[')[1].split(']')[0]
    times = ''
    i = 1
    while t[i] != '}':
        times += t[i]
        i += 1
    times = [ float(item) for item in times.split(', ')]
    nodes = t[(i+4):].split('{{')[1:]
    nodes2 = []
    for item in nodes:
        nodes2.append(item.split("}, {"))
    nodes3 = []
    for item in nodes2:
        first = ''
        i = 0
        while item[0][i] != ',':
            first += item[0][i]
            i += 1
        dest = ''
        i = -1
        while item[0][i] != ' ':
            dest = item[0][i] + dest
            i -= 1
        second = ''
        i = 0
        while item[1][i] != ',':
            second += item[1][i]
            i += 1
        if int(first) < int(second): #Making sure the consistency in the topology
            nodes3.append((int(first)-1,int(second)-1,int(dest)-1))
        else:
            nodes3.append((int(second)-1,int(first)-1,int(dest)-1))
    return localtree(site,times,nodes3) 

#%%
def get_all_trees(trees): #Returns a list of localtree object
    lst = []
    for t in trees:
        lst.append(SMARTree_read_individual(t))
    #Adding recombinations - some minor issues, check site 640-657, check site 1118-1164
    for i in range(len(lst)-1):
        if not lst[i].issame(lst[i+1]):
            lost_time = (set(lst[i].times) - set(lst[i+1].times)).pop()
            lost_index = lst[i].times.index(lost_time)
            
            for item in lst[i].nodes: #Find the lost node, and find the one it connects
                if lost_index == item[2]:
                    temp = (item[0],item[1])
                elif lost_index in item:
                    pretime = lst[i].times[item[2]]  
            
            pre = lst[i+1].times.index(pretime)
            
            for item in lst[i+1].nodes: #Find the start point of recombination
                if pre == item[2]:
                    if temp[0] in item:
                        start = temp[1]
                    else:
                        start = temp[0]
            
            for item in lst[i+1].nodes: #Find the end point of recombination
                if start in item and start != item[2]:
                    if item[0] == start:
                        end = item[1]
                    else:
                        end = item[0]
                    index = item[2] #To find the recombination time
            
            rectime = lst[i+1].times[index]
            lst[i].add_recomb(start,end,rectime,lost_time/2) 
    return lst
#%%
def get_trees_with_recomb(trees): #Returns a list localtree object that has unique topology
    lst = []
    for t in trees:
        if t.recomb_exists:
            lst.append(t)
    return lst
#%%
def get_trees_with_recomb_and_after_recomb(trees): #Returns a list localtree object that has unique topology
    lst = []
    for i in range(len(trees)):
        if trees[i].recomb_exists:
            lst.append(trees[i])
            from copy import deepcopy 
            nxt = deepcopy(trees[i+1])
            nxt.recomb_exists = False
            lst.append(nxt)
    return lst
#%%
lst = get_all_trees(trees)

#%%
recombs = get_trees_with_recomb_and_after_recomb(lst)
#%%
for t in recombs:
    t.getlatex()
    t.printinfo()  
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

#%%

#%%

   