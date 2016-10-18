import sys
import getopt
import copy

valboard = None

def best_first(staboard,cutoff,player,enemy):
    sumval = 0
    for i, rows in enumerate(staboard):
        for j, item in enumerate(rows):
            if staboard[i][j] is player:
                sumval += valboard[i][j]
            elif staboard[i][j] is enemy:
                sumval -= valboard[i][j]

    maxVal = float("-inf")
    nextCoord = []
    for i, rows in enumerate(staboard):
        for j, item in enumerate(rows):
            currval = sumval + valboard[i][j]
            neighbor = [None for x in range(4)]
            if item is "*":
                if i>0:
                    neighbor[0] = []
                    neighbor[0].append(staboard[i-1][j])
                    neighbor[0].append([i-1,j])
                if i<4:
                    neighbor[2] = []
                    neighbor[2].append(staboard[i+1][j])
                    neighbor[2].append([i+1,j])
                if j>0:
                    neighbor[3] = []
                    neighbor[3].append(staboard[i][j-1])
                    neighbor[3].append([i,j-1])
                if j<4:
                    neighbor[1] = []
                    neighbor[1].append(staboard[i][j+1])
                    neighbor[1].append([i,j+1])
                enemycoord = []
                for item in neighbor:
                    if item is not None and item[0] is player:
                        for itemene in neighbor:
                            if itemene is not None and itemene[0] is enemy:
                                row = itemene[1][0]
                                col = itemene[1][1]
                                currval += 2*valboard[row][col]
                                enemycoord.append(itemene[1])
                        break
                if currval>maxVal:
                    maxVal = currval
                    nextCoord = []
                    nextCoord.append([i,j])
                    nextCoord.append(enemycoord)
    coor = nextCoord[0]
    staboard[coor[0]][coor[1]] = player
    for coor in nextCoord[1]:
            staboard[coor[0]][coor[1]] = player

def minimax(staboard, cutoff,player,enemy):
    maxcut = cutoff
    best = float('-inf')
    move = None
    fo = open("traverse_log.txt","w+")
    fo.writelines("Node,Depth,Value\n")
    for i, rows in enumerate(staboard):
        for j, item in enumerate(rows):
            neighbor = [None for x in range(4)]
            if item is not None: 
                if i>0:
                    neighbor[0] = []
                    neighbor[0].append(staboard[i-1][j])
                    neighbor[0].append([i-1,j])
                if i<4:
                    neighbor[2] = []
                    neighbor[2].append(staboard[i+1][j])
                    neighbor[2].append([i+1,j])
                if j>0:
                    neighbor[3] = []
                    neighbor[3].append(staboard[i][j-1])
                    neighbor[3].append([i,j-1])
                if j<4:
                    neighbor[1] = []
                    neighbor[1].append(staboard[i][j+1])
                    neighbor[1].append([i,j+1])
                enemycoord = []
                for item in neighbor:
                    if item is not None and item[0] is player:
                        for itemene in neighbor:
                            if itemene is not None and itemene[0] is enemy:
                                row = itemene[1][0]
                                col = itemene[1][1]
                                enemycoord.append(itemene[1])
                        break
                newboard = copy.deepcopy(staboard)
                newboard[i][j] = player
                for coor in enemycoord:
                    newboard[coor[0]][coor[1]] = player
                if best == float('-inf'):
                    fo.writelines("root,0,"+"-Infinity\n")
                else:
                    fo.writelines("root,0,"+str(best)+"\n")
                val = min(enemy, copy.deepcopy(newboard),cutoff-1,maxcut,[i,j],fo)
                #print str(newboard)
                if val > best:
                    best = val
                    move = newboard 
    for i, rows in enumerate(staboard):
        for j,item in enumerate(rows):
            staboard[i][j] = move[i][j]
    fo.writelines("root,0,"+str(best)+"\n")

