import os
import requests
from celery import Celery
from sqlalchemy import create_engine
from app.models import WeatherData
from dotenv import load_dotenv
from sqlalchemy.orm import sessionmaker

load_dotenv()

celery = Celery(__name__, broker=os.getenv("REDIS_URL"))

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

@celery.task
def fetch_weather():
    session = SessionLocal()
    response = requests.get("https://api.open-meteo.com/v1/forecast?latitude=43.65107&longitude=-79.347015&current_weather=true")
    data = response.json()

    weather_data = WeatherData(
        city="Toronto",
        temperature=data["current_weather"]["temperature"],
        condition=data["current_weather"]["weathercode"]
    )

    session.add(weather_data)
    session.commit()
    session.close()
