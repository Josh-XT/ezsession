# ezsession
A small useful Python module to abstract away the common auth header methods used by different software vendors.  The output is a requests session with the authentication headers built in.

## Auth Types and Required Inputs

1. **oauth** - `client_id`, `client_secret`, `audience`
2. **oauth_basic** - `username`, `password`
3. **oauth_password** - `username`, `password`
4. **basic** - `username`, `password`
5. **bearer** - `api_key`
6. **ApiToken** - `api_key`
7. **dell** - `client_id`, `client_secret`

## Examples
Example usage for getting a Datto RMM or Huntress session:

```python
from ezsession import get_session
def datto_rmm_auth(api_key, api_secret):
    auth = {
        "type": "oauth_basic",
        "auth_uri": f"{base_uri}/auth/oauth/token",
        "username": api_key,
        "password": api_secret,
        "server": "concord",
    }
    return get_session(auth)
 
def huntress_auth(api_key, api_secret):
  auth = {
    "type": "basic",
    "username": auth_data["api_key"],
    "password": auth_data["api_secret"],
  }
  return get_session(auth)
```

Example to initialize a Datto RMM session then get account variables.

```python
server = "merlot" # Change to your Datto RMM server.
base_uri = f"https://{server}-api.centrastage.net"
session = datto_rmm_auth(drmm_user, drmm_pass)
response = session.get(f"https://{base_uri}/api/v2/account/variables")
variables = response.json()["variables"]
```