def minimax_alpha_beta(staboard, cutoff,player,enemy):
    maxcut = cutoff
    best = float('-inf')
    move = None
    fo = open("traverse_log.txt","w+")
    fo.writelines("Node,Depth,Value,Alpha,Beta\n")
    alpha = float('-inf')
    beta = float('inf')
    for i, rows in enumerate(staboard):
        for j, item in enumerate(rows):
            neighbor = [None for x in range(4)]
            if item is not None: 
                if i>0:
                    neighbor[0] = []
                    neighbor[0].append(staboard[i-1][j])
                    neighbor[0].append([i-1,j])
                if i<4:
                    neighbor[2] = []
                    neighbor[2].append(staboard[i+1][j])
                    neighbor[2].append([i+1,j])
                if j>0:
                    neighbor[3] = []
                    neighbor[3].append(staboard[i][j-1])
                    neighbor[3].append([i,j-1])
                if j<4:
                    neighbor[1] = []
                    neighbor[1].append(staboard[i][j+1])
                    neighbor[1].append([i,j+1])
                enemycoord = []
                for item in neighbor:
                    if item is not None and item[0] is player:
                        for itemene in neighbor:
                            if itemene is not None and itemene[0] is enemy:
                                row = itemene[1][0]
                                col = itemene[1][1]
                                enemycoord.append(itemene[1])
                        break
                newboard = copy.deepcopy(staboard)
                newboard[i][j] = player
                for coor in enemycoord:
                    newboard[coor[0]][coor[1]] = player
                if best == float('-inf'):
                    if alpha == float('-inf') and beta == float('inf'):
                        combin = "-Infinity,Infinity"
                    elif alpha==float('-inf'):
                        combin = "-Infinity,"+str(beta)
                    elif beta==float('inf'):
                        combin = str(alpha)+",Infinity"
                    else:
                        combin = str(alpha)+","+str(beta)

                    fo.writelines("root,0,"+"-Infinity,"+combin+"\n")
                else:
                    if alpha == float('-inf') and beta == float('inf'):
                        combin = "-Infinity,Infinity"
                    elif alpha==float('-inf'):
                        combin = "-Infinity,"+str(beta)
                    elif beta==float('inf'):
                        combin = str(alpha)+",Infinity"
                    else:
                        combin = str(alpha)+","+str(beta)
                    fo.writelines("root,0,"+str(best)+","+combin+"\n")
                val = min_beta(enemy, copy.deepcopy(newboard),cutoff-1,maxcut,[i,j],fo,alpha,beta)
                if val > best:
                    best = val
                    move = newboard 
                    alpha = best
    for i, rows in enumerate(staboard):
        for j,item in enumerate(rows):
            staboard[i][j] = move[i][j]
    fo.writelines("root,0,"+str(best)+","+str(alpha)+",Infinity"+"\n")

def min(player, staboard, cutoff,maxcut,node,fo):
    minval = float("inf")
    if player == "X":
        enemy = "O"
    else:
        enemy = "X"

    if cutoff is 0:
        sumval = 0
        for i, rows in enumerate(staboard):
            for j, item in enumerate(rows):
                if staboard[i][j] is player:
                    sumval += valboard[i][j]
                elif staboard[i][j] is enemy:
                        sumval -= valboard[i][j]
        sumval *= -1
        fo.writelines(chr(node[1]+ord('A'))+str(node[0]+1)+","+str(maxcut-cutoff)+","+str(sumval)+"\n")
        return sumval
    for i, rows in enumerate(staboard):
        for j, item in enumerate(rows):
            neighbor = [None for x in range(4)]
            if item is "*":
                if i>0:
                    neighbor[0] = []
                    neighbor[0].append(staboard[i-1][j])
                    neighbor[0].append([i-1,j])
                if i<4:
                    neighbor[2] = []
                    neighbor[2].append(staboard[i+1][j])
                    neighbor[2].append([i+1,j])
                if j>0:
                    neighbor[3] = []
                    neighbor[3].append(staboard[i][j-1])
                    neighbor[3].append([i,j-1])
                if j<4:
                    neighbor[1] = []
                    neighbor[1].append(staboard[i][j+1])
                    neighbor[1].append([i,j+1])
                enemycoord = []
                for item in neighbor:
                    if item is not None and item[0] is player:
                        for itemene in neighbor:
                            if itemene is not None and itemene[0] is enemy:
                                row = itemene[1][0]
                                col = itemene[1][1]
                                enemycoord.append(itemene[1])
                        break
                newboard = copy.deepcopy(staboard)
                newboard[i][j] = player
                for coor in enemycoord:
                    newboard[coor[0]][coor[1]] = player
                if minval == float('inf'):
                    fo.writelines(chr(node[1]+ord('A'))+str(node[0]+1)+","+str(maxcut-cutoff)+","+"Infinity"+"\n")
                else:
                    fo.writelines(chr(node[1]+ord('A'))+str(node[0]+1)+","+str(maxcut-cutoff)+","+str(minval)+"\n")
                val = max(enemy, newboard,cutoff-1,maxcut,[i,j],fo)
                if val < minval:
                    minval = val
    fo.writelines(chr(node[1]+ord('A'))+str(node[0]+1)+","+str(maxcut-cutoff)+","+str(minval)+"\n")
    return minval 

