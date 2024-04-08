from itertools import permutations 

liquidity = {
    ("tokenA", "tokenB"): (17, 10),
    ("tokenA", "tokenC"): (11, 7),
    ("tokenA", "tokenD"): (15, 9),
    ("tokenA", "tokenE"): (21, 5),
    ("tokenB", "tokenC"): (36, 4),
    ("tokenB", "tokenD"): (13, 6),
    ("tokenB", "tokenE"): (25, 3),
    ("tokenC", "tokenD"): (30, 12),
    ("tokenC", "tokenE"): (10, 8),
    ("tokenD", "tokenE"): (60, 25),
}
'''
possible path: 
B -> X1 -> X2 -> B
B -> X1 -> X2 -> X3 -> B
B -> X1 -> X2 -> X3 -> X4 -> B
'''
all_paths = [("tokenB",)+perm+("tokenB",) for perm in list(permutations(["tokenA", "tokenC", "tokenD", "tokenE"])) ]

def swap(del_x, x, y):
    del_y = 997 * del_x * y / (1000 * x + 997 * del_x)
    return del_y

def path(liquidity):
    max_balance = float('-inf')
    max_path = None
    max_amount = []
    valid_path = set()
    # del_x = 5
    flag = True
    for path in all_paths:
        del_x = 5
        amount = [del_x]
        for i in range(len(path)-1):
            new_pair = sorted([path[i], path[i+1]])
            if new_pair == [path[i], path[i+1]]:
                x, y = liquidity[tuple(new_pair)]
            else:
                y, x = liquidity[tuple(new_pair)]

            del_x = swap(del_x, x, y)
            amount.append(del_x)

            # if we end the chain early
            if path[i+1] != "tokenB":
                new_pair = sorted(["tokenB", path[i+1]])
                if new_pair == ["tokenB", path[i+1]]:
                    y, x = liquidity[tuple(new_pair)]
                else:
                    x, y = liquidity[tuple(new_pair)]
                out_x = swap(del_x, x, y)

                if out_x > max_balance:
                    max_balance = out_x
                    max_path = path[:i+2] + ("tokenB",)
                    max_amount = amount + [out_x]
                if out_x > 20:
                    valid_path.add(path[:i+2] + ("tokenB",))

                if path[:i+2] + ("tokenB",) == ("tokenB", "tokenA", "tokenD", "tokenB") and flag:
                    print(f"path: tokenB->tokenA->tokenD->tokenB, tokenB balance={round(out_x, 6)}")
                    flag = False
        if del_x > max_balance:
            max_balance = del_x
            max_path = path
            max_amount = amount

        if del_x > 20:
            valid_path.add(path)
        
    return max_balance, max_path, max_amount, valid_path


max_balance, max_path, max_amount, valid_path = path(liquidity)
# print(f"max_balance = {max_balance}, max_path = {max_path}, max_amount = {max_amount}", f"paths result > 20: {valid_path}", sep='\n')

'''
max_balance = 20.129888944077443, 
max_path = ('tokenB', 'tokenA', 'tokenD', 'tokenC', 'tokenB')
max_amount = [5, 5.655321988655322, 2.4587813170979333, 5.0889272933015155, 20.129888944077443]
paths result > 20: {('tokenB', 'tokenA', 'tokenD', 'tokenC', 'tokenB'), 
('tokenB', 'tokenA', 'tokenE', 'tokenD', 'tokenC', 'tokenB')}
'''