from models import Link
from sqlalchemy import insert
from sqlalchemy.orm import Session
from utils import get_session

def fill_link():
    session: Session = get_session()
    try:
        session.execute(
            insert(Link).values(
                car_name="Sportage",
                link="https://api.encar.com/search/car/list/premium?count=true&q=(And.Hidden.N._.(C.CarType.Y._.(C.Manufacturer.%EA%B8%B0%EC%95%84._.(C.ModelGroup.%EC%8A%A4%ED%8F%AC%ED%8B%B0%EC%A7%80._.(C.Model.%EC%8A%A4%ED%8F%AC%ED%8B%B0%EC%A7%80+5%EC%84%B8%EB%8C%80._.BadgeGroup.%EA%B0%80%EC%86%94%EB%A6%B0+2WD.))))_.Mileage.range(..30000)._.Year.range(..202206).)&sr=%7CModifiedDate%7C0%7C50",
                chat_id="-4915770110",
            )
        )
        session.commit()
    finally:
        session.close()

if __name__ == '__main__':
    fill_link()