import random

def get_random(length=10):
    chars='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    s=''
    for i in range(length):
        s+=chars[random.randint(0,len(chars)-1)]
    return s