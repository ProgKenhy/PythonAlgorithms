def findAns(ans: int, N: int = 100) -> (int, int):
    tries = 2
    cur_h = 0
    throws = 0
    mul_ = 0
    max_h = 100
    while tries != 1 and cur_h + mul_ // 2 < N:
        throws += 1
        mul_ = N // (2**throws)
        if mul_ < 2:
            mul_ = 2

        cur_h += mul_
        # print(f"first={cur_h}")

        if cur_h >= ans:
            tries -= 1
            max_h = cur_h
            cur_h -= mul_
            break

    while tries != 0 and cur_h+1 < N and cur_h + 1 < max_h:
        throws += 1
        cur_h += 1
        # print(f"second={cur_h}")
        if cur_h >= ans:
            tries -= 1
            break

    if tries == 0:
        return cur_h-1, throws
    else:
        return cur_h, throws


for i in range(0, 102):
    cur_h, throws = findAns(i, 100)
    if cur_h != i-1:
        print(f"H={cur_h}, throws={throws}")
    # print(f"{cur_h}, {throws}")



