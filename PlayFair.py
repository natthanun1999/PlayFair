characters =   ['A', 'B', 'C', 'D', 'E', 'F', 'G',
                'H', 'I', 'J', 'K', 'L', 'M', 'N',
                'O', 'P', 'Q', 'R', 'S', 'T', 'U',
                'V', 'W', 'X', 'Y', 'Z']

pairs_letters = []

cipher_text = []

decrypt_text = []

# Square Table [5 x 5]
rows = 5
cols = 5
table = [[0 for c in range(cols)] for r in range(rows)] 

# Clean Text
def CleanText():
    global secret_key, plain_text, characters

    # Make to Upper Characters and remove Empty Space
    secret_key = secret_key.strip()
    secret_key = secret_key.upper()

    plain_text = plain_text.strip()
    plain_text = plain_text.upper()

    # Check Duplicate Characters
    for char in secret_key:
        for letter in characters:
            if (letter == char):
                characters.remove(letter)
                break
    
    # Except 'J'
    try:
        characters.remove('J')
    except:
        pass

# Pairs of two letters
def PairsLetters():
    global secret_key, plain_text, characters, pairs_letters

    word = ''

    count = 0
    
    # Pairs of two letters
    for n in range(len(plain_text)):
        letter = plain_text[n]

        try:
            if (plain_text[n + 1] is None):
                pass
            elif (letter == plain_text[n + 1]):
                word += letter
                word += 'X'
                count += 2
            else:
                word += letter
                count += 1
        except:
            if (len(word) == 1):
                word += letter
                count += 1
            else:
                word += letter
                word += 'Z'
                count += 2

        if (count == 2):
            pairs_letters.append(word)

            word = ''
            count = 0

# Insert data to table
def InsertToTable():
    global secret_key, plain_text, characters, pairs_letters, table

    # Combind all characters
    combinded_letters = secret_key + "".join(characters)

    # Letter position
    letter_pos = 0

    # Put Letters to table
    for r in range(5):
        for c in range(5):
            table[r][c] = combinded_letters[letter_pos]
            letter_pos += 1

# Encryption
def Encrypt():
    global pairs_letters, table, cipher_text

    # Table
    # Rows : 0-4
    # Cols : 0-4

    compare_rows = []
    compare_cols = []
    r = 0
    c = 0
    found = False

    # Encoding to make Cipher Text
    for pairs in pairs_letters:                 # <= Encode each of pairs letters
        for letter in pairs:                    # <= Get each letter of pairs letters
            for rows_pos in table:              # <= Go on Rows of Table
                for cols_pos in rows_pos:       # <= Go in Columns of Rows (1 Cols = 1 Letter)
                    if (cols_pos == letter):    # <= Founded Letter And Save Pos. [Rows, Cols]
                        found = True
                        break
                    else:
                        c += 1
                
                if (found == True):
                    compare_rows.append(r)      # <= Save Pos. [Rows] to Comparable
                    compare_cols.append(c)      # <= Save Pos. [Cols] to Comparable

                    found = False

                    r = 0
                    c = 0

                    break
                else:
                    r += 1
                    c = 0

        # Algorithm
        if (compare_rows[0] == compare_rows[1]):                        # <= On Same Rows
            compare_cols[0] = (compare_cols[0] + 1) % 5                 # <= Pick Right Letter
            compare_cols[1] = (compare_cols[1] + 1) % 5
        elif (compare_cols[0] == compare_cols[1]):                      # <= On Same Cols
            compare_rows[0] = (compare_rows[0] + 1) % 5                 # <= Pick Below Letter
            compare_rows[1] = (compare_rows[1] + 1) % 5
        else:                                                           # <= Neither of two
            if (compare_cols[0] > compare_cols[1]):                     # <= If First Letter has position value more than Second Letter
                difference = compare_cols[0] - compare_cols[1]
                                                                        
                compare_cols[0] = (compare_cols[0] - difference) % 5    # <= First  Letter Pick Far Left
                compare_cols[1] = (compare_cols[1] + difference) % 5    # <= Second Letter Pick Far Right
            else:                                                       # <= If First Letter has position value less than Second Letter
                difference = compare_cols[1] - compare_cols[0]

                compare_cols[0] = (compare_cols[0] + difference) % 5    # <= First  Letter Pick Far Right
                compare_cols[1] = (compare_cols[1] - difference) % 5    # <= Second Letter Pick Far Left
        
        # Pair Letter
        pair =  table[compare_rows[0]][compare_cols[0]] + table[compare_rows[1]][compare_cols[1]]
        cipher_text.append(pair)
        
        # Clear Compare Position
        compare_rows.clear()
        compare_cols.clear()

    print('------------------------')

    # Print Test
    for items in table:
        print(items)

    print('------------------------')
    
    # Plain Text
    print("Plain Text  : " + "".join(pairs_letters))

    # Cipher Text
    print("Cipher Text : " + "".join(cipher_text))

    print('=> Encryption Success!')

