from tornado.web import RequestHandler
import tornado.gen as gen
from json import loads, dumps
from http import HTTPStatus
import os
import hashlib

class BaseHandler(RequestHandler):
    def prepare(self):
        self.db = self.application.db

    def check_passwd(self, salt, new_passwd, passwd):
        hashed_passwd = hashlib.sha512(salt+new_passwd.encode()).hexdigest()
        return hashed_passwd == passwd

    def hash_passwd_with_salt(self, passwd):
        salt = os.urandom(self.settings["salt_length"])
        hashed_passwd = hashlib.sha512(salt+passwd.encode()).hexdigest()
        return salt,hashed_passwd
