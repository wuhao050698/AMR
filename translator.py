def translator(input,output):
    # read the dataset
    with open(input, 'r', encoding='utf8') as load:
        loads = load.readlines()
    h = 0
    cnt = 0
    instance = []  # the instance
    arg = []  # the edge
    judge = []  # judge the same instance
    last_rank = 0  # Determine the number of layers of the current node according to the brackets
    last_var = ''  # last variable
    father = {}  # Record the parent node of each layer

    # process
    for line in loads:

        if line == '\n':
            h = 0
            cnt = 0
            instance = []  # the instance
            arg = []  # the edge
            judge = []  # judge the same instance
            last_rank = 0  # Determine the number of layers of the current node according to the brackets
            last_var = ''  # last variable
            father = {}  # Record the parent node of each layer
            continue
        if line[0] == '#':
            continue


        # preprocess
        h += 1
        flag = 0
        line = line.strip('\n')
        rank=line.count('(')-line.count(')')+last_rank
        line = line.replace('(', '')
        line = line.replace(')', '')
        line = line.replace('/ ', '')
        line = line.replace(':', '')
        line = line.strip()
        s_line = line.split(' ')

        if h == 1:  # the root
            instance.append({'var': s_line[0], 'instance': s_line[1]})
            judge.append(s_line[0])
            last_rank = rank
            last_var = s_line[0]
            continue
        else:
            if len(s_line) == 2:
                if s_line[1] not in judge:
                    instance.append({'var': s_line[1], 'instance': s_line[1]})
                    judge.append(s_line[1])
            else:
                instance.append({'var': s_line[1], 'instance': s_line[2]})
                judge.append(s_line[1])
        # if it's a new laywer, store its father
        if last_rank not in father.keys():
            father[last_rank] = last_var
        last_var = s_line[1]
        arg.append({'rel': s_line[0], 'a': father[last_rank], 'b': s_line[1]})
        last_rank = rank

        # If the AMR has ended, store the generated triples in a file
        if last_rank==0:
            with open(output, 'a', encoding='utf8') as fo:
                for i in instance:  # the instance
                    fo.write("instance(" + i['var'] + "," + i['instance'] + ")" + "\n")
                for i in arg:  # the arg
                    fo.write(i['rel'] + "(" + i['a'] + "," + i['b'] + ")" + "\n")
                fo.write("\n")
            continue


if __name__ == '__main__':
    translator("amr-bank-struct-v3.0.txt","triples.txt")