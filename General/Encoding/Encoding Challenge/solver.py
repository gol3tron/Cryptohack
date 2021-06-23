from pwn import * # pip install pwntools
import json
import codecs
from Crypto.Util.number import bytes_to_long
from Crypto.Util.number import long_to_bytes

r = remote('socket.cryptohack.org', 13377, level = 'debug')

def json_recv():
    line = r.recvline()
    return json.loads(line.decode())

def json_send(hsh):
    request = json.dumps(hsh).encode()
    r.sendline(request)

def decode(input, encoding):
    if encoding == "base64":
        decoded = b64d(input+'==').decode()
    elif encoding == "hex":
        decoded = unhex(input).decode()
    elif encoding == "rot13":
        decoded = codecs.decode(input, 'rot_13')
    elif encoding == "bigint":
        decoded = unhex(input[2::]).decode()
    elif encoding == "utf-8":
        decoded = ''.join([chr(i) for i in input])
    return decoded


i = 0

while(True):

    i += 1
    print("starting level "+str(i))
    received = json_recv()

    if "flag" in received:
        print("the flag is "+received["flag"])
        break
    else:
        print("Received type: ")
        print(received["type"])
        encoding = received["type"]

        print("Received encoded value: ")
        print(received["encoded"])
        encoded = received["encoded"]

        to_send = {"decoded": decode(encoded, encoding)}
    
        json_send(to_send)
    




