# to find the next key char in the AMR
def find_min(str):
    ans = len(str)+1
    if str.find('(')!=-1:
        ans = min(str.index('('),ans)
    if str.find(')')!=-1:
        ans = min(str.index(')'),ans)
    if str.find('/')!=-1:
        ans = min(str.index('/'),ans)
    if str.find(':')!=-1:
        ans = min(str.index(':'),ans)
    if ans == len(str)+1:
        return 0
    else:
        return ans

# the translator from AMR text format to conjunction of triples
def translator(input,output):
    # read the dataset
    with open(input, 'r', encoding='utf8') as load:
        loads = load.readlines()

    amr = ''
    for line in loads:
        if line[0] == '#':
            continue

        # process one AMR
        if line == '\n' and amr != '':
            with open(output, 'a', encoding='utf8') as fo:
                fo.write('\n')
            instance = []  # the instance
            arg = []  # the relation
            stack = []  # store each layer's instance in the stack judged by the brackets
            while 1:
                # if the key char is ( ,push the word into the stack
                if amr[0] == '(':
                    amr = amr[1:]
                    temp = find_min(amr)
                    word = amr[0:temp]
                    word = word.strip()
                    amr = amr[temp:]
                    stack.append(word)
                # if the key char is ), pop the word from the stack
                elif amr[0] == ')':
                    stack.pop()
                    amr = amr[1:]
                # if the key char is /, store the words on the both sides of it in the instance
                elif amr[0] == '/':
                    amr = amr[1:]
                    temp = find_min(amr)
                    word = amr[0:temp]
                    word = word.strip()
                    amr = amr[temp:]
                    instance.append({'var': stack[-1], 'instance': word})

                # if the key char is :
                elif amr[0] == ':':
                    flag = 1
                    amr = amr[1:]
                    temp = find_min(amr)
                    judge = amr.find(' ')
                    # if the word is not a instance
                    if judge < temp and amr[judge + 1] != '(':
                        flag = 0
                        rel = amr[0:judge]
                        rel.strip()
                        amr = amr[judge:]
                    else:  # if the word is a instance
                        rel = amr[0:temp]
                        rel.strip()
                        amr = amr[temp:]

                    amr = amr[1:]
                    temp = find_min(amr)
                    word = amr[0:temp]
                    word = word.strip()
                    amr = amr[temp:]
                    arg.append({'rel': rel.strip(), 'a': stack[-1], 'b': word})  # store the relation
                    if flag == 1:
                        stack.append(word)  # if the word is a instance, push it into the stack
                if amr == '':  # end
                    break
                if amr[0] == ' ':
                    amr = amr[1:]
            with open(output, 'a', encoding='utf8') as fo:
                for i in instance:
                    fo.write("instance(" + i['var'] + "," + i['instance'] + ")" + "\n")
                for i in arg:
                    fo.write(i['rel'] + "(" + i['a'] + "," + i['b'] + ")" + "\n")

        with open(output, 'a', encoding='utf8') as fo:
            fo.write(line)
        line = line.strip()
        line = line.strip('\n')
        amr += line


if __name__ == '__main__':
    translator("amr-bank-struct-v3.0.txt","triples.txt")