# Connection String
connectionString = {
    'links': "links.srt"
}
lamda = 0.20
tau = 0.005

# return Graph
def initGraph():
    # Map<String, Set<String>>
    ans = {}
    f = open(connectionString['links'], "r", encoding='utf-8')
    line = f.readline()
    while line:
        # arr[0]: source
        # arr[1]: destination
        arr = line.split('\t')
        arr[1] = arr[1][0:len(arr[1])-1]    # Remove '\n'
        if (ans.get(arr[0])): ans[arr[0]].add(arr[1])
        else: ans[arr[0]] = { arr[1] }
        
        if (not ans.get(arr[1])): ans[arr[1]] = set()
        
        line = f.readline()
        
    f.close()
    return ans

def inlinks(g):
    # Dict<String, Number>>
    dict = {}
    for ele in g:
        for l in g[ele]:
            if dict.get(l): dict[l] += 1
            else : dict[l] = 1
    
    ans = {k: v for k, v in sorted(dict.items(), key=lambda item: item[1], reverse=True)}
    
    # Take first 100 most inlink count
    f = open("inlinks.txt", "w")
    index = 0
    for i in ans:
        index += 1
        f.write(i + ' ' + str(index) + ' ' + str(ans[i]) + '\n')
        
        if index == 100: break
    f.close()

def rank100(r): 
    # List<Dict<String, Number>>
    ans = []
    for ele in r:
        ans.append({ 'url': ele, 'rank': r[ele] })
    
    ans = sorted(ans, key=lambda d: d['rank'], reverse=True) 
    
    # Take first 100 most inlink count
    f = open("pagerank.txt", "w")
    for i in range(0, 100):
        if (ans[i]):
            f.write(ans[i]['url'] + ' ' + str(i + 1) + ' ' + str(ans[i]['rank']) + '\n')
    f.close()
    
def pageRank(g):
    I, R = {}, {}
    # Start with each page being equally likely
    for i in g:
        I[i] = 1 / len(g)    
    converge = False
    while not converge:
        print('Not Converge')
        # Each page has a lamda/|P| change of random selection
        for i in g:
            R[i] = lamda / len(g)
        
        accumulator = 0
        for p in g:
            Q = g[p]
            if len(Q) > 0:
                # probability Ip of being at page p
                pr = (1 - lamda) * I[p] / len(Q)
                for q in Q:
                    R[q] += pr
            
            else:
                accumulator += (1 - lamda) * I[p] / len(g)
        
        # Rank-sink
        for q in g:
            R[q] += accumulator
            
        # Convergence test
        L1 = 0
        for ele in g:
            L1 += abs(I[ele] - R[ele])
        if L1 < tau: converge = True
        
        for i in I:
            I[i] = R[i]

    rank100(R)
    return R
        
g = initGraph()
inlinks(g)
pageRank(g)
