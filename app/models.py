from sqlalchemy import Integer, Boolean
from sqlalchemy.orm import declarative_base, Mapped, mapped_column


Base = declarative_base()


class Car(Base):
    __tablename__ = "cars"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str]
    equipment: Mapped[str | None]
    price: Mapped[int]
    created_date: Mapped[str]
    mileage: Mapped[int]
    is_sold: Mapped[bool] = mapped_column(Boolean, default=False)
    last_message_id: Mapped[int | None]
    accident_amount: Mapped[int | None]

    def __repr__(self):
        return f"<Car(id={self.id}, name={self.name})>"


class Link(Base):
    __tablename__ = "links"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    car_name: Mapped[str]
    link: Mapped[str]
    chat_id: Mapped[int]

    def __repr__(self):
        return f"<Link(id={self.id}, car_name={self.car_name})>"
