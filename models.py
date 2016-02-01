import uuid
import json
from flask.ext.redis import FlaskRedis

db = FlaskRedis()


class BadFieldException(BaseException):
    pass


class NotFoundException(BaseException):
    pass


class TTLDBaseModel(object):

    __key_pattern__ = 'nothing'
    __fields__ = []
    __blacklist__ = ['_meta']

    _doc = {}

    def __init__(self, *args, **kwargs):
        pass

    def _hasfield(self, key):
        return key in self.__fields__ and key not in self.__blacklist__

    def __setitem__(self, key, val):
        if self._hasfield(key):
            self._doc[key] = val
        else:
            raise BadFieldException

    def __getitem__(self, key):
        if self._hasfield(key):
            return self._doc[key]
        else:
            raise BadFieldException

    def __delitem__(self, key):
        if self._hasfield(key):
            del self._doc[key]
        else:
            raise BadFieldException

    @classmethod
    def get(cls, **kwargs):
        try:
            _key = cls.__key_pattern__.format(**kwargs)
        except KeyError:
            raise Exception('Missing something value for fill key pattern')
        _doc = db.get(_key)
        if _doc:
            _doc = json.loads(_doc)
            if _doc['_meta']['classname'] != cls.__name__:
                raise Exception('Invalid class')
            del _doc['_meta']
            rv = cls(**_doc)
            rv._doc = _doc
            return rv
        else:
            raise NotFoundException

    def getitem(self, key, default=None):
        if self._hasfield(key):
            try:
                return self._doc[key]
            except KeyError:
                return default
        else:
            raise BadFieldException

    def save(self):
        try:
            _key = self.__key_pattern__.format(**self._doc)
        except KeyError:
            raise Exception('Missing something value for fill key pattern')
        _doc = self._doc.copy()
        _doc['_meta'] = {
            'classname': self.__class__.__name__
        }
        db.set(_key, json.dumps(_doc))


class User(TTLDBaseModel):

    __key_pattern__ = 'users:{id}'
    __fields__ = ['id', 'email', 'username']

    _email_to_uid_key = 'username.to.id:{email}'

    def __init__(self, email, *arg, **kwargs):
        super(User, self).__init__(*arg, **kwargs)
        if not email:
            raise Exception('Email cannot be empty')
        self['id'] = str(uuid.uuid1())
        self['email'] = email

    @classmethod
    def get_user_by_email(cls, email):
        uid = db.get(cls._email_to_uid_key.format(email=email))
        if not uid:
            return None
        else:
            try:
                return cls.get(id=uid)
            except NotFoundException:
                return None

    def save(self):
        super(User, self).save()
        db.set(self._email_to_uid_key.format(email=self['email']), self['id'])
