from credentials import Credentials
import time
import json

SERVICE_ACCOUNT_PATH = 'test_service_account.json'

def test_init():
    cred = Credentials()
    assert(cred.expiration_time == 0)
    assert(cred.data == {})
    assert(cred.claims == {})
    assert(cred.access_token == {})
    assert(cred.base_path == "")
    assert(cred.base_url == "")

def test_set_credentials():
    cred = Credentials()
    with open(SERVICE_ACCOUNT_PATH) as service_account:
        data = json.load(service_account)

    cred.set_credentials(SERVICE_ACCOUNT_PATH, 800)
    assert(cred.expiration_time == 800)
    assert(cred.data == data)

def test_set_claims():
    cred = Credentials()
    with open(SERVICE_ACCOUNT_PATH) as service_account:
        data = json.load(service_account)

    cred.set_credentials(SERVICE_ACCOUNT_PATH, 800)
    now = int(time.time())
    cred.set_claims()

    assert(cred.claims['iss'] == data['client_email'])
    assert(cred.claims['scope'] == 'https://www.googleapis.com/auth/datastore')
    assert(cred.claims['aud'] == 'https://www.googleapis.com/oauth2/v4/token')
    assert(now - cred.claims['iat'] <= 5)
    assert((now+800) - cred.claims['exp'] <= 5)

def test_get_access_token():
    cred = Credentials()

    cred.set_credentials(SERVICE_ACCOUNT_PATH, 800)
    cred.set_claims()
    cred.get_access_token()

    assert('access_token' in cred.access_token)
    assert(cred.access_token['bearer'] == 'token')
    assert('expires_at' in cred.access_token)

def test_setup_db():
    cred = Credentials()
    with open(SERVICE_ACCOUNT_PATH) as service_account:
        data = json.load(service_account)

    cred.set_credentials(SERVICE_ACCOUNT_PATH, 800)
    cred.setup_db('test_db')

    assert(cred.base_path == "projects/{0}/databases/{1}/".format(data['project_id'], 'test_db'))
    assert(cred.base_url == "https://firestore.googleapis.com/v1/" + cred.base_path)

def main():
    test_init()
    test_set_credentials()
    test_set_claims()
    test_get_access_token()
    test_setup_db()

if __name__ == '__main__':
    main()