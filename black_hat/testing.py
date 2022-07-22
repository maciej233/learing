HEX_FILTER = ''.join([(len(repr(chr(i))) == 3) and chr(i) or '.' for i in range(256)])
string = "test1\ntest2\ntest\3"

#hexa = ' '.join([f'{ord(c):02X}' for c in word])

output = []
def fun(src, length=6, show=True):
    for i in range(0, len(src), length):
        word = str(src[i:i+length])
        printable = word.translate(HEX_FILTER)
        hex = ' '.join([f'{ord(c):02X}' for c in word])
        print('normal world: '+word + '\n')
        print('translated word: ' + printable + "\n")
        print(hex)


fun(string)
slowo = "moje slowo"
unicode_test = [f'{ord(litera):02X}' for litera in slowo]



print(unicode_test)
