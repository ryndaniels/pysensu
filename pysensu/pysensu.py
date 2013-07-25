#!/usr/bin/env python

import requests


class Pysensu():
    def __init__(self, host, user=None, password=None, port=4567):
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

    def _api_call(self, url, method, data=None):
        if method == "post":
            return requests.post(url, data=data)
        elif method == "get":
            return requests.get(url, data=data)
        elif method == "put":
            return requests.put(url, data=data)
        elif method == "delete":
            return requests.delete(url, data=data)
        else:
            raise ValueError("Invalid method")

    def create_stash(self, client, check=None):
        if check:
            r = self._api_call("{}/stashes/{}/{}".format(self.api_url, client, check), "post", "{}")
        else:
            r = self._api_call("{}/stashes/{}".format(self.api_url, client), "post", "{}")
        if r.status_code != requests.codes.created:
            raise ValueError("Error creating stash ({})".format(r.status_code))

    def delete_stash(self, client, check=None):
        if check:
            r = self._api_call("{}/stashes/{}/{}".format(self.api_url, client, check), "delete")
        else:
            r = self._api_call("{}/stashes/{}".format(self.api_url, client), "delete")
        if r.status_code != requests.codes.no_content:
            raise ValueError("Error deleting stash ({})".format(r.status_code))

    def delete_client(self, client):
        r = self._api_call("{}/clients/{}".format(self.api_url, client), "delete")
        if r.status_code != requests.codes.accepted:
            raise ValueError("Error deleting client ({})".format(r.status_code))

    def get_client_history(self, client):
        r = self._api_call("{}/clients/{}/history".format(self.api_url, client), "get")
        if r.status_code != requests.codes.ok:
            raise ValueError("Error getting client history ({})".format(r.status_code))
        return r.json

    def get_client(self, client):
        r = self._api_call("{}/clients/{}".format(self.api_url, client), "get")
        if r.status_code != requests.codes.ok:
            raise ValueError("Error getting client ({})".format(r.status_code))
        return r.json

    def get_all_clients(self):
        r = self._api_call("{}/clients".format(self.api_url), "get")
        if r.status_code != requests.codes.ok:
            raise ValueError("Error getting clients ({})".format(r.status_code))
        return r.json

    def get_all_stashes(self):
        r = self._api_call("{}/stashes".format(self.api_url), "get")
        if r.status_code != requests.codes.ok:
            raise ValueError("Error getting stashes ({})".format(r.status_code))
        return r.json

    def get_check(self, check):
        r = self._api_call("{}/checks/{}".format(self.api_url, check), "get")
        if r.status_code != requests.codes.ok:
            raise ValueError("Error getting check ({})".format(r.status_code))
        return r.json

    def get_all_checks(self):
        r = self._api_call("{}/checks".format(self.api_url), "get")
        if r.status_code != requests.codes.ok:
            raise ValueError("Error getting checks ({})".format(r.status_code))
        return r.json

    def request_check(self, check, subscribers):
        # TODO: Fix this, it currently 400s :(
        data = {
            "check": check,
            "subscribers": subscribers
        }
        r = self._api_call("{}/check/request".format(self.api_url), "post", data="{}".format(data))
        if r.status_code != requests.codes.accepted:
            raise ValueError("Error requesting check ({}, {})".format(r.status_code, r.json))

    def get_all_events(self):
        r = self._api_call("{}/events".format(self.api_url), "get")
        if r.status_code != requests.codes.ok:
            raise ValueError("Error getting events ({})".format(r.status_code))
        return r.json

    def get_all_client_events(self, client):
        r = self._api_call("{}/events/{}".format(self.api_url, client), "get")
        if r.status_code != requests.codes.ok:
            raise ValueError("Error getting client events ({})".format(r.status_code))
        return r.json

    def get_event(self, client, check):
        r = self._api_call("{}/events/{}/{}".format(self.api_url, client, check), "get")
        if r.status_code != requests.codes.ok:
            raise ValueError("Error getting event ({})".format(r.status_code))
        return r.json

    def delete_event(self, client, check):
        r = self._api_call("{}/events/{}/{}".format(self.api_url, client, check), "delete")
        if r.status_code != requests.codes.accepted:
            raise ValueError("Error deleting event ({})".format(r.status_code))

    def resolve_event(self, client, check):
        # TODO: Fix this
        data = {
            "client": client,
            "check": check
        }
        r = self._api_call("{}/event/resolve".format(self.api_url), "post", data=data)
        if r.status_code != requests.codes.accepted:
            raise ValueError("Error getting client({})".format(r.status_code))
