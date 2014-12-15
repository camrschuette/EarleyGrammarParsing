#Cameron Schuette
##Earley Grammar Parsing

import sys, re
from item import item

flag = True ##global flag for determining sameness
sg = "" ##global for finding the starting node

def error_check(N, terminals, file):

    ##find the terminals in the beginning of the file
    ##and put them into a list of tuples
    ##ex: ('IF', [regex stmt])
    fp = open(file)
    rex = re.compile(r'(\S+)\s?->\s?(.+)')
    for line in fp:
        if line == "\n":
            break
        x = re.findall(rex, line)
        for i in x:
            tmp = i[1].split('|')
            a = []
            for j in tmp:
                a.append(re.compile(j))
            terminals.append((i[0], a))

    ##find the nonterminals and put them into a dict
    ##ex: 'S': [['stmt', 'expr'], ['COMMA']]
    rex = fp.read().strip().splitlines()
    x = re.compile('([\w\'-]*)\s?->\s?(.*)')

    ctr = 0
    for i in rex:
        i = re.findall(x, i)[0]
        if not ctr:
            global sg
            sg = i[0]
            ctr = 1
        r = i[1].split('|')
        if i[0] not in N:
            N[i[0]] = []
        elif i[0] in N:
            print("More than one of same nonterminal")
            return
        for j in r:
            p = j.split(" ")
            for k in p:
                if k == "":
                    p.remove("")
            if j == 'epsilon':
                N[i[0]].append(['epsilon'])
            else:
                N[i[0]].append(p)

    ##ERRONEOUS##########################
        # -no double terminal declaration
        # -no double non terminal declaration
        # -not defined anywhere
        # -defined in two places
    seen = set()
    for i in range(0, len(terminals)):
        if terminals[i][0] not in seen:
            seen.add(terminals[i][0])
        elif terminals[i] in seen:
            print("More than one of same terminal")
            return

    for k in N:
        if k not in seen:
            seen.add(k)
        elif k in seen:
            print("Defined in more than one place")
            return


    for k in N:
        for x in N[k]:
            for y in x:
                if y == 'epsilon' or y == 'EPSILON':
                    continue
                if y not in seen:
                    print(y + " not defined anywhere")
                    return

def token_check(gram, input):

    ##read in grammar file and check errors
    terminals = []
    N = {}
    error_check(N, terminals, gram)

    ##read in input and put in terminal key if
    ##one of the strings matches
    matches = []

    fp = open(input)
    for line in fp:
        line = line.replace("\n", "")
        line = line.split(" ")
        for i in line:
            s = ""
            while len(i) > 0 and i != s:
                s = i.strip()
                for k in terminals:
                    for v in k[1]:
                        tmp = re.search(v, i)
                        if tmp:
                            matches.append(k[0])
                            q = tmp.regs[0]
                            i = i.replace(i[q[0]:q[1]], "")
                            break

    return terminals, N, matches

def scan(L, i, j, matches, N, T):
    if L.dpos == len(L.rhs):
        return

    if j != len(T) and L.rhs[L.dpos] == matches[j]:
        L2 = item(L.lhs, L.rhs, L.dpos + 1)

        inside = False
        for x in T[i][j+1]:
            if L2.lhs == x.lhs and L2.rhs == x.rhs:
                    inside = True
                    break
        if not inside:
            T[i][j+1].add(L2)
            global flag
            flag = True

def predict(L, i, j, matches, N, T):
    if L.dpos == len(L.rhs):
        return

    Q = L.rhs[L.dpos]
    if Q in N:
        for P in N[Q]:
            L2 = item(Q, P, 0)

            inside = False
            for x in T[j][j]:
                if L2.lhs == x.lhs and L2.rhs == x.rhs:
                    inside = True
                    break
            if not inside:
                T[j][j].add(L2)
                global flag
                flag = True

def complete(L, i, j, matches, N, T):
    if L.dpos != len(L.rhs):
        return

    for k in range(0, i+1):
        tmp2 = list(T[k][i])
        for L2 in tmp2:
            if L2.dpos != len(L2.rhs) and L2.rhs[L2.dpos] == L.lhs:
                L3 = item(L2.lhs, L2.rhs, L2.dpos+1)
                inside = False
                for x in T[k][j]:
                    if L3.lhs == x.lhs and L3.rhs == x.rhs:
                        inside = True
                        break
                if not inside:
                    T[k][j].add(L3)
                    global flag
                    flag = True

def process_column(j, matches, N, T):
    global flag
    flag = True
    while (flag):
        global flag
        flag = False
        for i in range(0, j+1):
            tmp = list(T[i][j])
            for l in tmp:
                scan(l, i, j, matches, N, T)
                predict(l, i, j, matches, N, T)
                complete(l, i, j, matches, N, T)

def main():
    try:
        gram = sys.argv[1]
        input = sys.argv[2]
    except IndexError:
        print("Please enter two files: a grammar specification file and an input file")

    ##find terminals, Nodes, and the token matches
    terminals, N, matches = token_check(gram, input)

    T = [] ##list we will be using to store the scan, predict, complete results

    n = len(matches) + 1
    for i in range(0, n):
        T.append([])
        for j in range(0, n):
            T[i].append(set())

    ##creating the start position
    tmp = item("S'", sg, 0)
    T[0][0].add(tmp)
    for j in range(0, n):
        process_column(j, matches, N, T)

    ##checking if the input is is the grammar
    for i in T[0][-1]:
        if i.rhs == sg:
            print('yes')
            return

    print('no')

if __name__ == "__main__":
    main()