import requests
import datetime
import json
import os


class DataRetriever:

    def __init__(self):
        self.file_saver = self.FileSaver()
        self.access_token = self.AccessToken()

    class AccessToken:

        def __init__(self):
            f = open('api_key_secret_pairs.json', 'r')
            file_data = json.load(f)

            oldest_api_key = ""
            oldest_api_secret = ""
            oldest_api_usage_time = datetime.datetime.strptime("2100-01-01 00:00:00", "%Y-%m-%d %H:%M:%S")
            for each in file_data['key_pairs']:
                datetime.datetime.strptime(each['last_usage_time'], "%Y-%m-%d %H:%M:%S")
                if datetime.datetime.strptime(each['last_usage_time'], "%Y-%m-%d %H:%M:%S") < oldest_api_usage_time:
                    oldest_api_usage_time = datetime.datetime.strptime(each['last_usage_time'], "%Y-%m-%d %H:%M:%S")
                    oldest_api_key = each['api_key']
                    oldest_api_secret = each['api_secret']
            for each in file_data['key_pairs']:
                if each['api_key'] == oldest_api_key:
                    each['last_usage_time'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            f.close()
            f_w = open('api_key_secret_pairs.json', 'w')
            json.dump(file_data, f_w, indent=2)

            self.CID = oldest_api_key
            self.CSCRT = oldest_api_secret
            print(self.CID, self.CSCRT)
            self.access_token = ""
            self.token_type = ""
            self.expires_at = None
            self.expire_flag = True

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
                self.expire_flag = False

            return self.access_token

        def check_if_expired(self):
            '''
            if self.expires_at is not None:
                if self.expires_at > datetime.datetime.now():
                    return False
            return True
            '''
            return self.expire_flag

        def set_expire(self):
            self.expire_flag = True

    class FileSaver:
        def __init__(self):
            self.current_path = os.path.dirname(__file__)

            if not os.path.exists('/result'):
                os.mkdir(os.path.join(self.current_path, "/result"))

            result_relative_path = "result/" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S") + "/"
            self.abs_file_path = os.path.join(self.current_path, result_relative_path)
            os.mkdir(self.abs_file_path)

        def save(self, page_num: int, data):
            file_name = "AllPet_" + str(page_num) + ".txt"
            file_abs_path = os.path.join(self.abs_file_path, file_name)
            f = open(file_abs_path, "a")
            f.write(json.dumps(data, indent=2))
            f.close()

    def expire_access_token(self):
        self.access_token = self.AccessToken()

    def pull_a_page(self, page_num: int):
        headers = {
            'Authorization': 'Bearer ' + self.access_token.get_access_token()
        }

        params = (
            ('limit', 100),
            ('page', page_num)
        )

        response = requests.get('https://api.petfinder.com/v2/animals', headers=headers, params=params)
        response_data = response.json()

        self.file_saver.save(page_num, response_data)

    def pull_everything(self):
        cnt = 1
        while cnt < 1001:
            data_retriever.pull_a_page(cnt)
            print("Page Number: ", cnt)
            cnt = cnt + 1
        self.expire_access_token()
        while cnt < 2001:
            data_retriever.pull_a_page(cnt)
            print("Page Number: ", cnt)
            cnt = cnt + 1
        self.expire_access_token()
        while cnt < 2005:
            data_retriever.pull_a_page(cnt)
            print("Page Number: ", cnt)
            cnt = cnt + 1


data_retriever = DataRetriever()
data_retriever.pull_everything()

'''
c = 1001
while c < 2002:
    data_retriever.pull_a_page(c)
    print("Page Number: ", c)
    c = c + 1
'''
