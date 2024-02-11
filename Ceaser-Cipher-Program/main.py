'''
Cease Cipher is used to encrypt the message and then decrypt it by passing the certain shift number
'''
from art import logo
def cipher(text,direction, shift):
    staging_index = []
    decrypted_staging_index = []
    encrypted_letter = []
    decrypted_letter = []
    if direction=="encode":
        for i in text:
            if i == " ":
                staging_index.append('-')
            else:
                staging_index.append(int(alphabet.index(i)) + shift%26)
        for i in staging_index:
            if i == "-":
                encrypted_letter.append(' ')
            else:
                encrypted_letter.append(alphabet[i])
        final_encrypted_letter = ''.join(map(str, encrypted_letter))
        print(f"Here is the encoded result: {final_encrypted_letter}")
    elif direction=="decode":
        for i in text:
            if i == " ":
                decrypted_staging_index.append('-')
            else:
                decrypted_staging_index.append(int(alphabet.index(i)) - shift%26)
        for i in decrypted_staging_index:
            if i == "-":
                decrypted_letter.append(' ')
            else:
                decrypted_letter.append(alphabet[i])
        final_decrypted_letter = ''.join(map(str, decrypted_letter))
        print(f"Here is you decoded result is: {final_decrypted_letter}")
    else:
        print("please provide valid options which are 'encode' to encrypt the message and 'decode' to decrypt the message")
print(logo)
alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z','a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
direction = input("Type 'encode' to encrypt, type 'decode' to decrypt:\n")
text = input("Type your message:\n").lower()
shift = int(input("Type the shift number:\n"))
cipher(text=text, direction=direction, shift=shift)
while input("Type 'yes' to go again otherwise type 'no' \n") == "yes":
    direction = input("Type 'encode' to encrypt, type 'decode' to decrypt:\n")
    text = input("Type your message:\n").lower()
    shift = int(input("Type the shift number:\n"))
    cipher(text=text, direction=direction, shift=shift)
# while restart_program=="yes":
#     cipher(text=text, direction=direction, shift=shift)
