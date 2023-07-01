# импорты
import sqlalchemy as sq
from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import Session
from config import db_url_object

# схема БД
metadata = MetaData()
Base = declarative_base()

class Seen(Base):
    __tablename__ = 'vkinder_seen'
    profile_id = sq.Column(sq.Integer, primary_key=True)
    worksheet_id = sq.Column(sq.Integer, primary_key=True)


# добавление записи в бд
#db_url_object = "postgresql://postgres:postgres@localhost/vkinder"
engine = create_engine(db_url_object)
Base.metadata.create_all(engine)
with Session(engine) as session:
    to_bd = Seen(profile_id=1, worksheet_id=1)
    session.add(to_bd)
    session.commit()

# извлечение записей из БД

engine = create_engine(db_url_object)
with Session(engine) as session:
    from_bd = session.query(Seen).filter(Seen.profile_id==1).all()
    for item in from_bd:
        print(item.worksheet_id)

if __name__ == '__main__':
    bot = BotFront(comunity_token, acces_token)
    bot.event_handler()
            