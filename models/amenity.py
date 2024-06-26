#!/usr/bin/python3
""" Module for AirBnb project """
from models.base_model import BaseModel, Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String
from os import getenv


class Amenity(BaseModel, Base):
    """ test class """
    __tablename__ = "amenities"

    if getenv("HBNB_TYPE_STORAGE") == "db":
        name = Column(String(128), nullable=False)

        place_amenities = relationship(
            "Place", secondary="place_amenity", back_populates="amenities")

    else:
        name = ""
