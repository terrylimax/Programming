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

def decrypt_caesar(ciphertext, shift):
    plaintext = ""
    for symbol in ciphertext:
        if ord(symbol.upper()) - shift%26 < ord('A'):
            plaintext += chr(ord(symbol) - shift%26 + 26)
        else:
            plaintext += chr(ord(symbol) - shift%26)
    print(plaintext)
    return plaintext
decrypt_caesar("SBWKRQ",29)
decrypt_caesar("sbwkrq",29)