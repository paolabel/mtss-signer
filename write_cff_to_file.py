import sys
from mtsssigner.cff_builder import *
import ast

if __name__ == '__main__':
    q = int(sys.argv[1])
    k = int(sys.argv[2])
    
    if k == 1:
        # nesse caso q = n
        cff = create_1_cff(q)
        n = q
        t = len(cff)
        d = 1
    else:
        # seleciona 1-cff ou cff polinomial de acordo com d obtido
        cff = create_cff(q, k)
        n = q**k
        t = q**2
        d = get_d(q, k)

    with open(f"cffs/{d}-CFF({t}, {n}).txt", "w", encoding="utf-8") as file:
        for line in cff[:-1]:
            file.write(str(line[0]))
            for block in line[1:]:
                file.write(f" {block}")
            file.write("\n")
        file.write(str(cff[-1][0]))
        for block in cff[-1][1:]:
            file.write(f" {block}")