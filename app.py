from flask import Flask, render_template, request
from google_fit import get_heart_rate_data, get_blood_pressure_data, authorize_google_fit
from email_alert import send_email_alert
from utils import check_anomalies, create_alert_message
import webbrowser
import threading

app = Flask(__name__)

# Ruta principal para mostrar la página HTML
@app.route('/')
def index():
    return render_template('index.html')

# Ruta para iniciar sesión y obtener datos
@app.route('/authorize', methods=['POST'])
def authorize():
    # Recuperar datos del formulario
    user_email = request.form.get("user_email")
    user_name = request.form.get("user_name")  # Nuevo campo para nombre
    recipient_email = request.form.get("recipient_email")
    hours = int(request.form.get("hours"))  # Horas ingresadas por el usuario

    creds = authorize_google_fit()
    heart_data = get_heart_rate_data(creds, hours)
    blood_pressure_data = get_blood_pressure_data(creds, hours)

    # Evaluar datos y enviar alerta si es necesario
    if check_anomalies(heart_data, blood_pressure_data):
        subject = "⚠️ Alerta de Salud Detectada"
        message = create_alert_message(user_name, heart_data, blood_pressure_data)  # Pasar nombre del usuario
        send_email_alert(user_email, "umxx fpsm grlx zsct", recipient_email, subject, message)

    return render_template('index.html', heart_data=heart_data, blood_pressure_data=blood_pressure_data)

if __name__ == '__main__':
    # Abrir el navegador en un hilo separado para evitar bloquear la aplicación
    threading.Timer(1.0, lambda: webbrowser.open('http://localhost:5000')).start()
    app.run(debug=True)