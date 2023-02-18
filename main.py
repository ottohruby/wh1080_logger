import sqlalchemy
import base
import weather_model
import weather

# todo move somewhere else, so it is not exposed
settings = {"user": "root", 
            "password": "raspberry",
            "host": "127.0.0.1", #127.0.0.1
            "port": "3306",
            "default_database": "data"}

if __name__ == "__main__":
    # Define the MariaDB engine using MariaDB Connector/Python
    engine = sqlalchemy.create_engine(f"""mariadb+mariadbconnector://{settings.get('user')}:{settings.get('password')}@{settings.get('host')}:{settings.get('port')}/{settings.get('default_database')}""")

    base.Base.metadata.create_all(engine, checkfirst=True)
    Session = sqlalchemy.orm.sessionmaker(bind=engine)
    session = Session()

    ws = weather.MyWeatherstation()
    rows = ws.measure()

    weather_model.addWeather(session, rows)
    print("ok")