def max(player, staboard, cutoff,maxcut,node,fo):
    maxval = float("-inf")
    if player == "X":
        enemy = "O"
    else:
        enemy = "X"

    if cutoff is 0:
        sumval = 0
        for i, rows in enumerate(staboard):
            for j, item in enumerate(rows):
                if staboard[i][j] is player:
                    sumval += valboard[i][j]
                elif staboard[i][j] is enemy:
                        sumval -= valboard[i][j]
        fo.writelines(chr(node[1]+ord('A'))+str(node[0]+1)+","+str(maxcut-cutoff)+","+str(sumval)+"\n")
        return sumval
    for i, rows in enumerate(staboard):
        for j, item in enumerate(rows):
            neighbor = [None for x in range(4)]
            if item is "*":
                if i>0:
                    neighbor[0] = []
                    neighbor[0].append(staboard[i-1][j])
                    neighbor[0].append([i-1,j])
                if i<4:
                    neighbor[2] = []
                    neighbor[2].append(staboard[i+1][j])
                    neighbor[2].append([i+1,j])
                if j>0:
                    neighbor[3] = []
                    neighbor[3].append(staboard[i][j-1])
                    neighbor[3].append([i,j-1])
                if j<4:
                    neighbor[1] = []
                    neighbor[1].append(staboard[i][j+1])
                    neighbor[1].append([i,j+1])
                enemycoord = []
                for item in neighbor:
                    if item is not None and item[0] is player:
                        for itemene in neighbor:
                            if itemene is not None and itemene[0] is enemy:
                                row = itemene[1][0]
                                col = itemene[1][1]
                                enemycoord.append(itemene[1])
                        break
                newboard = copy.deepcopy(staboard)
                newboard[i][j] = player
                for coor in enemycoord:
                    newboard[coor[0]][coor[1]] = player
                if maxval == float('-inf'):
                    fo.writelines(chr(node[1]+ord('A'))+str(node[0]+1)+","+str(maxcut-cutoff)+","+"-Infinity"+"\n")
                else:
                    fo.writelines(chr(node[1]+ord('A'))+str(node[0]+1)+","+str(maxcut-cutoff)+","+str(maxval)+"\n")
                val = min(enemy, newboard,cutoff-1,maxcut,[i,j],fo)
                if val > maxval:
                    maxval = val
    fo.writelines(chr(node[1]+ord('A'))+str(node[0]+1)+","+str(maxcut-cutoff)+","+str(maxval)+"\n")
    return maxval 

