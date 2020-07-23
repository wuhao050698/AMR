def translator(input,output):
    # read the dataset
    with open(input, 'r', encoding='utf8') as load:
        loads = load.readlines()
    h = 0
    cnt = 0
    temp = ''
    instance = []  # the instance
    arg = []  # the edge
    judge = [] # judge the same instance

    # process
    for line in loads:

        # extract the original text
        if line[0] == '#':
            cnt += 1
            if cnt == 2:
                with open(output, 'a', encoding='utf8') as fo:
                    fo.write(line)
            continue

        # initialize parameters and variables
        if cnt == 3:
            h = 0
            cnt = 0
            instance = [] # the instance
            arg = [] # the edge
            judge = [] # judge the same instance

        # If the AMR has ended, store the generated triples in a file
        if line == '\n':
            with open(output, 'a', encoding='utf8') as fo:
                for i in instance:  # the instance
                    fo.write("instance(" + i['var'] + "," + i['instance'] + ")" + "\n")
                for i in arg:  # the arg
                    fo.write(i['rel'] + "(" + i['a'] + "," + i['b'] + ")" + "\n")
                fo.write("\n")
            continue

        # preprocess
        h += 1
        flag = 0
        line = line.strip('\n')
        if line[-1] != ')':
            flag = 1
        line = line.replace('(', '')
        line = line.replace(')', '')
        line = line.replace('/ ', '')
        line = line.replace(':', '')
        line = line.strip()
        s_line = line.split(' ')

        if h == 1:  # the root
            instance.append({'var': s_line[0], 'instance': s_line[1]})
            judge.append(s_line[0])
            temp = s_line[0]
            continue
        else:
            if len(s_line) == 2:
                if s_line[1] not in judge:
                    instance.append({'var': s_line[1], 'instance': s_line[1]})
                    judge.append(s_line[1])
            else:
                instance.append({'var': s_line[1], 'instance': s_line[2]})
                judge.append(s_line[1])
        arg.append({'rel': s_line[0], 'a': temp, 'b': s_line[1]})
        # the next point
        if flag == 1:
            temp = s_line[1]


if __name__ == '__main__':
    translator("amr-bank-struct-v3.0.txt","triples.txt")