#Алфавит
ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯABCDEFGHIJKLMNOPQRSTUVWXYZАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'

def encryption(message, step):
    encrypted = []
    for char in message:
        index = ALPHABET.find(char)
        new_index = index + step
        if char in ALPHABET:
            encrypted.append(ALPHABET[new_index])
        else:
            encrypted.append(char)
    return ''.join(encrypted)

def decryption(message, step):
    decrypted = []
    for char in message:
        index = ALPHABET.find(char)
        new_index = index - step
        if char in ALPHABET:
            decrypted.append(ALPHABET[new_index])
        else:
            decrypted.append(char)
    return ''.join(decrypted)

while True:
    step = int(input('Введите шаг шифровки: '))
    if step < len(ALPHABET):
        break
    else:
        print("Неправильное число для сдвига! Повторите попытку!")

message = input('Введите сообщение: ').upper()
result = ''

result = encryption(message, step)

print("ЗАШИФРОВАНО: ", result)
print("РАСШИФРОВАНО: ", decryption(result, step))
