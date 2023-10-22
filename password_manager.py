import hashlib
import random
import codecs
import os

def to_bytes(string):
    return codecs.decode(bytes(string,"utf-8"),"hex")

def to_str(bytes):
    return str(codecs.encode(bytes,"hex"),"utf-8")

def generate_password_hash(password):
    salt = os.urandom(32)
    key = hashlib.pbkdf2_hmac("sha256", password.encode('utf-8'),salt,100000)
    salt = to_str(salt)
    key = to_str(key)
    return f'{salt}-{key}'

def verify_password_hash(password,password_hash):
    salt, saved_key = password_hash.split('-')
    salt = to_bytes(salt)
    password_key = to_str(hashlib.pbkdf2_hmac("sha256", password.encode('utf-8'),salt,100000))
    return saved_key == password_key


if __name__ == "__main__":
    e = generate_password_hash("test")
    print(type(e))
    print(e)
    r = verify_password_hash("test", e)
    print(r)
    r = verify_password_hash("password", e)
    print(r)