import random
import string

def random_id():
    characters = string.ascii_lowercase + string.digits
    return ''.join(random.choices(characters, k=16))










if __name__ == '__main__':
    print(random_id())
    print('done...')