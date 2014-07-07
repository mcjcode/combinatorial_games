def determine_number_of_twos_and_fours(tiles,score) :
    xx = 0
    for tile in tiles :
        k = int(log(tile)/log(2))
        score += (k-2)*tile
    xx = score - xx
    return xx/2
