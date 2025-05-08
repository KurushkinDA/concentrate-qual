from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.concentrate.models import Concentrate
from app.core.database import Base


class User(Base):
    """
    Модель пользователя системы.
    Хранит данные авторизации и связывается с записями показателей (concentrates).
    """

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(
        String(50), nullable=False, index=True, unique=True
    )
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)

    concentrates = relationship(Concentrate, back_populates="user")
