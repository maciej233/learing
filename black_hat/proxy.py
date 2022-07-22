
FILTER = ''.join(len(repr(chr(i))) == 3 and chr(i) or '.' for i in range(256))
src = 'test1\ntest2\ntest3\n'
# change string to hexadecimal representation
def hexdump(src, length=6, show=True):
    if isinstance(src, bytes): # make sure the input is a string, ints will crush program bcs of ord() function
        src = src.decode()
    output = []
    for i in range(0, len(src), length):
        word = str(src[i:i+length]) # we cut the sensence in pices with parametr length
        printable = word.translate(FILTER) # make printable representation of all characters supported by ASCII
        hex = ' '.join([f'{ord(letter):02X}'for letter in word]) # change every letter in "piece of sentace"= "word" to hex
        hexwidth= length*3 # just for nice show up
        output.append(f'{i:04X} {hex:<{hexwidth}} {printable}') #put all together in the list
    if show:
        for line in output:
            print(line)
    else:
        return output


hexdump(src)


