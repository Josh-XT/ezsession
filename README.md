[![GitHub](https://img.shields.io/badge/GitHub-Sponsor%20Josh%20XT-blue?logo=github&style=plastic)](https://github.com/sponsors/Josh-XT) [![PayPal](https://img.shields.io/badge/PayPal-Sponsor%20Josh%20XT-blue.svg?logo=paypal&style=plastic)](https://paypal.me/joshxt) [![Ko-Fi](https://img.shields.io/badge/Kofi-Sponsor%20Josh%20XT-blue.svg?logo=kofi&style=plastic)](https://ko-fi.com/joshxt)

# ezsession
A small useful Python module to abstract away the common auth header methods used by different software vendors.  The output is a requests session with the authentication headers built in.

```
pip install ezsession
```

## Auth Types and Required Inputs

1. **oauth** - `auth_uri`, `client_id`, `client_secret`, `audience`
2. **oauth_basic** - `auth_uri`, `username`, `password`
3. **oauth_password** - `auth_uri`, `username`, `password`
4. **basic** - `username`, `password`, `auth_uri` (optional)
5. **bearer** - `api_key`
6. **ApiToken** - `api_key`
7. **dell** - `auth_uri`, `client_id`, `client_secret`

## Examples
Example usage for getting a Datto RMM session:

```python
from ezsession import get_session
def datto_rmm_session(api_key, api_secret, server):
    base_uri = f"https://{server}-api.centrastage.net"
    auth = {
        "type": "oauth_basic",
        "auth_uri": f"{base_uri}/auth/oauth/token",
        "username": api_key,
        "password": api_secret,
        "server": server,
    }
    return get_session(auth), base_uri
```

Example to initialize a Datto RMM session then get account variables.

```python
drmm_user = "Your Datto RMM API Key"
drmm_pass = "Your Datto RMM API Secret"
drmm_server = "merlot" # Change to your Datto RMM server.
session, base_uri = datto_rmm_auth(drmm_user, drmm_pass, drmm_server)
response = session.get(f"{base_uri}/api/v2/account/variables")
variables = response.json()["variables"]
```
