from database.crud.base import BaseCRUD
from database.models import Server

class ServerCRUD(BaseCRUD):
    model = Server
    