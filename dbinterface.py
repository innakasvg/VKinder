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

def add_profile(engine, profile_id, worksheet_id):
    with Session(engine) as session:
        add_to_bd = Seen(profile_id=profile_id, worksheet_id=worksheet_id)
        session.add(add_to_bd)
        session.commit()

#engine = create_engine(db_url_object)
#Base.metadata.create_all(engine)

# извлечение записей из БД
def find_profile(engine, profile_id, worksheet_id):
    with Session(engine) as session:
        find_in_bd = session.query(Seen).filter(
            Seen.profile_id == profile_id,
            Seen.worksheet_id == worksheet_id
        ).first()
        return True if find_in_bd else False


#engine = create_engine(db_url_object)
#with Session(engine) as session:
#    from_bd = session.query(Seen).filter(Seen.profile_id==2).all()
#    for item in from_bd:
#        print(item.worksheet_id)

if __name__ == '__main__':
    #bot = BotFront(comunity_token, acces_token)
    bot.event_handler()

if __name__ == '__main__':
    profile_id = []
    worksheet_id = []
    engine = create_engine(db_url)
    Base.metadata.create_all(engine)
    add_profile(engine, profile_id, worksheet_id)
    result = finde_profile(engine, profile_id, worksheet_id)
    print(result)
            