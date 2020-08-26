
def gen_matrix_reverse(n=4, no_next_join=True):
    # Sq LoL filled with a range
    Sq = [[1 + i + n * j for i in range(n)] for j in range(n)]
    if no_next_join == False:
        for row in Sq[1::2]:
            row.reverse()     # reverse od d row's columns
    return Sq[::-1][:]    # reverse order of rows
