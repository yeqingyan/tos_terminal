def char_to_bin(char):
    if ord(char) > 127 or ord(char) < 0:
        return []
    bin_value = [int(value) for value in "{0:0=7b}".format(ord(char))]
    return bin_value
    
def bin_to_char(bin_values):
    result = 0
    for i,j in zip(xrange(0, 8), xrange(6, -1, -1)):
        result += bin_values[i] << j
    if result > 127:
        result = 0
    return chr(result)    