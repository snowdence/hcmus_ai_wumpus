
def gen_matrix_reverse(self, n=4):
    # Sq LoL filled with a range
    Sq = [[1 + i + n * j for i in range(n)] for j in range(n)]
    for row in Sq[1::2]:
        row.reverse()     # reverse odd row's columns
    return Sq[::-1][:]    # reverse order of rows
