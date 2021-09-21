import getopt, sys
import zlib
import os
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import scrypt
import timeit
import threading
import cProfile
import time
from guppy import hpy


def compress_data(data_block):
    return zlib.compress(data_block)


def decompress_data(data_block):
    return zlib.decompress(data_block)


def encrypt_data(cipher, data_block):
    return cipher.encrypt(data_block)


def decrypt_data(cipher, data_block):
    return cipher.decrypt(data_block)


def return_compressed_encrypted_data_inner(block_size, key):

    try:

        inner_start_time = timeit.timeit()
        data = bytearray(os.urandom(int(block_size)))

        compressed_data = compress_data(data)
        cipher = AES.new(key, AES.MODE_GCM)  # Create a cipher object to encrypt data

        # Read, encrypt and write the data
        data_to_encrypt = compressed_data  # Read in some of the file
        encrypted_data = encrypt_data(cipher, data_to_encrypt)  # Encrypt the data we read
#        tag = cipher.digest()  # Signal to the cipher that we are done and get the tag
        print_heap_stats()
        inner_end_time = timeit.timeit()
        print("Total inner execution time : ", inner_end_time - inner_start_time)

        return encrypted_data

    except getopt.error as err:
        # output error, and return with an error code
        print(str(err))


def return_compressed_encrypted_data(block_size, key):

    try:
        parallel_threads = 96
        threads = []

        for i in range(parallel_threads):
            threads.append(threading.Thread(target=return_compressed_encrypted_data_inner, args=(block_size, key)))

        for i in range(parallel_threads):
            threads[i].start()

        for i in range(parallel_threads):
            threads[i].join()
        #print("Total inner execution time : ", inner_end_time - inner_start_time)


    except getopt.error as err:
        # output error, and return with an error code
        print(str(err))


def generate_return_key():
    password = "pA$sW0rD"
    salt = get_random_bytes(32)  # Generate salt
    # print("Generating key ..")
    key = scrypt(password, salt, key_len=32, N=2 ** 17, r=8, p=1)  # Generate a key using the password and salt
    return key


def print_heap_stats():
    h = hpy()
    print(h.heap())


def trial_func():
    password = "pA$sW0rD"
    print_heap_stats()
    start_time = timeit.timeit()

    salt = get_random_bytes(32)  # Generate salt
    #print("Generating key ..")
    key = generate_return_key()

    time_values = []

    block_size = 1024

    while(block_size <= 1048576):
        t = timeit.repeat(lambda: return_compressed_encrypted_data(block_size, key), number=1, repeat=1)
        print(block_size, t)
        time_values.append(t)
        block_size = block_size * 2

    print_heap_stats()


def main_func():
    password = "pA$sW0rD"
    start_time = timeit.timeit()

    salt = get_random_bytes(32)  # Generate salt
    #print("Generating key ..")
    key = generate_return_key()

    #print("Creating cipher ..")
    return_compressed_encrypted_data(1048576, key)


#
# start_time = timeit.timeit()
# #cProfile.run('main()')
# main()
# end_time = timeit.timeit()
# print("Total inner execution time : ", end_time - start_time)
#