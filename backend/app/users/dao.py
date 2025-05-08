from app.core.dao import BaseDAO
from app.users.models import User


class UserDAO(BaseDAO[User]):
    model = User
