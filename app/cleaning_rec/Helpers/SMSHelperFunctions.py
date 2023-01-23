import requests

class TelstraSMSFunctions:

    def telstra_request(self, endpoint, body=None, headers=None, *, token=None, method='POST'):
        send_headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
        if token:  # if this is an authenticated request, add the token header
            send_headers['Authorization'] = 'Bearer ' + token
        if headers:  # add any extra headers if desired
            send_headers.update(headers)

        url = "https://tapi.telstra.com/v2/" + endpoint
        return requests.request(method, url, json=body, headers=send_headers)

    def auth(self, app_key, app_secret):
        body = dict(client_id=app_key, client_secret=app_secret,
            grant_type="client_credentials", scope="NSMS")
        response = requests.post("https://tapi.telstra.com/v2/oauth/token", body)

        if response.status_code != 200:
            raise RuntimeError("Bad response from Telstra API! " + response.text)

        response_json = response.json()
        return response_json['access_token']

    def create_subscription(self, token):
        response = self.telstra_request("messages/provisioning/subscriptions", {}, token=token)

        if response.status_code != 201:
            raise RuntimeError("Bad response from Telstra API! " + response.text)

        response_json = response.json()
        return response_json['destinationAddress']
    
    def send_sms(self, token, to, body):
        payload = dict(to=to, body=body)
        response = self.telstra_request("messages/sms", payload, token=token)

        if response.status_code != 201:
            raise RuntimeError("Bad response from Telstra API! " + response.text)

        response_json = response.json()
        return response_json