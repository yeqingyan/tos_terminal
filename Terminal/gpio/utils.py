def char_to_bin(char):
    if ord(char) > 255 or ord(char) < 0:
        return []
    bin_value = [int(value) for value in "{0:0=8b}".format(ord(char))]
    return bin_value
    
def bin_to_char(bin_values):
    result = 0
    print bin_values
    for i,j in zip(xrange(0, 8), xrange(7, -1, -1)):
        result += bin_values[i] << j
    if result > 255:
        result = 0
    print "Receive char {0}".format(result)
    return chr(result)    
