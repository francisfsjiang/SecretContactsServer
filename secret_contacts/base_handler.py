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


class BaseHandler(RequestHandler):
    def prepare(self):
        self.db = self.application.db

    def check_passwd(self, salt, new_passwd, passwd):
        hashed_passwd = hashlib.sha512(salt+new_passwd.encode()).hexdigest()
        return hashed_passwd == passwd

    def hash_passwd_with_salt(self, passwd):
        salt = os.urandom(self.settings["salt_length"])
        hashed_passwd = hashlib.sha512(salt+passwd.encode()).hexdigest()
        return salt, hashed_passwd

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

