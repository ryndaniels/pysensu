#!/usr/bin/env python

import requests

class Pysensu():
    def __init__(self, host, user=None, password=None, port=4567):
        if not host:
            raise ValueError("Cannot create Pysensu object without host")

        self.host = host
        self.user = user
        self.password = password
        self.port = port

        if self.user and self.port:
            self.api_url = "https://{}:{}@{}:{}".format(user, password, host, port)
        elif not self.user and not self.port:
            self.api_url = "http://{}:{}".format(host, port)
        else:
            raise ValueError("Must specify both user and password")

    def _api_call(url, method):
        if method == "post":
            return requests.post(url)
        elif method == "get":
            return requests.get(url)
        elif method == "put":
            return requests.put(url)
        elif method == "delete":
            return requests.delete(url)
        else:
            raise ValueError("Invalid method")

    def create_stash(self, client, check=None):
        if not client:
            raise ValueError("Must specify client to create stash")
        if check:
            r = self._api_call("{}/stashes/{}/{}".format(self.api_url, client, check), "post")
        else:
            r = self._api_call("{}/stashes/{}".format(self.api_url, client), "post")
        if r.status_code != requests.codes.ok:
            raise ValueError("Error creating stash ({})".format(r.status_code))

    def delete_stash(self, client, check=None):
        if not client:
            raise ValueError("Must specify client to delete stash")
        if check:
            r = self._api_call("{}/stashes/{}/{}".format(self.api_url, client, check), "delete")
        else:
            r = self._api_call("{}/stashes/{}".format(self.api_url, client), "delete")
        if r.status_code != requests.codes.ok:
            raise ValueError("Error deleting stash ({})".format(r.status_code))

    def delete_client(self, client):
        if not client:
            raise ValueError("Must specify client to delete")
        r = self._api_call("{}/clients/{}".format(self.api_url, client), "delete")
        if r.status_code != requests.codes.ok:
            raise ValueError("Error deleting client ({})".format(r.status_code))
