def alfabe(key):
    alphabet = "abcçdefgğhıijklmnoöprsştuüvyz"
    new = ""
    for i in range(len(alphabet)):
        x = (i+key) % 29
        y = alphabet[x]
        new = new + y
    return new

def decode(key,message):
    decoded = ""
    for i in range(len(message)):
        if message[i] in new_alphabet:
            index = new_alphabet.find(message[i])
            decoded = decoded + new_alphabet[(index-key) % 29]
        else:
            decoded = decoded + message[i]
    print(decoded)

while True:
    key = input("Enter shift number: ")
    if key.isnumeric():
        key = int(key)
        break

new_alphabet = alfabe(key)
print(new_alphabet)
decode(key,'ogşiyzy fyöay')
