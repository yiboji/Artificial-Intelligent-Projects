import sys
import getopt
import copy

class Query:

    types = None
    query = {}
    evid = {}

    def __init__(self, types, query, evid):
        self.types = types
        self.query = query
        self.evid = evid

class Distribute:

    def __init__(self, queryname):
        self.var = queryname
        self.prob = {}
    def __setitem__(self,val,probval):
        self.prob[val] = probval
    def __getitem__(self, val):
        return self.prob[val]

class BNet:

    def __init__(self, node=[]):
        self.nodes=[]
        self.variable=[]
        for item in node:
            self.varialbe.append(item[0])

def enumerate_ask(X,e,bn_vars):
    #X is the 'Demoalize'
    #e is the {'L':True, 'I':True}
    #bn_vars is ['D','L','I','N'] with parents
    Q = Distribute(X)
    for xi in [True, False]:
        exte = copy.deepcopy(e)
        exte[X] = xi
        Q[xi] = enumerate_all(bn_vars,exte)
    normalize(Q)
    print "result of enumerate "+X+" T:"+str(Q[True])+" F:"+str(Q[False])

def enumerate_all(bn_vars, e):
    if not bn_vars:
        return 1.0
    Y, res = bn_vars[0], bn_vars[1:]
    if Y[0] in e:
        result = get_p(Y,e[Y[0]],e)*enumerate_all(res,e)
        print res
        return result
    else:
        result = 0
        for val in [True,False]:
            exte = copy.deepcopy(e)
            exte[Y[0]] = val
            result  = result + get_p(Y,val,e)*enumerate_all(res,exte)
        print res
        return result 

def get_p(Y,val,e):
    key = ()
    table = {}
    for i, item in enumerate(Y):
        if i>0 and i<len(Y)-1:
            if len(item)==0:
                break
            key = key+(e[item],)
        elif i==len(Y)-1:
            table = item
            if len(key)==1:
                key = key[0]
            if val==True:
                print "key"
                print key
                return float(table[key])
            else:
                return 1-float(table[key])
    if val==True:
        return float(Y[-1]) 
    else:
        return 1-float(Y[-1])

def normalize(Q):
    total = Q[True]+Q[False]
    Q[True] = Q[True]/total
    Q[False] = Q[False]/total

def main_logic(argv):
    try:
        opts,args = getopt.getopt(argv,"i:")
    except getopt.GetoptError:
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-i"):
            filename = arg
        else:
            sys.exit(2)
    fp = open(filename)
    cnt=0
    queries = []
    network = []
    node = []
    posilist = {}
    for i, line in enumerate(fp):
        line  = line.split("\n")[0] 
        if line=="******":
            cnt += 1
            continue
        if cnt==0:
            line = line.replace(' ','')
            typetmp = None
            querytmp = {}
            evidtmp = {}
            #query lines
            print line
            if line[0]=='P':
                typetmp = 'P'
                line = line[2:-1]
            elif line[0]=='E':
                typetmp = 'EU'
                line = line[3:-1]
            elif line[0]=='M':
                typetmp = 'MEU'
                line = line[4:-1]
            line = line.split('|')
            queryline = line[0].split(',') 
            for item in queryline:
                item = item.split('=')
                querytmp[item[0]] = (item[1]=='+' if True else False)

            if len(line)>1:
                evidline = line[1].split(',')
                for item in evidline:
                    item = item.split('=')
                    evidtmp[item[0]] = (item[1]=='+' if True else False)
            queries.append(Query(typetmp, querytmp, evidtmp))
        elif cnt>=1:
            #Bayesian network
            if line=='***':
                if posilist:
                    node.append(posilist)
                network.append(node)
                node = []
                posilist = {}
                continue
            print line
            if len(node)==0: 
                line = line.split('|')
                nodeline = line[0].split(' ')
                for item in nodeline:
                    if len(item)!=0:
                        node.append(item)
                if len(line)>1:
                    condline = line[1].split(' ')
                    for item in condline:
                        if len(item)!=0:
                            node.append(item)
                else:
                    node.append('')
            elif len(node[1])==0:
                node.append(line)
            else:
                line = line.split(' ')
                keys = ()
                if len(line)<3:
                    posilist[(line[1]=='+' if True else False)]=line[0]
                else:
                    for i, item in enumerate(line):
                        if i is len(line)-1:
                            keys = keys + ((item=='+' if True else False),)
                        elif i>0 and i<len(line)-1:
                            keys = keys + ((item=='+' if True else False),)
                    posilist[keys] = line[0]
    if len(node)!=0:
        if posilist:
            node.append(posilist)
        network.append(node)
    netvars=[]
    for item in network:
        netvars.append(item[0])
    print "netvars:"
    print netvars

    print str(network)
    print "queries:"
    for q in queries:
        print q.types
        print q.query
        print q.evid
        for key in q.query:
            print "final result"
            print key
            print enumerate_ask(key,q.evid,network)

if __name__=='__main__':
    main_logic(sys.argv[1:])


















