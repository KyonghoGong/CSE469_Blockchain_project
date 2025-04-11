# Ensures secure encryption/decryption of UUIDs and IDs using AES.

# Handles AES encryption/decryption.

# encryption.py
from Crypto.Cipher import AES
import base64
import uuid
import struct

# hard coded in your program
AES_KEY = base64.b64decode("R0chLi4uLi4uLi4=")  # This is the base64-encoded key

def pad(data):
    return data + b'\0' * (16 - len(data) % 16)

def encrypt_uuid(uuid_str):
    cipher = AES.new(AES_KEY, AES.MODE_ECB)
    u_bytes = uuid.UUID(uuid_str).bytes
    return cipher.encrypt(pad(u_bytes))

def encrypt_item_id(item_id):
    cipher = AES.new(AES_KEY, AES.MODE_ECB)
    item_bytes = struct.pack('I', item_id) + b'\0' * 12
    return cipher.encrypt(item_bytes)

def decrypt_bytes(data):
    cipher = AES.new(AES_KEY, AES.MODE_ECB)
    decrypted = cipher.decrypt(data)
    return decrypted.rstrip(b'\0')