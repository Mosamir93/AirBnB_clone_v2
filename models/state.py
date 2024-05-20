#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import String, Column
from sqlalchemy.orm import relationship
from models.city import City
import os


class State(BaseModel, Base):
    """ State class """
    __tablename__ = 'states'
    if os.getenv('HBNB_TYPE_STORAGE') == 'db':
        __table_args__ = {'extend_existing': True}
        name = Column(String(128), nullable=False)
        cities = relationship("City", cascade="all, delete", backref="state")

    else:
        name = ''

        @property
        def cities(self):
            """Getter attribute that returns a list of cities."""
            from models import storage
            city_instances = storage.all(City)
            return [city for city in city_instances.values()
                    if city.state_id == self.id]
