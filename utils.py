from datetime import datetime
import pytz

def format_time(nanos):
    seconds = int(nanos) / 1e9
    utc_time = datetime.utcfromtimestamp(seconds)
    local_tz = pytz.timezone("America/Mexico_City")
    local_time = utc_time.replace(tzinfo=pytz.utc).astimezone(local_tz)
    return local_time.strftime('%Y-%m-%d %H:%M:%S')

def check_anomalies(heart_data, blood_pressure_data):
    anomalies = []  # Almacenar las anomalías
    # Verificar frecuencia cardíaca
    for bpm, date in heart_data:
        if bpm > 100:
            anomalies.append(f"Frecuencia cardíaca alta: {bpm} BPM en la fecha y hora: {date}")
        elif bpm < 60:
            anomalies.append(f"Frecuencia cardíaca baja: {bpm} BPM en la fecha y hora: {date}")

    # Verificar presión arterial
    for systolic, diastolic, date in blood_pressure_data:
        if systolic > 140 or diastolic > 90:
            anomalies.append(f"Presión arterial alta: {systolic}/{diastolic} en la fecha y hora: {date}")
        elif systolic < 90 or diastolic < 60:
            anomalies.append(f"Presión arterial baja: {systolic}/{diastolic} en la fecha y hora: {date}")

    return anomalies

def create_alert_message(user_name, heart_data, blood_pressure_data):
    anomalies = check_anomalies(heart_data, blood_pressure_data)
    message = f"Hola... {user_name} te ha designado como destinatario para su cuidado ya que se han detectado valores anómalos en sus datos de salud:\n\n"
    for anomaly in anomalies:
        message += f"- {anomaly}\n"
    message += "\nPor favor, revisa estos valores y consulta a un médico si es necesario."
    return message
