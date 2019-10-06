import time
import jwt
import requests
import json

class Credentials():

        def __init__(self):
            self.expiration_time = 0
            self.data = {}
            self.claims = {}
            self.access_token = {}
            self.base_path = ""
            self.base_url = ""

        def set_credentials(self, key_path, expiration_time=3600):
            self.expiration_time = expiration_time
            with open(key_path) as config_file:
                self.data = json.load(config_file)

        def set_claims(self):
            now = int(time.time())
            later = now + self.expiration_time
            self.claims = {
                'iss': self.data["client_email"],
                'scope': 'https://www.googleapis.com/auth/datastore',
                'aud': 'https://www.googleapis.com/oauth2/v4/token',
                'iat': now,
                'exp': later   
            }

        def get_access_token(self):
            privateKey = self.data["private_key"]
            encodedJwt = jwt.encode(self.claims, privateKey.strip(), algorithm='RS256')
            payload = {
                'grant_type': 'urn:ietf:params:oauth:grant-type:jwt-bearer',
                'assertion': encodedJwt
            }
            self.access_token = requests.post("https://www.googleapis.com/oauth2/v4/token", data=json.dumps(payload), verify=True).json()
            
        def setup_db(self, database):
            self.base_path = "projects/{0}/databases/{1}/".format(self.data['project_id'], database)
            self.base_url = "https://firestore.googleapis.com/v1/" + self.base_path
        
        def initialize_app(self, database="(default)"):
            self.set_claims()
            self.get_access_token()
            self.setup_db(database)