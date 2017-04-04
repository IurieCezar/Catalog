from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.sql import func
import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    email = Column(String(80), nullable=False)
    picture = Column(String(250))

class Category(Base):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)
    items = relationship('Item', back_populates='category')

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'cat_name'         : self.name,
            'id'           : self.id,
            'item'         : [i.serialize for i in self.items],
        }

class Item(Base):
    __tablename__ = 'item'

    title = Column(String(80), nullable = False)
    id = Column(Integer, primary_key = True)
    description = Column(String(250))
    image = Column(String(250))
    date_created = Column(DateTime(timezone=True), server_default=func.now())
    cat_id = Column(Integer,ForeignKey('category.id'))
    category = relationship('Category', back_populates='items')
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
           'cat_id'        : self.cat_id,
           'description'   : self.description,
           'image'         : self.image,
           'id'            : self.id,
           'title'         : self.title,
        }


engine = create_engine('sqlite:///catalog.db')
Base.metadata.create_all(engine)
