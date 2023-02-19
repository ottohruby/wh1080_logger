from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

# todo move somewhere else, so it is not exposed
settings = {"user": "root", 
            "password": "raspberry",
            "host": "127.0.0.1", #127.0.0.1
            "port": "3306",
            "default_database": "data"}