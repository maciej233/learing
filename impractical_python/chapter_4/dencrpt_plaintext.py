"""THIS PROGRAM DECRYPT CIPERTEXT TO PLANTEXT KEY"""

cipertext = "16 12 8 4 0 1 5 9 13 17 18 14 10 6 2 3 7 11 15 19"

cipertext_converted = [str(i) for i in cipertext.split()]

COLS = 4
ROWS = 5
KEY = "-1 2 -3 4"
translation_matrix = [None]*COLS
start = 0
stop = ROWS
plaintext = ''

# confer KEY into seperate numbers
key_converted = [int(i) for i in KEY.split()]

# tranform the cipertext into usefull list
for k in key_converted:
    if k < 0:
        col_items = cipertext_converted[start:stop]
    elif k > 0:
        col_items = list(reversed(cipertext_converted[start:stop]))
    translation_matrix[abs(k) - 1] = col_items
    start += ROWS
    stop += ROWS

# check values
print(f"\ncipertext = {cipertext}")
print(f"translation_matrix = {translation_matrix}")
print(f"KEY = {KEY}")

for i in range(ROWS):
    for item in translation_matrix:
        word = str(item.pop())
        plaintext += word + ' '

print(f"\n plaintext = {plaintext}")