def min_beta(player, staboard, cutoff,maxcut,node,fo,alpha, beta):
    minval = float("inf")
    if player == "X":
        enemy = "O"
    else:
        enemy = "X"

    if cutoff is 0:
        sumval = 0
        for i, rows in enumerate(staboard):
            for j, item in enumerate(rows):
                if staboard[i][j] is player:
                    sumval += valboard[i][j]
                elif staboard[i][j] is enemy:
                        sumval -= valboard[i][j]
        sumval *= -1
        if alpha == float('-inf') and beta == float('inf'):
            combin = "-Infinity,Infinity"
        elif alpha==float('-inf'):
            combin = "-Infinity,"+str(beta)
        elif beta==float('inf'):
            combin = str(alpha)+",Infinity"
        else:
            combin = str(alpha)+","+str(beta)
        fo.writelines(chr(node[1]+ord('A'))+str(node[0]+1)+","+str(maxcut-cutoff)+","+str(sumval)+","+combin+"\n")
        return sumval
    for i, rows in enumerate(staboard):
        for j, item in enumerate(rows):
            neighbor = [None for x in range(4)]
            if item is "*":
                if i>0:
                    neighbor[0] = []
                    neighbor[0].append(staboard[i-1][j])
                    neighbor[0].append([i-1,j])
                if i<4:
                    neighbor[2] = []
                    neighbor[2].append(staboard[i+1][j])
                    neighbor[2].append([i+1,j])
                if j>0:
                    neighbor[3] = []
                    neighbor[3].append(staboard[i][j-1])
                    neighbor[3].append([i,j-1])
                if j<4:
                    neighbor[1] = []
                    neighbor[1].append(staboard[i][j+1])
                    neighbor[1].append([i,j+1])
                enemycoord = []
                for item in neighbor:
                    if item is not None and item[0] is player:
                        for itemene in neighbor:
                            if itemene is not None and itemene[0] is enemy:
                                row = itemene[1][0]
                                col = itemene[1][1]
                                enemycoord.append(itemene[1])
                        break
                newboard = copy.deepcopy(staboard)
                newboard[i][j] = player
                for coor in enemycoord:
                    newboard[coor[0]][coor[1]] = player
                if minval == float('inf'):
                    if alpha == float('-inf') and beta == float('inf'):
                        combin = "-Infinity,Infinity"
                    elif alpha==float('-inf'):
                        combin = "-Infinity,"+str(beta)
                    elif beta==float('inf'):
                        combin = str(alpha)+",Infinity"
                    else:
                        combin = str(alpha)+","+str(beta)
                    fo.writelines(chr(node[1]+ord('A'))+str(node[0]+1)+","+str(maxcut-cutoff)+","+"Infinity"+","+combin+"\n")
                else:
                    if alpha == float('-inf') and beta == float('inf'):
                        combin = "-Infinity,Infinity"
                    elif alpha==float('-inf'):
                        combin = "-Infinity,"+str(beta)
                    elif beta==float('inf'):
                        combin = str(alpha)+",Infinity"
                    else:
                        combin = str(alpha)+","+str(beta)
                    fo.writelines(chr(node[1]+ord('A'))+str(node[0]+1)+","+str(maxcut-cutoff)+","+str(minval)+","+combin+"\n")
                val = max_alpha(enemy, newboard,cutoff-1,maxcut,[i,j],fo,alpha,beta)
                if val<=alpha:
                    if alpha == float('-inf') and beta == float('inf'):
                        combin = "-Infinity,Infinity"
                    elif alpha==float('-inf'):
                        combin = "-Infinity,"+str(beta)
                    elif beta==float('inf'):
                        combin = str(alpha)+",Infinity"
                    else:
                        combin = str(alpha)+","+str(beta)
                    fo.writelines(chr(node[1]+ord('A'))+str(node[0]+1)+","+str(maxcut-cutoff)+","+str(val)+","+combin+"\n")
                    return val
                if val < minval:
                    minval = val
                    beta = minval
    if alpha == float('-inf') and beta == float('inf'):
        combin = "-Infinity,Infinity"
    elif alpha==float('-inf'):
        combin = "-Infinity,"+str(beta)
    elif beta==float('inf'):
        combin = str(alpha)+",Infinity"
    else:
        combin = str(alpha)+","+str(beta)

    fo.writelines(chr(node[1]+ord('A'))+str(node[0]+1)+","+str(maxcut-cutoff)+","+str(minval)+","+combin+"\n")
    return minval 

