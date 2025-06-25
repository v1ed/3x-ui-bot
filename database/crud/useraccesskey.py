from database.crud.base import BaseCRUD
from database.models import UserAccessKey

class UserAccessKeyCRUD(BaseCRUD):
    model = UserAccessKey
    