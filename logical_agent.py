import sys
import getopt
import copy

fo = open("output.txt","w+")
class KB:
    imply = {}
    clause = {}
    last_goal = ""
    def __init__(self):
        pass
    def add(self,query):
        if '=>' in query:
            lbs = query.split('=>')[0]
            rbs = query.split('=>')[1]
            element = []
            args = []
            predicate = self.dearg(rbs, args)
            element.append(args)
            leftelem = lbs.split('&&')
            leftres = []
            for item in leftelem:
                item = item.replace(" ", "")
                arg = []
                predic = self.dearg(item,arg)
                elem = []
                elem.append(predic)
                elem.append(arg)
                leftres.append(elem)
            element.append(leftres) 
            if predicate not in self.imply:
                self.imply[predicate] = []
            self.imply[predicate].append(element)
        else:
            args = []
            predicate = self.dearg(query, args)
            if predicate not in self.clause:
                self.clause[predicate] = [];
            self.clause[predicate].append(args);
    def dearg(self,query,args):
        predicate = query.split('(')[0]
        rest = query.split('(')[1].split(')')[0]
        args_val = rest.split(',')
        for item in args_val:
            item = item.replace(" ", "")
            args.append(item)
        return predicate.replace(" ", "")
    def bc_ask(self, goal, sub):
        args = []
        predicate = self.dearg(goal,args) 
        rules = self.imply.get(predicate)
        if rules is not None:
            for rul_item in rules: #OR
                subsub = {}
                pre_args  = rul_item[0]
                rul_lps = rul_item[1]
                for i,rarg in enumerate(pre_args):
                    if rarg.islower() is True and args[i].islower() is False: 
                        subsub[rarg] = args[i]
                newlast_goal = predicate+'(' 
                for i, pre_val in enumerate(pre_args):
                    newlast_goal = newlast_goal+args[i]
                    newlast_goal = newlast_goal + ','
                newlast_goal = newlast_goal[0:-1]+')'
                fo.writelines("Ask: " + self.reform(newlast_goal)+"\n")
                pos_sub = []
                pos_sub.append(subsub)
                and_flag = False 
                lastandpred = None
                lastandargs = None
                for rule in rul_lps: #AND
                    last_query = copy.deepcopy(self.last_goal) 
                    and_flag = False
                    new_pos_sub = []
                    rule_pred = rule[0] 
                    rule_args = rule[1]
                    for i, subs in enumerate(pos_sub):
                        traces = subs.get('trace') #Note the None
                        if traces is not None:
                            for query in traces:
                                reformed_query = self.reform(query)
                                if "_" in reformed_query:
                                    fo.writelines("Ask: "+reformed_query+"\n")
                                else:
                                    fo.writelines("True: " + reformed_query+"\n")
                        newgoal = rule_pred+'('
                        rule_args_sub = []
                        for rule_val in rule_args: #substituet args
                            newval = subs.get(rule_val)
                            if newval is not None:
                                newgoal = newgoal+newval
                                rule_args_sub.append(newval)
                            else: #if the args hasn't assigned yet
                                newgoal = newgoal + rule_val
                                rule_args_sub.append(rule_val)
                            newgoal = newgoal + ','
                        newgoal = newgoal[0:-1]+')'
                        retsub = [] 
                        fo.writelines("what's the goal " + newgoal)
                        if self.bc_ask(newgoal, retsub) is True:
                            fo.writelines("return to "+ rule_pred+"\n")
                            for i, rows in enumerate(retsub):
                                fo.writelines(str(rows)+"\n")
                                retrace = rows.pop()
                                newsub = copy.deepcopy(subs)
                                for i, item in enumerate(rows):
                                    if rule_args_sub[i].islower() is False:
                                        if rule_args_sub[i]==item is True:
                                            break
                                    else:
                                        if newsub.get(rule_args_sub[i]) is None:
                                            newsub[rule_args_sub[i]] = item
                                newsub['trace'] = copy.deepcopy(retrace)
                                new_pos_sub.append(newsub)
                            and_flag = True
                    pos_sub = copy.deepcopy(new_pos_sub)
                    lastandpred = rule_pred
                    lastandargs = copy.deepcopy(rule_args)
                if and_flag is True:
                    #count = 0
                    for subs in pos_sub: 
                        trace = subs.get('trace')
                        subtmp = []
                        for item in pre_args:
                            if item.islower() is True:
                                subtmp.append(subs.get(item))
                            else:
                                subtmp.append(item)
                        if trace is not None:
                            newgoal = predicate+'('
                            for item in subtmp:
                                newgoal = newgoal+item+','
                            newgoal = newgoal[0:-1]+')'
                            #if count > 0:
                                #trace.append(goal)
                            trace.append(newgoal)
                        subtmp.append(trace)
                        sub.append(subtmp)
                        #count = count + 1 
                    return True
                else:
                   continue #continue to try another or clause 
        fact = self.clause.get(predicate)
        if fact is not None:
            fo.writelines("Ask: " + self.reform(goal) +"\n")
            count = 0
            for i, facttmp in enumerate(fact):
                subtmp = []
                fact_flag = True
                for i, item in enumerate(args):
                    if item.islower() is True:
                        subtmp.append(facttmp[i]) 
                    else:
                        if item!=facttmp[i]:
                            fact_flag = False
                            break;
                        subtmp.append(args[i])
                if fact_flag is True: 
                    goaltmp = []
                    newgoal = predicate+'('
                    for item in subtmp:
                        newgoal = newgoal+item+','
                    newgoal = newgoal[0:-1]+')'
                    if count>0:
                        goaltmp.append(goal)
                    goaltmp.append(newgoal)
                    subtmp.append(goaltmp)
                    sub.append(subtmp)
                    count = count+1
            if len(sub) > 0:
                self.last_goal = copy.deepcopy(goal)
                return True
            else:
                fo.writelines("False: "+self.reform(goal)+"\n")
                return False
        else:
            fo.writelines("False: "+self.reform(goal)+"\n")
            return False
        fo.writelines("False: "+self.reform(goal)+"\n")
        return False

    def bc_query(self, query):
        queries = query.split('&&')  
        traces= None
        ret = []
        for item in queries:
            if len(ret)>0 and len(ret[0])>0:
                trace = ret[0].pop() #the trace should be check!!!!!!
                for query in trace:
                    reformed_query = self.reform(query)
                    if "_" in reformed_query:
                        fo.writelines("Ask: "+reformed_query+"\n")
                    else:
                        fo.writelines("True: " + reformed_query+"\n")
            ret = []
            item = item.replace(" ", "")
            if self.bc_ask(item, ret) is False:
                return False
        if len(ret)>0 and len(ret[0])>0:
            trace = ret[0].pop() #the trace should be CHECK!!!!!
            for query in trace:
                reformed_query = self.reform(query)
                if "_" in reformed_query:
                    fo.writelines("Ask: " + reformed_query+"\n")
                else:
                    fo.writelines("True: " + reformed_query+"\n")
        return True
    def reform(self, query):
        args = []
        predicate = self.dearg(query, args)
        goal = predicate+'('
        for item in args:
            if item.islower() is True:
                goal  = goal + '_'
            else:
                goal = goal+item
            goal  = goal + ', '
        goal = goal[0:-2]+')'
        return goal
def main(argv):
    kb = KB()
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
    for i, line in enumerate(fp):
        if i==0:
            goal = line.split("\n")[0]
        elif i==1:
            KB_number = int(line)
        elif i>=2:
            clause = line.split("\n")[0]
            kb.add(clause)
    if kb.bc_query(goal) is True:
        fo.writelines("True"+"\n")
    else:
        fo.writelines("False"+"\n")

main(sys.argv[1:])
