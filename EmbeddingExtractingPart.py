from cv2 import imread, imwrite
from cryptography.fernet import Fernet
from math import ceil
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend


import base64

#Encryption algorithm for vigenere cipher
def vigenere_encrypt(plaintext, key):
    ciphertext = ''
    key = key.upper()
    key_length = len(key)

    for i, char in enumerate(plaintext):
        if char.isalpha():
            key_char = key[i % key_length]
            shift = ord(key_char) - ord('A')

            if char.isupper():
                encrypted_char = chr((ord(char) + shift - ord('A')) % 26 + ord('A'))
            else:
                encrypted_char = chr((ord(char) + shift - ord('a')) % 26 + ord('a'))

            ciphertext += encrypted_char
        else:
            ciphertext += char
    ciphertext += "="
    return ciphertext

#Decryption algorithm for vigenere cipher
def vigenere_decrypt(ciphertext, key):
    decrypted_text = ''
    key = key.upper()
    key_length = len(key)

    for i, char in enumerate(ciphertext):
        if char.isalpha():
            key_char = key[i % key_length]
            shift = ord(key_char) - ord('A')

            if char.isupper():
                decrypted_char = chr((ord(char) - shift - ord('A')) % 26 + ord('A'))
            else:
                decrypted_char = chr((ord(char) - shift - ord('a')) % 26 + ord('a'))

            decrypted_text += decrypted_char
        else:
            decrypted_text += char
    return decrypted_text

#Key for Vigenere Cipher. number_list is coming from info_position_on_image function. The list has 3 numbers.
#A new key is created according to the positions of the numbers in the list in the alphabet.
def find_vigenere_key(number_list):
    new_key = "" 
    for number in number_list: 
        if number >= 0 and number < 26:
            alfabe = 'abcdefghijklmnopqrstuvwxyz'
            char = alfabe[number]
            new_key += char
        else:
            return "Invalid Char"
    return new_key

#Padding for encryption algorithm
def pad(data, block_size):
    if isinstance(data, str):
        data = data.encode('utf-8')
    padding_value = block_size - (len(data) % block_size)
    return data + bytes([padding_value] * padding_value)

#Unpadding for decryption algorithm
def unpad(data):
    padding_value = data[-1]
    return data[:-padding_value]

#Encryption algorithm using AES in mode CBC
def encrypt(message, key):
    block_size = 16
    key = key.ljust(32, b'\0')
    iv = key[:16]
    backend = default_backend()
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=backend)
    encryptor = cipher.encryptor()
    cipher_text = encryptor.update(pad(message, block_size)) + encryptor.finalize()
    return cipher_text

#Decryption algorithm according to encryption algorithm
def decrypt(cipher_text, key):
    key = key.ljust(32, b'\0')
    iv = key[:16]
    backend = default_backend()
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=backend)
    decryptor = cipher.decryptor()
    decrypted_data = decryptor.update(cipher_text) + decryptor.finalize()
    return unpad(decrypted_data)

#Generates key for encryption algorithm AES mode CBC
def generate_key():
    fernet_key = Fernet.generate_key()
    aes_key_256_bits = fernet_key[:32]
    return aes_key_256_bits

#Finds the key positions on image. 
#Quarter is the 16. quarter on the image. (15. index)
def key_position_on_img(quarter):
    key_positions = []
    index = 0
    while len(key_positions) < 4 and index < len(quarter):
        current_value = quarter[index] % 5 + 10 #The value must be between 10,14 because those quarters are empty.
        if current_value not in key_positions:
            key_positions.append(current_value)
        index += 1
    return key_positions

#Finds the information positions on img.
def info_position_on_img(key):
    sum = 0
    for char in key:
        sum += ord(char)
    value = sum 
    while not (len(set(str(value))) == len(str(value))): #For the numbers to be different from each other.
        value += 1
    digits = [int(digit) for digit in str(value)]
    return digits[1:4]

#LSB extraction from image
def LSB_extraction(quarter):
    return ''.join(str(pixel & 1) for pixel in quarter)

def convert_text_to_binary(img_size, text):
    binary_text = ''.join(format(ord(char), '08b') for char in text)
    if len(binary_text) > img_size:
        raise ValueError("Text is too long to be hidden in the image")
    return binary_text

def convert_binary_to_text(binary_text):
    text = ''.join(chr(int(binary_text[i:i+8], 2)) for i in range(0, len(binary_text), 8))
    return text

