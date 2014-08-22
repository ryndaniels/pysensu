#!/usr/bin/env python

import json
import requests


class Pysensu():
    def __init__(self, host, user=None, password=None, port=4567, ssl=False):
        self.host = host
        self.user = user
        self.password = password
        self.port = port
        self.ssl = ssl
        self.api_url = self._build_api_url(host, user, password, port, ssl)

    def _build_api_url(self, host, user, password, port, ssl):
        if ssl == True:
            protocol = 'https'
        else:
            protocol = 'http'
        if user and password:
            credentials = "{}:{}@".format(user, password)
        elif (user and not password) or (password and not user):
            raise ValueError("Must specify both user and password, or neither")
        else:
            credentials = ""
        return "{}://{}{}:{}".format(protocol, credentials, host, port)

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
        return r.json()

    def get_client(self, client):
        r = self._api_call("{}/clients/{}".format(self.api_url, client), "get")
        if r.status_code != requests.codes.ok:
            raise ValueError("Error getting client ({})".format(r.status_code))
        return r.json()

    def get_all_clients(self):
        r = self._api_call("{}/clients".format(self.api_url), "get")
        if r.status_code != requests.codes.ok:
            raise ValueError("Error getting clients ({})".format(r.status_code))
        return r.json()

    def get_all_stashes(self):
        r = self._api_call("{}/stashes".format(self.api_url), "get")
        if r.status_code != requests.codes.ok:
            raise ValueError("Error getting stashes ({})".format(r.status_code))
        return r.json()

    def get_check(self, check):
        r = self._api_call("{}/checks/{}".format(self.api_url, check), "get")
        if r.status_code != requests.codes.ok:
            raise ValueError("Error getting check ({})".format(r.status_code))
        return r.json()

    def get_all_checks(self):
        r = self._api_call("{}/checks".format(self.api_url), "get")
        if r.status_code != requests.codes.ok:
            raise ValueError("Error getting checks ({})".format(r.status_code))
        return r.json()

    def request_check(self, check, subscribers):
        data = {
            "check": check,
            "subscribers": subscribers
        }
        r = self._api_call("{}/check/request".format(self.api_url), "post", json.dumps(data))
        if r.status_code != requests.codes.accepted:
            raise ValueError("Error requesting check ({}, {})".format(r.status_code, r.json))

    def get_all_events(self):
        r = self._api_call("{}/events".format(self.api_url), "get")
        if r.status_code != requests.codes.ok:
            raise ValueError("Error getting events ({})".format(r.status_code))
        return r.json()

    def get_all_client_events(self, client):
        r = self._api_call("{}/events/{}".format(self.api_url, client), "get")
        if r.status_code != requests.codes.ok:
            raise ValueError("Error getting client events ({})".format(r.status_code))
        return r.json()

    def get_event(self, client, check):
        r = self._api_call("{}/events/{}/{}".format(self.api_url, client, check), "get")
        if r.status_code != requests.codes.ok:
            raise ValueError("Error getting event ({})".format(r.status_code))
        return r.json()

    def delete_event(self, client, check):
        r = self._api_call("{}/events/{}/{}".format(self.api_url, client, check), "delete")
        if r.status_code != requests.codes.accepted:
            raise ValueError("Error deleting event ({})".format(r.status_code))

    def resolve_event(self, client, check):
        data = {
            "client": client,
            "check": check
        }
        r = self._api_call("{}/event/resolve".format(self.api_url), "post", json.dumps(data))
        if r.status_code != requests.codes.accepted:
            raise ValueError("Error getting client({})".format(r.status_code))
