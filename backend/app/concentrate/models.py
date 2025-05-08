from sqlalchemy import ForeignKey, Integer, String, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base

class Concentrate(Base):
    """
    Модель для хранения показателей железорудного концентрата за определённый месяц.

    Поля:
    - id: Уникальный идентификатор записи.
    - name: Наименование концентрата или пробы.
    - iron: Содержание железа (Fe).
    - silicon: Содержание кремния (Si).
    - aluminum: Содержание алюминия (Al).
    - calcium: Содержание кальция (Ca).
    - sulfur: Содержание серы (S).
    - report_month: Отчётный месяц в формате YYYY-MM.
    - user_id: Идентификатор пользователя, который добавил запись.
    - user: Объект пользователя (связь с моделью User).
    """
    __tablename__ = "concentrates"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)

    iron: Mapped[float] = mapped_column(nullable=False)     # Содержание железа (Fe)
    silicon: Mapped[float] = mapped_column(nullable=False)  # Содержание кремния (Si)
    aluminum: Mapped[float] = mapped_column(nullable=False) # Содержание алюминия (Al)
    calcium: Mapped[float] = mapped_column(nullable=False)  # Содержание кальция (Ca)
    sulfur: Mapped[float] = mapped_column(nullable=False)   # Содержание серы (S)

    report_month: Mapped[str] = mapped_column(String(7), nullable=False)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    user = relationship("User", back_populates="concentrates")