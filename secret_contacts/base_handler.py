from tornado.web import RequestHandler
import tornado.gen as gen
from json import loads, dumps
from http import HTTPStatus
from OpenSSL import crypto
import os
import time
import hashlib
import uuid


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

    def get_uuid(self):
        return str(uuid.uuid4())

    def generate_rsa_key_pair(self, bits):
        key = crypto.PKey()
        key.generate_key(crypto.TYPE_RSA, bits)
        public_key = str(crypto.dump_publickey(crypto.FILETYPE_PEM, key))
        private_key = str(crypto.dump_privatekey(crypto.FILETYPE_PEM, key))
        return public_key, private_key

