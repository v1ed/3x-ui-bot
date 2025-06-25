import aiohttp
import json
import asyncio
import uuid

import aiohttp.http_exceptions
import aiohttp.web_exceptions


class XUIAPI:
    def __init__(self, host, port, webpath):
        self.username = ""
        self.password = ""
        self.host = host
        self.url = f"https://{host}:{port}{webpath}/"
        # self.ses = None
        self.ses = aiohttp.ClientSession(base_url=self.url)
    
    async def close_session(self):
        if self.ses and not self.ses.closed:
            await self.ses.close()

    async def login(self, username, password):
        self.username = username
        self.password = password
        data = {
            "username": self.username,
            "password": self.password,
        }
        response = await self._send_request("POST", "login", data=data)
        return response
    
    async def inbounds(self):
        response = await self._send_request("GET", "panel/api/inbounds/list")
        return response
    
    async def inbound(self, inbound_id):
        response = await self._send_request("GET", f"panel/api/inbounds/get/{inbound_id}")
        return response
    
    async def client_traffic_by_email(self, email):
        response = await self._send_request("GET", f"panel/api/inbounds/getClientTraffics/{email}")
        return response
    
    async def client_traffic_by_id(self, client_id):
        response = await self._send_request("GET", f"panel/api/inbounds/getClientTraffics/{client_id}")
        return response
    
    async def generate_link(self, inbound_id, client_name):
        resp = await self.inbound(inbound_id)
        inbound_name = resp['obj']['remark']
        protocol = resp['obj']['protocol']
        port = resp['obj']['port']
        settings = json.loads(resp['obj']['settings'])
        clients = settings['clients']
        client = None
        for c in clients:
            if c['email'] == client_name:
                client = c
                break
        client_id = client['id']
        client_flow = client['flow']

        streamSettings = json.loads(resp['obj']['streamSettings'])
        network = streamSettings['network']
        security = streamSettings['security']
        publicKey = streamSettings['realitySettings']['settings']['publicKey']
        fingerprint = streamSettings['realitySettings']['settings']['fingerprint']
        sni = streamSettings['realitySettings']['serverNames'][0]
        sid = streamSettings['realitySettings']['shortIds'][0]
        return f"{protocol}://{client_id}@{self.host}:{port}?type={network}&security={security}&pbk={publicKey}&fp={fingerprint}&sni={sni}&sid={sid}&spx=%2F&flow={client_flow}#{inbound_name}-{client_name}"
    
    async def create_client(self, client_id, inbound_id, email, traffic_limit = 0, expiry_time = 0):
        data = {
            "id": inbound_id,
            "settings": json.dumps({
                "clients": [
                    {
                        "id": client_id,
                        "flow": "xtls-rprx-vision",
                        "email": email,
                        "limitIp": 0,
                        "totalGB": 0,
                        "expiryTime": expiry_time,
                        "enable": True,
                        # "tgId": "",
                        # "subId": "",
                        # "reset": 0
                    }
                ]
            })
        }
        response = await self._send_request("POST", "panel/api/inbounds/addClient", data=data)
        return response
    
    async def delete_client(self, client_id, inbound_id):
        response = await self._send_request("POST", f"panel/api/inbounds/{inbound_id}/delClient/{client_id}")
        return response
    
    async def _send_request(self, method: str, path: str, data: dict = None, max_attempts: int = 5):
        for attempt in range(max_attempts):
            print(f"Trying to make {method} request to {self.url}{path} (attempt {attempt + 1})...")
            try:
                async with self.ses.request(
                        method=method, 
                        url=f"{path}", 
                        json=data) as resp:
                    if resp.status == 200:
                        print(f"Susscessful {method} request to {self.url}{path}")
                        if resp.content_type == 'application/json':
                            return await resp.json()
                        elif resp.content_type == 'text/plain':
                            return await resp.text()
                        else:
                            return resp
                    else:
                        print(f"[ERROR] An error occured while making {method} request to {self.url}{path}\nResponse status: {resp.status}\tDetail: {await resp.text()}")
                        return None
            except Exception as e:
                print(f"[ERROR] An error occured while making {method} request to {self.url}{path}\nDetail: {e}")
            await asyncio.sleep(1)
        print(f"Failed to to make {method} request to {self.url}{path} after {max_attempts} attempts.")
        return None