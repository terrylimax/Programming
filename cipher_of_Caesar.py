def encrypt_caesar(plaintext, shift):
    ciphertext = ""
    for symbol in plaintext:
        if ord(symbol.upper()) + shift%26 > ord('Z'):
            ciphertext += chr(ord(symbol) + shift%26 - 26)
        else:
            ciphertext += chr(ord(symbol) + shift%26)
    print(ciphertext)
    return ciphertext
encrypt_caesar("PYTHON",29)
encrypt_caesar("python",29)