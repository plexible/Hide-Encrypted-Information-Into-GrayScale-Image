from cv2 import imread, imwrite
from cryptography.fernet import Fernet
from math import ceil

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

def generate_key():
    return Fernet.generate_key()

def encrypt(data, key):
    cipher = Fernet(key)
    encrypted_data = cipher.encrypt(data.encode())
    return encrypted_data

def decrypt(encrypted_data, key):
    cipher = Fernet(key)
    decrypted_data = cipher.decrypt(encrypted_data.encode()).decode()
    return decrypted_data

def key_position_on_img(quarter):
    key_positions = []
    index = 0
    while len(key_positions) < 4 and index < len(quarter):
        current_value = quarter[index] % 5 + 10
        if current_value not in key_positions:
            key_positions.append(current_value)
        index += 1
    return key_positions

def info_position_on_img(key):
    sum = 0
    for char in key:
        sum += ord(char)
    value = sum
    while not (len(set(str(value))) == len(str(value))):
        value += 1
    digits = [int(digit) for digit in str(value)]
    return digits[1:4]

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

def find_quarters(img, height, width):
    quarters = []
    rng = 4
    for i in range(rng):
        for j in range(rng):
            quarter = img[i * height // 4:(i + 1) * height // 4, j * width // 4:(j + 1) * width // 4].flatten()
            quarters.append(quarter)
    return quarters

def text_to_binary_list(img, encrypted_list):
    binary_list = []
    img_size = img.size
    for text in encrypted_list:
        binary_text = convert_text_to_binary(img_size, text)
        binary_list.append(binary_text)
    return binary_list

def divide_key_to_parts(encryption_key):
    parts_number = 4
    part_length = ceil(len(encryption_key) / parts_number)
    parts = [encryption_key[i:i+part_length] for i in range(0, len(encryption_key), part_length)]

    divided_parts = [part + "=" for part in parts[:-1]] + [parts[-1]]
    return divided_parts

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
            binary_text = convert_text_to_binary(img.size, encrypted_text.decode())
        binary_list.append(binary_text)
    binary_list += encryption_key_divided_binary_list
    positions += key_positions
    new_img = embedding_part(quarters, binary_list, img, positions)
    print("Embedding Completed!")
    return new_img

def extract_key(quarters, key_positions):
    key = ""
    for i in key_positions:
        binary_text = LSB_extraction(quarters[i])
        decoded_text = convert_binary_to_text(binary_text)
        key += decoded_text.split('=', 1)[0]
    key += "="
    return key

def extract_name_surname(binary_text):
    decoded_text = convert_binary_to_text(binary_text)
    decoded_text = decoded_text.split('=', 1)[0]
    return decoded_text

def extract_tcno(binary_text):
    decoded_text = convert_binary_to_text(binary_text[0:800])
    return decoded_text

def save_as_dictionary(info_list):
    info = {"name": "", "surname": "", "tcno": ""}
    for i, key in zip(info_list,info):
        info[key] = i
        print(key.capitalize() + ": " + info[key])
    return info

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
            decrypted_text = decrypt(decoded_text, key)
        extracted_info.append(decrypted_text)
        count += 1
    return save_as_dictionary(extracted_info)

def run_embedding():    
    info_to_hide = {"name": "Alperen", 
                    "surname": "Cavusoglu", 
                    "tcno": "123456789123"}
    
    image_path = "Embedding_Images/1.jpg"
    output_path = "Extracting_Images/embedded_img.png"
    new_img = embedding_to_img(image_path, info_to_hide)
    imwrite(output_path, new_img)

def run_extraction():
    output_path = "Extracting_Images/embedded_img.png"
    extracted_info = extracting_embedded_data(output_path)

print("Embedding Part")
run_embedding()
print("Extractin Part")
run_extraction()