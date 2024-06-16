def encrypt(text, key_encrypt: int = 3):
    result = ""

    # traverse text
    for i in range(len(text)):
        char = text[i]

        if char.isupper():
            result += chr((ord(char) + key_encrypt - 65) % 26 + 65)
        else:
            result += chr((ord(char) + key_encrypt - 97) % 26 + 97)

    return result


def decrypt(text):
    result = ""

    for index in range(len(text)):
        char = ord(text[index])
        decrypt_pass = char - 103
        result += str(decrypt_pass)
    return result
