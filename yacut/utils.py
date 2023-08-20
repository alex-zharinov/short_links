import random
import string


def get_unique_short_id(LEN):
    keylist = [random.choice(string.ascii_letters + string.digits) for i in range(LEN)]
    return ("".join(keylist))