def max_alpha(player, staboard, cutoff,maxcut,node,fo,alpha,beta):
    maxval = float("-inf")
    if player == "X":
        enemy = "O"
    else:
        enemy = "X"

    if cutoff is 0:
        sumval = 0
        for i, rows in enumerate(staboard):
            for j, item in enumerate(rows):
                if staboard[i][j] is player:
                    sumval += valboard[i][j]
                elif staboard[i][j] is enemy:
                        sumval -= valboard[i][j]
        if alpha == float('-inf') and beta == float('inf'):
            combin = "-Infinity,Infinity"
        elif alpha==float('-inf'):
            combin = "-Infinity,"+str(beta)
        elif beta==float('inf'):
            combin = str(alpha)+",Infinity"
        else:
            combin = str(alpha)+","+str(beta)
        fo.writelines(chr(node[1]+ord('A'))+str(node[0]+1)+","+str(maxcut-cutoff)+","+str(sumval)+","+combin+"\n")
        return sumval
    for i, rows in enumerate(staboard):
        for j, item in enumerate(rows):
            neighbor = [None for x in range(4)]
            if item is "*":
                if i>0:
                    neighbor[0] = []
                    neighbor[0].append(staboard[i-1][j])
                    neighbor[0].append([i-1,j])
                if i<4:
                    neighbor[2] = []
                    neighbor[2].append(staboard[i+1][j])
                    neighbor[2].append([i+1,j])
                if j>0:
                    neighbor[3] = []
                    neighbor[3].append(staboard[i][j-1])
                    neighbor[3].append([i,j-1])
                if j<4:
                    neighbor[1] = []
                    neighbor[1].append(staboard[i][j+1])
                    neighbor[1].append([i,j+1])
                enemycoord = []
                for item in neighbor:
                    if item is not None and item[0] is player:
                        for itemene in neighbor:
                            if itemene is not None and itemene[0] is enemy:
                                row = itemene[1][0]
                                col = itemene[1][1]
                                enemycoord.append(itemene[1])
                        break
                newboard = copy.deepcopy(staboard)
                newboard[i][j] = player
                for coor in enemycoord:
                    newboard[coor[0]][coor[1]] = player
                if maxval == float('-inf'):
                    if alpha == float('-inf') and beta == float('inf'):
                        combin = "-Infinity,Infinity"
                    elif alpha==float('-inf'):
                        combin = "-Infinity,"+str(beta)
                    elif beta==float('inf'):
                        combin = str(alpha)+",Infinity"
                    else:
                        combin = str(alpha)+","+str(beta)
                    fo.writelines(chr(node[1]+ord('A'))+str(node[0]+1)+","+str(maxcut-cutoff)+","+"-Infinity"+","+combin+"\n")
                else:
                    if alpha == float('-inf') and beta == float('inf'):
                        combin = "-Infinity,Infinity"
                    elif alpha==float('-inf'):
                        combin = "-Infinity,"+str(beta)
                    elif beta==float('inf'):
                        combin = str(alpha)+",Infinity"
                    else:
                        combin = str(alpha)+","+str(beta)
                    fo.writelines(chr(node[1]+ord('A'))+str(node[0]+1)+","+str(maxcut-cutoff)+","+str(maxval)+","+combin+"\n")
                val = min_beta(enemy, newboard,cutoff-1,maxcut,[i,j],fo,alpha,beta)
                if val >= beta:
                    if alpha == float('-inf') and beta == float('inf'):
                        combin = "-Infinity,Infinity"
                    elif alpha==float('-inf'):
                        combin = "-Infinity,"+str(beta)
                    elif beta==float('inf'):
                        combin = str(alpha)+",Infinity"
                    else:
                        combin = str(alpha)+","+str(beta)
                    fo.writelines(chr(node[1]+ord('A'))+str(node[0]+1)+","+str(maxcut-cutoff)+","+str(maxval)+","+combin+"\n")
                    return val
                if val > maxval:
                    maxval = val
                    alpha = maxval
    if alpha == float('-inf') and beta == float('inf'):
        combin = "-Infinity,Infinity"
    elif alpha==float('-inf'):
        combin = "-Infinity,"+str(beta)
    elif beta==float('inf'):
        combin = str(alpha)+",Infinity"
    else:
        combin = str(alpha)+","+str(beta)
    fo.writelines(chr(node[1]+ord('A'))+str(node[0]+1)+","+str(maxcut-cutoff)+","+str(maxval)+","+combin+"\n")
    return maxval 

