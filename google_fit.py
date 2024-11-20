from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
import requests
from datetime import datetime, timedelta
import pytz
from utils import format_time

SCOPES = [
    'https://www.googleapis.com/auth/fitness.blood_pressure.read',
    'https://www.googleapis.com/auth/fitness.heart_rate.read'
]

# Obtener credenciales de Google Fit
def authorize_google_fit():
    flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
    creds = flow.run_local_server(port=8080)
    return creds

# Obtener datos de presión arterial
def get_blood_pressure_data(creds, hours):
    url = "https://www.googleapis.com/fitness/v1/users/me/dataset:aggregate"
    headers = {
        "Authorization": f"Bearer {creds.token}",
        "Content-Type": "application/json"
    }
    start_time = datetime.now() - timedelta(hours=hours)  # Ahora usa las horas proporcionadas por el usuario
    end_time = datetime.now()
    startTimeMillis = int(start_time.timestamp() * 1000)
    endTimeMillis = int(end_time.timestamp() * 1000)

    body = {
        "aggregateBy": [{"dataTypeName": "com.google.blood_pressure"}],
        "bucketByTime": {"durationMillis": 60000},
        "startTimeMillis": startTimeMillis,
        "endTimeMillis": endTimeMillis,
    }

    response = requests.post(url, headers=headers, json=body)
    data = response.json()

    blood_pressure_data = []
    for bucket in data.get("bucket", []):
        dataset = bucket["dataset"][0]
        points = dataset.get("point", [])
        for point in points:
            systolic = point["value"][0].get("fpVal")
            diastolic = point["value"][3].get("fpVal")
            start_time = point["startTimeNanos"]
            formatted_start = format_time(start_time)
            blood_pressure_data.append((systolic, diastolic, formatted_start))
    return blood_pressure_data

# Obtener datos de frecuencia cardíaca
def get_heart_rate_data(creds, hours):
    url = "https://www.googleapis.com/fitness/v1/users/me/dataset:aggregate"
    headers = {
        "Authorization": f"Bearer {creds.token}",
        "Content-Type": "application/json"
    }
    start_time = datetime.now() - timedelta(hours=hours)  # Ahora usa las horas proporcionadas por el usuario
    end_time = datetime.now()
    startTimeMillis = int(start_time.timestamp() * 1000)
    endTimeMillis = int(end_time.timestamp() * 1000)

    body = {
        "aggregateBy": [{"dataTypeName": "com.google.heart_rate.bpm"}],
        "bucketByTime": {"durationMillis": 60000},
        "startTimeMillis": startTimeMillis,
        "endTimeMillis": endTimeMillis,
    }

    response = requests.post(url, headers=headers, json=body)
    data = response.json()

    heart_rate_data = []
    for bucket in data.get("bucket", []):
        dataset = bucket["dataset"][0]
        points = dataset.get("point", [])
        for point in points:
            bpm = point["value"][0]["fpVal"]
            start_time = point["startTimeNanos"]
            formatted_start = format_time(start_time)
            heart_rate_data.append((bpm, formatted_start))
    return heart_rate_data
