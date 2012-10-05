import requests
import base64
import json
import sys
from functools import partial
import logging

logging.basicConfig(level=logging.DEBUG)

def encode_credentials(credentials):
    return base64.b64encode('{0}:{1}'.format(credentials['user'], credentials['password']))

def http(method, url, credentials, data=None):
    credentials = encode_credentials(credentials)
    headers = {}
    headers['Authorization'] = 'Basic {0}'.format(credentials)
    headers['Content-Type'] = 'application/json'
    method = getattr(requests, method)
    params = {'headers': headers}
    if data:
        params['data'] = json.dumps(data)

    params['config'] = {'verbose': sys.stderr}
    return method(url, **params)

http_get = partial(http, 'get')
http_post = partial(http, 'post')

class User(dict):
    def __init__(self, url, credentials):
        self.url = url
        self.credentials = credentials

    def init(self):
        obj = User(self.url, self.credentials)
        return obj

    def save(self):
        print 'hola'

class Organization(dict):
    def __init__(self, url, credentials):
        self.url = url
        self.credentials = credentials

    def init(self, name):
        obj = Organization(self.url, self.credentials)
        obj.name = name
        return obj

    def __call__(self, organization):
        response = http_get(self.url + '/organizations_{0}'.format(organization), self.credentials)
        response = json.loads(response.content) if response.content else None
        return response

    @property
    def name(self):
        return self._id

    @name.setter
    def name(self, name):
        self._id = name

    def save(self):
        data = dict(self.items())
        data['_id'] = "organizations_{0}".format(self.name)
        response = http_post(self.url, self.credentials, data=data)
        response = json.loads(response.content) if response.content else None
        return response


class Client(object):

    def __init__(self, url, user, password):
        self.url = url
        self.credentials = {'user': user, 'password': password}
        self._user_client = User(self.url, self.credentials)
        self._organization_client = Organization(self.url, self.credentials)

    @property
    def user(self):
        return self._user_client

    @property
    def organization(self):
        return self._organization_client

if __name__ == '__main__':
    url = 'https://juandebravo.cloudant.com/hackaton'
    user = 'juandebravo'
    password = 'hackaton'
    client = Client(url, user, password)
    #organization = client.organization('prueba_juan')
    #print organization
    
    ORGANIZATIONS = ('telefonicaid', )
    
    for org in ORGANIZATIONS:
        organization = client.organization.init(org)
        organization["users"] = [{"login": u"juandebravo",
                                  "points": 30,
                                  "rank": 1,
                                  "badges": [
                                    {u"padowan": "20121002"},
                                    {u"adventurer": "20121001"}]
                                },
                                {"login": u"jegumi",
                                  "points": 10,
                                  "rank": 3,
                                  "badges": [
                                    {u"pringao": "20121002"}]
                                },
                                {"login": u"fran",
                                  "points": 28,
                                  "rank": 2,
                                  "badges": [
                                    {u"padowan": "20121002"},
                                    {u"adventurer": "20121001"}]
                                }]

        print organization.save()
