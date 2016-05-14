from tornado.web import RequestHandler
import tornado.gen as gen
from json import loads, dumps
from http import HTTPStatus
from OpenSSL import crypto
import os
import time
import hashlib
import uuid
from bson.objectid import ObjectId
import base64
import hashlib
from Crypto import Random
from Crypto.Cipher import AES


class BaseHandler(RequestHandler):
    def prepare(self):
        self.db = self.application.db

    def check_passwd(self, salt, new_passwd, passwd):
        hashed_passwd = hashlib.sha512(salt+new_passwd.encode()).hexdigest()
        hashed_passwd2 = hashlib.sha512(hashed_passwd.encode() + salt).hexdigest()
        return hashed_passwd2 == passwd

    def hash_passwd_with_salt(self, passwd):
        salt = os.urandom(self.settings["salt_length"])
        hashed_passwd = hashlib.sha512(salt+passwd.encode()).hexdigest()
        hashed_passwd2 = hashlib.sha512(hashed_passwd.encode() + salt).hexdigest()
        return salt, hashed_passwd2

    def generate_uuid(self):
        return str(uuid.uuid4())

    def generate_recovery_key(self):
        return str(uuid.uuid4())[0:18]

    def generate_rsa_key_pair(self, bits):
        key = crypto.PKey()
        key.generate_key(crypto.TYPE_RSA, bits)
        public_key = crypto.dump_publickey(crypto.FILETYPE_PEM, key).decode()
        private_key = crypto.dump_privatekey(crypto.FILETYPE_PEM, key).decode()
        public_key = public_key.replace("-----BEGIN PUBLIC KEY-----", "")
        public_key = public_key.replace("-----END PUBLIC KEY-----", "")
        public_key = public_key.replace("\n", "")
        private_key = private_key.replace("-----BEGIN PRIVATE KEY-----", "")
        private_key = private_key.replace("-----END PRIVATE KEY-----", "")
        private_key = private_key.replace("\n", "")
        return public_key, private_key

    def encrypt_pri_key(self, plain_pri_key, login_password):
        aes_cipher = AESCipher(login_password)
        cipher_pri_key = aes_cipher.encrypt(plain_pri_key)
        print(plain_pri_key)
        print(cipher_pri_key)
        return cipher_pri_key

    def decrypt_pri_key(self, cipher_pri_key, login_password):
        aes_cipher = AESCipher(login_password)
        plain_pri_key = aes_cipher.decrypt(cipher_pri_key)
        print(cipher_pri_key)
        print(plain_pri_key)
        return plain_pri_key


class AESCipher(object):

    def __init__(self, key):
        self.bs = 32
        tmp = hashlib.sha256(key.encode()).digest()
        self.key = hashlib.sha256(tmp).digest()

    def encrypt(self, raw):
        raw = self._pad(raw)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(raw))

    def decrypt(self, enc):
        enc = base64.b64decode(enc)
        iv = enc[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return self._unpad(cipher.decrypt(enc[AES.block_size:])).decode('utf-8')

    def _pad(self, s):
        return s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)

    @staticmethod
    def _unpad(s):
        return s[:-ord(s[len(s)-1:])]