#Divides the image into 16 parts
def find_quarters(img, height, width):
    quarters = []
    rng = 4
    for i in range(rng):
        for j in range(rng):
            quarter = img[i * height // 4:(i + 1) * height // 4, j * width // 4:(j + 1) * width // 4].flatten()
            quarters.append(quarter)
    return quarters

#It allows converting texts to binary and then keeping them as a list.
def text_to_binary_list(img, encrypted_list):
    binary_list = []
    img_size = img.size
    for text in encrypted_list:
        binary_text = convert_text_to_binary(img_size, text)
        binary_list.append(binary_text)
    return binary_list

#Divides the key by the specified number of parts
def divide_key_to_parts(encryption_key):
    parts_number = 4
    part_length = ceil(len(encryption_key) / parts_number)
    parts = [encryption_key[i:i+part_length] for i in range(0, len(encryption_key), part_length)]

    divided_parts = [part + "=" for part in parts]
    return divided_parts

#Using LSB technique to embed informations on image and generates the new image.
def embedding_part(quarters, binary_list, img, positions):
    height, width, _ = img.shape
    text_index = 0
    for k in positions:
        if text_index == len(binary_list):
            break
        text = binary_list[text_index]
        for i in range(len(binary_list[text_index])):
            quarter = quarters[k]

            quarter[i] = (quarter[i] & 0b11111110) | int(text[i])
            if len(text) > quarter.size:
                raise ValueError("Text is too long to be hidden in the image")
        text_index += 1

    for i in range(4):
        for j in range(4):
            x = ((i + 1) * height // 4) - (i * height // 4)
            y = ((j + 1) * width // 4) - (j * width // 4)
            img[i * height // 4:(i + 1) * height // 4, j * width // 4:(j + 1) * width // 4] = \
                quarters[i * 4 + j].reshape((x, y, -1))
    return img

#All encryption and embedding operations.
def embedding_to_img(image_path, info):
    img = imread(image_path)
    height, width, _ = img.shape
    quarters = find_quarters(img, height, width)
    encryption_key = generate_key()
    positions = info_position_on_img(encryption_key.decode())
    key_positions = key_position_on_img(quarters[15])
    encryption_key_divided = divide_key_to_parts(encryption_key.decode())
    encryption_key_divided_binary_list = text_to_binary_list(img, encryption_key_divided)
    binary_key = convert_text_to_binary(img.size, encryption_key.decode())
    binary_list = []
    vigenere_key = find_vigenere_key(positions)
    for key in info:
        if(key == "name" or key == "surname"):
            encrypted_text = vigenere_encrypt(info[key], vigenere_key)
            binary_text = convert_text_to_binary(img.size, encrypted_text)
        else:
            encrypted_text = encrypt(info[key], encryption_key)
            encrypted_text = base64.b64encode(encrypted_text).decode('utf-8')
            binary_text = convert_text_to_binary(img.size, encrypted_text)
        binary_list.append(binary_text)
    binary_list += encryption_key_divided_binary_list
    positions += key_positions
    new_img = embedding_part(quarters, binary_list, img, positions)
    print("Embedding Completed!")
    return new_img

#Extract key from image.
def extract_key(quarters, key_positions):
    key = ""
    for i in key_positions:
        binary_text = LSB_extraction(quarters[i])
        decoded_text = convert_binary_to_text(binary_text)
        key += decoded_text.split('=', 1)[0]
    return key


def extract_name_surname(binary_text):
    decoded_text = convert_binary_to_text(binary_text)
    decoded_text = decoded_text.split('=', 1)[0]
    return decoded_text

def extract_tcno(binary_text):
    decoded_text = convert_binary_to_text(binary_text[0:192])
    return decoded_text

#Saving decrypted information as a dictionary format.
def save_as_dictionary(info_list):
    info = {"name": "", "surname": "", "tcno": ""}
    for i, key in zip(info_list,info):
        info[key] = i
        print(key.capitalize() + ": " + info[key])
    return info

#Extraction and Decryption operations.
def extracting_embedded_data(image_path):
    img = imread(image_path)
    height, width, _ = img.shape
    quarters = find_quarters(img, height, width)
    key_positions = key_position_on_img(quarters[15])
    key = extract_key(quarters, key_positions)
    positions = info_position_on_img(key)
    vigenere_key = find_vigenere_key(positions)
    extracted_info = []
    count = 0
    for i in positions:
        quarter = quarters[i]
        if(count!=2):
            binary_text = LSB_extraction(quarter)
            decoded_text = extract_name_surname(binary_text)
            decrypted_text = vigenere_decrypt(decoded_text, vigenere_key)
        else:
            binary_text = LSB_extraction(quarter)
            decoded_text = extract_tcno(binary_text)
            decoded_text = base64.b64decode(decoded_text)
            decrypted_text = decrypt(decoded_text, key.encode('utf-8')).decode()
        extracted_info.append(decrypted_text)
        count += 1
    return save_as_dictionary(extracted_info)

#Running encryption and embedding part
def run_embedding():    
    info_to_hide = {"name": "Alperen", 
                    "surname": "Cavusoglu", 
                    "tcno": "123456789123"}
    
    image_path = "Embedding_Images/1.jpg"
    output_path = "Extracting_Images/embedded_img.png"
    new_img = embedding_to_img(image_path, info_to_hide)
    imwrite(output_path, new_img)
    
#Running extractiong and decryption part
def run_extraction():
    output_path = "Extracting_Images/embedded_img.png"
    extracted_info = extracting_embedded_data(output_path)

#Printing the running functions
#print("Embedding Part")
#run_embedding()
#print("Extractin Part")
#run_extraction()