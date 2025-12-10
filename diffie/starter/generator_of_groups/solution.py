p = 28151
print(next((g for g in range(1, p) if len(set([pow(g, k, p) for k in range(p)])) == p - 1)))
