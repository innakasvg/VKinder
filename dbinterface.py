# импорты
#import sqlalchemy as sq
#from sqlalchemy.orm import declarative_base
#from sqlalchemy import create_engine
#from sqlalchemy.orm import Session

import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, Session
from sqlalchemy import create_engine, MetaData


from config import db_url_object

# схема БД
metadata = MetaData()
Base = declarative_base()

engine = create_engine(db_url_object)

class Seen(Base):
    __tablename__ = 'vkinder_seen'
    profile_id = sq.Column(sq.Integer, primary_key=True)
    worksheet_id = sq.Column(sq.Integer, primary_key=True)


# добавление записи в бд
class DbTools:
    def __init__(self, engine):
        self.engine = engine

    def add_profile(self, profile_id, worksheet_id):
        print('add')
        print(profile_id)
        print(worksheet_id)
        with Session(self.engine) as session:
            add_to_bd = Seen(profile_id=profile_id, worksheet_id=worksheet_id)
            session.add(add_to_bd)
            session.commit()

# извлечение записей из БД

    def find_profile(self, profile_id, worksheet_id):
        print('look')
        print(profile_id)
        print(worksheet_id)
        with Session(self.engine) as session:
            find_in_bd = session.query(Seen).filter(
                Seen.profile_id == profile_id,
                Seen.worksheet_id == worksheet_id
                ).first()
            print(find_in_bd)
            return True if find_in_bd else False

if __name__ == '__main__':
    profile_id = []
    worksheet_id = []
    metadata.create_all(engine)
    DbTools.add_profile(engine, profile_id, worksheet_id)
    result = DbTools.find_profile(engine, profile_id, worksheet_id)
    print(result)
            