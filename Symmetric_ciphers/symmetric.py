import math, random, datetime, hashlib

#OTP generation
#при вызове функции возвращается сгенерироанный пароль

def generateOTP():
    string = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    OTP = ""
    length = len(string)
    for i in range(6):
        OTP += string[math.floor(random.random() * length)]
    return OTP

#Blockchain
#класс для использования в технологии блокчейн

class Block:

    def __init__(self, index, timestamp, data, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.hash_block()

    def hash_block(self):
        sha = hashlib.sha256()
        tm = str(self.timestamp)
        sha.update((str(self.index) + tm + str(self.data) + str(self.previous_hash)).encode('utf-8'))
        return sha.hexdigest()

def create_genesis_block():
 return Block(0, datetime.datetime.now(), "Genesis Block", "0")

def next_block(last_block):
    this_index = last_block.index + 1
    this_timestamp = datetime.datetime.now()
    this_data = "Hey! I'm block " + str(this_index)
    this_hash = last_block.hash
    return Block(this_index, this_timestamp, this_data, this_hash)

#Feistel network

ROUNDS = 16
KEY = 'Abcdefg'
text = 'Hello programming world'
block = []
key_pos = 0
if len(text) % 2 != 0 :
    text = text +' '
for i in range(0, len(text), 2):
    block.append(text[i:i + 2])

def festel(L,R,key_pos):
    for i in range(ROUNDS):
        k = ord(KEY[key_pos % 7::][0])
        temp = R ^ (L ^ k)
        R = L
        L = temp
        key_pos += 1
        end = (chr(R) + chr(L))
    return end,key_pos

def festel_decript(L,R, key_pos):
    for i in range(ROUNDS):
        K = ord(KEY[key_pos % 7::][0])
        temp = R ^ (L ^ K)
        R = L
        L = temp
        key_pos -= 1
        end = (chr(L) + chr(R))
    return end, key_pos

print('\nШифруем\n')
shifr = []
for x in block:
    block,key_pos = festel(ord(x[0]), ord(x[1]), key_pos)
    shifr.append(block)

print(''.join(shifr))

print('\nДешифруем\n')

defshifr=[]

key_pos -= 1

for x in shifr[::-1]:
    block,key_pos = festel_decript(ord(x[0]), ord(x[1]), key_pos)
    defshifr.append(block)
    defshifr1 = ''.join(defshifr)
print(defshifr1[::-1])
