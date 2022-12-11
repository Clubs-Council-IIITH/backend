import secrets
import sys
import string
import random


def private(num, symbols):
    if num == -1:
        num = random.randint(15, 60)

    s = ''
    letters = string.ascii_letters + string.digits + string.punctuation
    for i in range(num):
        s += secrets.choice(letters)
    s = secrets.choice(string.ascii_lowercase) + secrets.choice(string.punctuation) + \
        secrets.choice(string.ascii_uppercase) + \
        secrets.choice(string.digits) + s

    n = 0
    for i in s:
        n += int(i in string.punctuation)

    while n < symbols:
        n += 1
        s += secrets.choice(string.punctuation)

    random.shuffle(list(s))

    return "".join(s)


if __name__ == '__main__':
    num = 60
    symbols = 6
    if len(sys.argv) == 2:
        num = int(sys.argv[1])
    elif len(sys.argv) == 3:
        num = int(sys.argv[1])
        symbols = int(sys.argv[2])

    print(private(num, symbols))
