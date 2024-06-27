def generate_key_matrix(key):
    # Convert key to uppercase and replace 'J' with 'I'
    key = key.upper().replace('J', 'I')
    matrix = []
    used = set()

    # Add characters of the key to the matrix if not already used
    for char in key:
        if char not in used:
            used.add(char)
            matrix.append(char)

    # Add remaining letters of the alphabet to the matrix
    for char in 'ABCDEFGHIKLMNOPQRSTUVWXYZ':  # 'J' is excluded
        if char not in used:
            used.add(char)
            matrix.append(char)

    # Create a 5x5 matrix
    return [matrix[i * 5:(i + 1) * 5] for i in range(5)]

def find_position(matrix, char):
    # Find the row and column position of a character in the matrix
    for i, row in enumerate(matrix):
        if char in row:
            return i, row.index(char)
    return None

def decrypt_playfair(ciphertext, key):
    # Generate the key matrix
    matrix = generate_key_matrix(key)
    plaintext = []
    ciphertext = ciphertext.upper().replace('J', 'I')

    # Process the ciphertext in pairs of characters
    for i in range(0, len(ciphertext), 2):
        a, b = ciphertext[i], ciphertext[i + 1]
        row1, col1 = find_position(matrix, a)
        row2, col2 = find_position(matrix, b)

        # Apply Playfair Cipher decryption rules
        if row1 == row2:
            # Same row: replace with letters to the left
            plaintext.append(matrix[row1][(col1 - 1) % 5])
            plaintext.append(matrix[row2][(col2 - 1) % 5])
        elif col1 == col2:
            # Same column: replace with letters above
            plaintext.append(matrix[(row1 - 1) % 5][col1])
            plaintext.append(matrix[(row2 - 1) % 5][col2])
        else:
            # Form a rectangle: replace with letters on the same row but at the opposite corners
            plaintext.append(matrix[row1][col2])
            plaintext.append(matrix[row2][col1])

    decrypted_text = ''.join(plaintext)

    # Remove 'X' characters that were added for padding or separation
    final_text = []
    i = 0
    while i < len(decrypted_text):
        if decrypted_text[i] == 'X':
            if (i > 0 and i < len(decrypted_text) - 1 and 
                decrypted_text[i - 1] == decrypted_text[i + 1]):
                i += 1
                continue
        final_text.append(decrypted_text[i])
        i += 1

    # Remove trailing 'X' that were used for padding
    while final_text and final_text[-1] == 'X':
        final_text.pop()

    return ''.join(final_text)

if __name__ == "__main__":
    # Encrypted message and key
    encrypted_message = "IKEWENENXLNQLPZSLERUMRHEERYBOFNEINCHCV"
    key = "SUPERSPY"
    
    # Decrypt the message
    decrypted_message = decrypt_playfair(encrypted_message, key)
    
    # Output the decrypted message
    print(decrypted_message)

