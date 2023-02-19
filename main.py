import sqlalchemy
import base
import weather_model
import weather

if __name__ == "__main__":
    # Define the MariaDB engine using MariaDB Connector/Python
    engine = sqlalchemy.create_engine(f"""mariadb+mariadbconnector://{base.settings.get('user')}:{base.settings.get('password')}@{base.settings.get('host')}:{base.settings.get('port')}/{base.settings.get('default_database')}""")

    base.Base.metadata.create_all(engine, checkfirst=True)
    Session = sqlalchemy.orm.sessionmaker(bind=engine)
    session = Session()

    ws = weather.MyWeatherstation()
    rows = ws.measure()

    try:
        weather_model.addWeather(session, rows)
    except sqlalchemy.exc.SQLAlchemyError as e:
        print(f"err: {e}")
    else:
        # Reset counter in weatherstation if logged to db
        ws.prepare_set_data_count(0)
        ws.set_fixed_data()
        