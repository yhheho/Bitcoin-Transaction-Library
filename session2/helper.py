import hashlib


BASE58_ALPHABET = b'123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'


def bytes_to_str(b, encoding='ascii'):
    """Returns a string version fo the bytes"""
    return b.decode(encoding)


def str_to_bytes(s, encoding='ascii'):
    """Returns a bytes version of the string"""
    return s.encode(encoding)


def little_endian_to_int(b):
    return int.from_bytes(b, 'little')


def int_to_little_endian(n, length):
    return n.to_bytes(length, 'little')


def hash160(s):
    return hashlib.new('ripemd160', hashlib.sha256(s).digest()).digest()


def double_sha256(s):
    return hashlib.sha256(hashlib.sha256(s).digest()).digest()


def encode_base58(s):
    count = 0
    for c in s:
        if c == 0:
            count += 1
        else:
            break

    prefix = b'1' * count
    num = int(s.hex(), 16)
    result = bytearray()
    while num > 0:
        num, mod = divmod(num, 58)
        result.insert(0, BASE58_ALPHABET[mod])

    return prefix + bytes(result)



