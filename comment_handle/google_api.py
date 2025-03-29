import requests
from decouple import config
from rest_framework import status
from rest_framework.response import Response

class HandleText:
    def __init__(self):
        self.url = config("GOOGLE_LANGUAGE_URL")
        self.__user_project = config("GOOGLE_PROJECT")
        self.token_url = config("GOOGLE_AUTH_URL")
        self.client_id = config("GOOGLE_CLIENT_ID")
        self.client_secret = config("GOOGLE_CLIENT_SECRET")
        self.refresh_token = config("GOOGLE_REFRESH_TOKEN")

    def get_google_token(self):
        try:
            payload = f"client_id={self.client_id}&client_secret={self.client_secret}&refresh_token={self.refresh_token}&grant_type=refresh_token"
            headers = {
              'Content-Type': 'application/x-www-form-urlencoded'
            }
            response = requests.request("POST", self.token_url, headers=headers, data=payload)
            if response.status_code == 200:
                self.token = response.json().get('access_token')
                return self.token
            return response.status_code()
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def call_google_api(self,text):
        """
            Function to call google api to check text
        """
        try:
            token = self.get_google_token()
            payload = {"document":{"type":"PLAIN_TEXT","content":text}}
            headers = {
              'Authorization': f'Bearer {token}',
              'Content-Type': 'application/json; charset=utf-8',
              'x-goog-user-project': self.__user_project
            }
            response = requests.request("POST", self.url, headers=headers, data=str(payload))
            if response.status_code == 200:
                return response.json()
            return Response({"error":"Unexpected error occured"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


