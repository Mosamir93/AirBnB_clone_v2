from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from os import getenv
from models.base_model import Base


class DBStorage:
    __engine = None
    __session = None

    def __init__(self):
        """Init method."""
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.format(
            getenv('HBNB_MYSQL_USER'),
            getenv('HBNB_MYSQL_PWD'),
            getenv('HBNB_MYSQL_HOST', 'localhost'),
            getenv('HBNB_MYSQL_DB')),
            pool_pre_ping=True)

        if getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Query on the current database session."""
        from models.user import User
        from models.place import Place
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.review import Review
        objects = {}
        if cls:
            query = self.__session.query(cls).all()
            for obj in query:
                key = f"{cls.__name__}.{obj.id}"
                objects[key] = obj
        else:
            query = self.__session\
                .query(User, Place, State, City, Amenity, Review).all()
            for obj in query:
                key = f"{obj.__class__.__name__}.{obj.id}"
                objects[key] = obj
        return objects

    def new(self, obj):
        """Adds the object to session."""
        self.__session.add(obj)

    def save(self):
        """Commit all changes in session."""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete from the current database session."""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """Create all tables in the database and
         create the current database session."""
        from models.user import User
        from models.place import Place
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.review import Review
        Base.metadata.create_all(self.__engine)
        Session = sessionmaker(bind=self.__engine, expire_on_commit=False)
        self.__session = scoped_session(Session)

    def close(self):
        """Call remove() method on the private session attribute."""
        self.__session.remove()