# Decryption
def Decrypt():
    global table, cipher_text, decrypt_text

    # Table
    # Rows : 0-4
    # Cols : 0-4

    compare_rows = []
    compare_cols = []
    r = 0
    c = 0
    found = False

    # Decoding Cipher Text to Plain Text
    for pairs in cipher_text:
        for letter in pairs:
            for rows_pos in table:
                for cols_pos in rows_pos:
                    if (cols_pos == letter):
                        found = True
                        break
                    else:
                        c += 1
                
                if (found == True):
                    compare_rows.append(r)
                    compare_cols.append(c)

                    found = False

                    r = 0
                    c = 0

                    break
                else:
                    r += 1
                    c = 0

        # Algorithm
        if (compare_rows[0] == compare_rows[1]):                        # <= On Same Rows
            if (compare_cols[0] == 0):                                  # <= Pick far right letter, If first letter at far left
                compare_cols[0] = 4                                     
            else:
                compare_cols[0] = (compare_cols[0] - 1)                 # <= Pick left letter
            
            if (compare_cols[1] == 0):                                  # <= Pick far right letter, If second letter at far left
                compare_cols[1] = 4
            else:
                compare_cols[1] = (compare_cols[1] - 1)                 # <= Pick left letter
        elif (compare_cols[0] == compare_cols[1]):                      # <= On Same Cols
            if (compare_rows[0] == 0):                                  # <= Pick bottom letter, If first letter at top
                compare_rows[0] = 4
            else:
                compare_rows[0] = (compare_rows[0] - 1)                 # <= Pick upper letter

            if (compare_rows[1] == 0):                                  # <= Pick bottom letter, If second letter at top
                compare_rows[1] = 4
            else:
                compare_rows[1] = (compare_rows[1] - 1)                 # <= Pick upper letter
        else:                                                           # <= Neither of two
            if (compare_cols[0] > compare_cols[1]):                     # <= If First Letter has position value more than Second Letter
                difference = compare_cols[0] - compare_cols[1]

                compare_cols[0] = (compare_cols[0] - difference) % 5    # <= First  Letter Pick Far Left
                compare_cols[1] = (compare_cols[1] + difference) % 5    # <= Second Letter Pick Far Right
            else:                                                       # <= If First Letter has position value less than Second Letter
                difference = compare_cols[1] - compare_cols[0]

                compare_cols[0] = (compare_cols[0] + difference) % 5    # <= First  Letter Pick Far Right
                compare_cols[1] = (compare_cols[1] - difference) % 5    # <= Second Letter Pick Far Left
        
        # Pair Letter
        pair =  table[compare_rows[0]][compare_cols[0]] + table[compare_rows[1]][compare_cols[1]]
        decrypt_text.append(pair)
        
        # Clear Compare Position
        compare_rows.clear()
        compare_cols.clear()

    # Cipher Text
    print("Cipher Text : " + "".join(cipher_text))

    # Plain Text
    print("Plain Text  : " + "".join(decrypt_text))

    print('=> Decryption Success!')

# Input
secret_key = str(input('Enter Secret Key : '))
plain_text = str(input('Enter Text to Encrypt : '))

# Calling
CleanText()

PairsLetters()

InsertToTable()

Encrypt()

print('------------------------')

Decrypt()

print('------------------------')