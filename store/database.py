import os
from dotenv import load_dotenv
from sqlalchemy import Table, Column, Integer, String, ForeignKey, create_engine
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base


load_dotenv()


# Schema
Base = declarative_base()

association_table = Table('recordtocategory', Base.metadata,
    Column('record_id', Integer, ForeignKey('record.id')),
    Column('category_id', Integer, ForeignKey('category.id'))
)

class Record(Base):
    __tablename__ = 'record'
    id = Column(Integer, primary_key=True)
    text = Column(String(length=4095))
    categories = relationship("Category",
                    secondary=association_table)

class Category(Base):
    __tablename__ = 'category'
    id = Column(Integer, primary_key=True)
    name = Column(String(length=127), unique=True)


# Database Engine Wrapper
class Database:
    def __init__(self):
        self.engine = create_engine(os.getenv("DATABASE_URL"))
        self.Session = sessionmaker(bind=self.engine)

    def createDB(self):
        Base.metadata.create_all(self.engine)

    def recordsCreate(self, records):   # records:[dict] -> [int]
        session = self.Session()
        ids = []
        for r in records:
            newRecord = Record(text=r["text"])
            for c in r["categories"]:
                category = session.query(Category).filter(Category.id == self.toCategoryId(c)).first()
                newRecord.categories.append(category)
            session.add(newRecord)
            session.flush()
            ids.append(newRecord.id)
        session.commit()
        return ids

    def recordsDelete(self, ids):   # ids: [int] ->
        session = self.Session()
        for id in ids:
            delete_relations = association_table.delete().where(association_table.c.record_id == id)
            session.execute(delete_relations)
            record = session.query(Record).filter(Record.id == id).first()
            session.delete(record)
        session.commit()

    def recordGetAll(self):   # -> [Record]
        session = self.Session()
        records = session.query(Record).all()
        return records

    def categoryCreate(self, name):  # name: str ->
        session = self.Session()
        newCategory = Category(name=name)
        session.add(newCategory)
        session.commit()

    def categoryDelete(self, category):  # category: str|int -> str|None
        session = self.Session()
        category = self.toCategoryId(category)
        relations = session.query(association_table.c.record_id).filter(association_table.c.category_id == category).all()
        recordIds = list(map(lambda x: x[0], relations))
        self.recordsDelete(recordIds)
        category = session.query(Category).filter(Category.id == category).first()
        session.delete(category)
        session.commit()

    def toCategoryId(self, category):  # category: str|int -> int
        if type(category) == str:
            session = self.Session()
            category = session.query(Category.id).filter(Category.name == category).first()[0]
        return category

    def categoryGetAll(self):   # -> [Category]
        session = self.Session()
        categories = session.query(Category).all()
        return categories

    def categoryInUse(self, category):   # str|int -> bool
        session = self.Session()
        category = self.toCategoryId(category)
        record = session.query(association_table).filter(association_table.c.category_id == category).first()
        return record != None
