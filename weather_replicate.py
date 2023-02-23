import sqlalchemy
import base
import weather_model
import requests
import json

url = 'https://iot-api-4exo5vh6.ew.gateway.dev/v1/weather/insert' #todo: move
headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}

if __name__ == "__main__":
    # Define the MariaDB engine using MariaDB Connector/Python
    engine = sqlalchemy.create_engine(f"""mariadb+mariadbconnector://{base.settings.get('user')}:{base.settings.get('password')}@{base.settings.get('host')}:{base.settings.get('port')}/{base.settings.get('default_database')}""")

    base.Base.metadata.create_all(engine, checkfirst=True)
    Session = sqlalchemy.orm.sessionmaker(bind=engine)
    session = Session()

    try:
        r = weather_model.selectWeatherReplication(session)
        print(r)
    except sqlalchemy.exc.SQLAlchemyError as e:
        print(f"err: {e}")

    data = json.dumps({"data": json.dumps(r)})
    print(data)
    q = requests.post(url, headers=headers, data=data)
    print(q, q.text)