import datetime
import json

import requests
import uuid


class X3:
    login: str
    password: str
    host: str
    headers = {}
    ses = requests.Session()

    def get_data(self):
        return {"username": self.login, "password": self.password}

    def test_connect(self):
        response = self.ses.post(f"{self.host}/login", data=self.get_data())
        return response

    def send_request(self, method: str, path: str, data: dict = None):
        if method == "POST":
            return self.ses.post(f"{self.host}{path}", data=data)
        elif method == "GET":
            return self.ses.get(f"{self.host}{path}", data=data)
        elif method == "DELETE":
            return self.ses.delete(f"{self.host}{path}", data=data)
        elif method == "PUT":
            return self.ses.put(f"{self.host}{path}", data=data)
        elif method == "PATCH":
            return self.ses.patch(f"{self.host}{path}", data=data)



if __name__ == "__main__":
    x3 = X3()
    
    print(x3.test_connect())