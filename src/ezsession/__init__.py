import requests
import json
import base64
from requests.auth import HTTPBasicAuth, HTTPDigestAuth


def get_session(**auth):
    session = requests.Session()
    session = session
    session.headers = {"Content-Type": "application/json", "Accept": "application/json"}
    input_keys = [
        "auth_uri",
        "client_id",
        "client_secret",
        "audience",
        "username",
        "password",
        "type",
        "api_key",
        "scope",
    ]
    print(auth)
    if "auth" in auth:
        auth.update(**auth["auth"])
        del auth["auth"]
    if auth != None:
        if auth["type"] == "digest":
            session.auth = HTTPDigestAuth(auth["username"], auth["password"])
        elif auth["type"] == "oauth":
            body = {
                "client_id": auth["client_id"],
                "client_secret": auth["client_secret"],
                "audience": auth["audience"],
                "grant_type": "client_credentials"
                if "grant_type" not in auth
                else auth["grant_type"],
                "scope": "*" if "scope" not in auth else auth["scope"],
            }
            response = requests.post(auth["auth_uri"], data=body)
            auth = response.json()
            session.headers = {
                "Authorization": auth["token_type"] + " " + auth["access_token"],
                "Content-Type": "application/json",
                "Accept": "application/json",
            }
        elif auth["type"] == "oauth_basic":
            body = {
                "username": auth["username"],
                "password": auth["password"],
                "grant_type": "password",
            }
            response = requests.post(
                auth["auth_uri"],
                data=body,
                headers={"Content-Type": "application/x-www-form-urlencoded"},
                auth=("public-client", "public"),
            )
            response.raise_for_status()
            auth = response.json()
            session.headers = {
                "Authorization": auth["token_type"] + " " + auth["access_token"],
                "Content-Type": "application/json",
                "Accept": "application/json",
            }
        elif auth["type"] == "oauth_password":
            msg = base64.b64encode(
                bytes(auth["client_id"] + ":" + auth["client_secret"], "utf-8")
            )
            headers = {
                "Accept": "application/json",
                "Content-Type": "application/x-www-form-urlencoded",
                "Authorization": "Basic " + str(msg.decode("utf-8")),
            }
            body = {
                "username": auth["username"],
                "password": auth["password"],
                "grant_type": "password",
                "scope": "*",
            }
            response = requests.post(auth["auth_uri"], data=body, headers=headers)
            response.raise_for_status()
            auth = response.json()
            session.headers = {
                "Authorization": auth["token_type"] + " " + auth["access_token"],
                "Content-Type": "application/json",
                "Accept": "application/json",
                "scope": "*",
            }
        elif auth["type"] == "basic":
            if "auth_uri" in auth:
                response = session.get(
                    auth["auth_uri"],
                    auth=HTTPBasicAuth(
                        username=auth["username"],
                        password=auth["password"],
                    ),
                )
            else:
                msg = base64.b64encode(
                    bytes(auth["username"] + ":" + auth["password"], "utf-8")
                )
                session.headers.update(
                    {"Authorization": "Basic " + str(msg.decode("ascii"))}
                )
        elif auth["type"] == "bearer":
            session.headers.update({"Authorization": "Bearer " + auth["api_key"]})
        elif auth["type"] == "ApiToken":
            session.headers.update({"Authorization": f"ApiToken {auth['api_key']}"})
        elif auth["type"] == "dell":
            credentials = f"{auth['client_id']}:{auth['client_secret']}".encode()
            basic_auth = base64.b64encode(credentials).decode()
            auth_request = requests.post(
                auth["auth_uri"],
                headers={"Authorization": f"Basic {basic_auth}"},
                data={"grant_type": "client_credentials"},
            ).json()
            session.headers = {
                "Authorization": auth_request["token_type"]
                + " "
                + auth_request["access_token"],
                "Content-Type": "application/json",
                "Accept": "application/json",
            }
        else:
            # Delete auth type
            if "type" in auth:
                del auth["type"]
            session.headers.update({**auth})
    for key in auth:
        auth[key] = str(auth[key])
        if key not in input_keys:
            session.headers.update({key: auth[key]})
    return session
