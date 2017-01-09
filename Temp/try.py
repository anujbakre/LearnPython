if __name__ == '__main__':
    N = int(input())
    lyst = []
    cmd = [""] * 3
    d = {"insert": "lyst.insert(int(cmd[1]),int(cmd[2]))"}
    d ["print"]= "print(lyst)"
    d ["remove"] = "lyst.remove(int(cmd[1]))"
    d ["append"]= "lyst.append(int(cmd[1]))"
    d ["sort"] = "lyst.sort()"
    d ["pop"] =  "lyst.pop()"
    d ["reverse"]= "lyst.reverse()"

    for x in range(N):
        cmd = input().split()
        if cmd[0] in d:
            eval(d[cmd[0]])