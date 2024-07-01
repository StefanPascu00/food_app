def decrypt(message: str, key: int = 20):
    message = message
    alpha = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijkmlmnopqestuvwxyz"
    result = ""

    for letter in message:
        if letter in alpha:
            letter_index = (alpha.find(letter) + key) % len(alpha)

            result = result + alpha[letter_index]
        else:
            result = result + letter

    return result


def encrypt(message: str, key: int = 20):
    message = message
    alpha = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijkmlmnopqestuvwxyz"
    result = ""

    for letter in message:
        if letter in alpha:
            letter_index = (alpha.find(letter) - key) % len(alpha)

            result = result + alpha[letter_index]
        else:
            result = result + letter

    return result


if __name__ == '__main__':
    print(encrypt("123salut"))
    print(decrypt("ZGSba123h"))