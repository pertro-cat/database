#config/config.py
import yaml
from flask import Flask
import mysql.connector

app = Flask(__name__)

# Завантаження конфігурації з файлу app.yml
with open("config/app.yml", "r") as config_file:
    config = yaml.safe_load(config_file)

# Налаштування параметрів бази даних
db_config = {
    'host': config['mysql']['host'],
    'user': config['mysql']['user'],
    'password': config['mysql']['password'],
    'database': config['mysql']['database'],
    'port': config['mysql']['port']
}

# Функція для підключення до бази даних
def get_db_connection():
    connection = mysql.connector.connect(**db_config)
    return connection

@app.route('/')
def home():
    return 'Hello, Flask + MySQL!'

if __name__ == '__main__':
    app.run(debug=True)