def battle(staboard,player,first_algor,first_cutoff,enemy,second_algor,second_cutoff):
    fo = open("trace_state.txt","w+")
    total = 0
    for rows in staboard:
        for cols in rows:
            if cols == "*":
                total += 1
    while total > 0:
        if first_algor==1:
            best_first(staboard,first_cutoff,player,enemy)
        elif first_algor==2:
            minimax(staboard,first_cutoff,player,enemy)
        elif first_algor==3:
            minimax_alpha_beta(staboard,first_cutoff,player,enemy)
        for val in staboard:
            line = ""
            for item in val:
                line += item
            line += "\n"
            fo.writelines(line)
        total -= 1
        if total > 0:
            if second_algor==1:
                best_first(staboard,second_cutoff,ememy,player)
            elif second_algor==2:
                minimax(staboard,second_cutoff,enemy,player)
            elif second_algor==3:
                minimax_alpha_beta(staboard,second_cutoff,enemy,player)
            for val in staboard:
                line = ""
                for item in val:
                    line += item
                line += "\n"
                fo.writelines(line)
            total -= 1
            
def main_logic(argv):
    try:
        opts,args = getopt.getopt(argv,"i:")
    except getopt.GetoptError:
        print "argument error"
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-i"):
            filename = arg
        else:
            print "input file error"
            sys.exit(2)

    staboard = [[None for x in range(5)] for x in range(5)] 
    global valboard
    valboard = [[0 for x in range(5)] for x in range(5)]
    fp = open(filename)
    for i, line in enumerate(fp):
        if i==0:
            task = int(line)
            if task==4:
                break;
        elif i==1:
            player = line.split()[0]
            if player is "X":
                enemy = "O"
            elif player is "O":
                enermy = "X"
        elif i==2:
            cutoff = int(line)
            if cutoff<=0:
                sys.exit(2)
        elif i>=3 and i<8:
            for index, item in enumerate(line.split()):
                valboard[i-3][index] = int(item)
        elif i>=8 and i<13:
            for index, item in enumerate(line.split()[0]):
                staboard[i-8][index] = item
    if task!=4:
        total = 0
        for rows in staboard:
            for cols in rows:
                total += 1
        if total < cutoff:
            cutoff = total
            maxcut = cutoff
    if task==1:
        best_first(staboard,cutoff,player,enemy)
        fo = open("next_state.txt","w+")
        for item in staboard:
            line = ""
            for val in item:
                line += val
            line += "\n"
            fo.writelines(line)
        fo.close()
    elif task==2:        
        minimax(staboard,cutoff,player,enemy)
        fo = open("next_state.txt","w+")
        for item in staboard:
            line = ""
            for val in item:
                line += val
            line += "\n"
            fo.writelines(line)
        fo.close()
    elif  task==3:
        minimax_alpha_beta(staboard,cutoff,player,enemy)
        fo = open("next_state.txt","w+")
        for item in staboard:
            line = ""
            for val in item:
                line += val
            line += "\n"
            fo.writelines(line)
        fo.close()
    elif task==4:
        fp.close()
        fp = open(filename)
        for i, line in enumerate(fp):
            if i==0:
                task = int(line)
            elif i==1:
                player = line.split()[0]
            elif i==2:
                first_algor = int(line)
            elif i==3:
                first_cutoff = int(line)
                if first_cutoff<=0:
                    sys.exit(2)
            elif i==4:
                enemy = line.split()[0]
            elif i==5:
                second_algor = int(line)
            elif i==6:
                second_cutoff = int(line)
                if second_cutoff<=0:
                    sys.exit(2)
            elif i>=7 and i<12:
                for index, item in enumerate(line.split()):
                    valboard[i-7][index] = int(item)
            elif i>=12 and i<17:
                for index, item in enumerate(line.split()[0]):
                    staboard[i-12][index] = item
        total = 0
        for rows in staboard:
            for cols in rows:
                total += 1
        if total < first_cutoff:
            first_cutoff = total
        if total < second_cutoff:
            second_cutoff = total

        battle(staboard,player,first_algor,first_cutoff,enemy,second_algor,second_cutoff)
        fo = open("next_state.txt","w+")
        for item in staboard:
            line = ""
            for val in item:
                line += val
            line += "\n"
            fo.writelines(line)
        fo.close()

if __name__=="__main__":
    main_logic(sys.argv[1:])
