class Luis_data:
    def __init__(self):
        self.target_user = []
        self.url_api = "https://westus.api.cognitive.microsoft.com/luis/v2.0/apps/ff06e71f-599b-449c-a0a7-c8e40cb47474"
        self.headers = {
        # Request headers
        'Ocp-Apim-Subscription-Key': 'ffca408d10db49febef3cd29d31863f4',
        }

        self.params = {
        'q' : "",
        # Optional request parameters, set to default values
        'timezoneOffset': '0',
        'verbose': 'false',
        'spellCheck': 'false',
        'staging': 'false',
        }

    def send(self, message_to_luis):
        self.params['q'] = message_to_luis
        return "working on this, try later"

        try:
            response = requests.get(self.url_api, headers=self.headers, params=self.params)
            print(r.json())

        except Exception as e:
            print("[Errno {0}] {1}".format(e.errno, e.strerror))

    def process_msg(self, msg, return_msg):
        return_msg.main = self.send(msg.msg_trim)

    def add_user(self, msg, return_msg):
        self.target_user.append(msg.author)
        return_msg.main = msg.author.mention + " is now talking with LUIS"

    def remove_user(self, msg, return_msg):
        self.target_user.remove(msg.author)
        return_msg.main = msg.author.mention + " no longer talk with LUIS"
