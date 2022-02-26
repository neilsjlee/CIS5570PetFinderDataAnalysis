import requests
import datetime
import json
import os


class DataRetriever:

    def __init__(self):
        self.CLIENT_ID = "DUMMY_API_KEY"
        self.CLIENT_SECRET = "DUMMY_API_SECRET"

        self.current_path = os.path.dirname(__file__)
        result_relative_path = "result/" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S") + "/"
        os.mkdir(result_relative_path)
        self.abs_file_path = os.path.join(self.current_path, result_relative_path)

        self.access_token = self.AccessToken(self.CLIENT_ID, self.CLIENT_SECRET, self.abs_file_path)
        self.access_token.get_access_token()

    class AccessToken:
        # A singleton class that manages the Access Token required for accessing PetFinder API.

        def __init__(self, client_id, client_secret, abs_file_path):
            self.CID = client_id
            self.CSCRT = client_secret
            self.abs_file_path = abs_file_path
            self.access_token = ""
            self.token_type = ""
            self.expires_at = None

        def __str__(self):
            self.get_access_token()
            return self.access_token

        def get_access_token(self):
            if self.check_if_expired():
                data = {
                    'grant_type': 'client_credentials',
                    'client_id': self.CID,
                    'client_secret': self.CSCRT
                }

                response = requests.post('https://api.petfinder.com/v2/oauth2/token', data=data)
                response_data = response.json()
                print(response_data)
                self.access_token = response_data['access_token']
                self.token_type = response_data['token_type']
                expires_in = response_data['expires_in']

                self.expires_at = datetime.datetime.now() + datetime.timedelta(seconds=expires_in)

            return self.access_token

        def check_if_expired(self):
            if self.expires_at is not None:
                if self.expires_at > datetime.datetime.now():
                    return False
            return True

    def pull_everything(self, page_num: int):
        headers = {
            'Authorization': 'Bearer ' + self.access_token.get_access_token(),
        }

        params = (
            ('limit', 100),
            ('page', page_num)
        )

        response = requests.get('https://api.petfinder.com/v2/animals', headers=headers, params=params)
        response_data = response.json()

        # if os.path.exists('/result')
        current_path = os.path.dirname(__file__)

        file_name = "AllPet_" + str(page_num) + ".txt"
        file_abs_path = os.path.join(self.abs_file_path, file_name)
        f = open(file_abs_path, "a")
        f.write(json.dumps(response_data, indent=2))
        f.close()


data_retriever = DataRetriever()

c = 1
while c < 11:
    data_retriever.pull_everything(c)
    print("Page Number: ", c)
    c = c + 1

