from flask import Flask, jsonify, render_template
import paramiko
from datetime import datetime
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

# Configuration for SFTP servers
sftp_servers = [
    {'name': 'sftp-1', 'hostname': os.getenv('SFTP_SERVER_HOSTNAME', '127.0.0.1'), 'port': int(os.getenv('SFTP_SERVER_1_PORT', 2222)), 'username': os.getenv('SFTP_SERVER_USERNAME', 'sftp'), 'password': os.getenv('SFTP_SERVER_PASSWORD', 'pass'), 'directory': os.getenv('SFTP_SERVER_DIRECTORY', '/uploads/')},
    {'name': 'sftp-2', 'hostname': os.getenv('SFTP_SERVER_HOSTNAME', '127.0.0.1'), 'port': int(os.getenv('SFTP_SERVER_2_PORT', 2200)), 'username': os.getenv('SFTP_SERVER_USERNAME', 'sftp'), 'password': os.getenv('SFTP_SERVER_PASSWORD', 'pass'), 'directory': os.getenv('SFTP_SERVER_DIRECTORY', '/uploads/')},
    {'name': 'sftp-3', 'hostname': os.getenv('SFTP_SERVER_HOSTNAME', '127.0.0.1'), 'port': int(os.getenv('SFTP_SERVER_3_PORT', 2201)), 'username': os.getenv('SFTP_SERVER_USERNAME', 'sftp'), 'password': os.getenv('SFTP_SERVER_PASSWORD', 'pass'), 'directory': os.getenv('SFTP_SERVER_DIRECTORY', '/uploads/')},
]


# Function to convert string to datetime for sorting logs
def convert_to_datetime(date_str, time_str):
    try:
        return datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M:%S")
    except ValueError:
        return None


# Fetch logs from an SFTP server
def fetch_logs_from_server(server):
    logs = []
    try:
        # Підключення до SFTP
        transport = paramiko.Transport((server['hostname'], server['port']))
        transport.connect(username=server['username'], password=server['password'])

        sftp = paramiko.SFTPClient.from_transport(transport)
        files = sftp.listdir(server['directory'])

        for file in files:
            if file.endswith('.txt'):  # Обробляємо тільки .txt файли
                with sftp.open(server['directory'] + file, 'r') as f:
                    content = f.read().strip()

                    # Перетворюємо в рядок, якщо тип даних - байти
                    if isinstance(content, bytes):
                        content = content.decode('utf-8')

                    logs.append({'filename': file, 'content': content})

        sftp.close()
        transport.close()
    except Exception as e:
        print(f"Помилка при отриманні логів з сервера {server['name']}: {e}")

    return logs


# Organize logs and count entries per sender
def process_logs(logs):
    sender_logs = {}
    sender_counts = {}

    for log in logs:
        try:
            date, time, sender_name = log['content'].split(', ')
            log_entry = {
                'filename': log['filename'],
                'date': date,
                'time': time,
                'sender_name': sender_name,
                'content': log['content']
            }
        except ValueError:
            log_entry = {'filename': log['filename'], 'content': log['content']}
            continue

        if sender_name not in sender_logs:
            sender_logs[sender_name] = []
            sender_counts[sender_name] = 0

        sender_logs[sender_name].append(log_entry)
        sender_counts[sender_name] += 1

    for sender_name in sender_logs:
        sender_logs[sender_name].sort(key=lambda x: convert_to_datetime(x['date'], x['time']) or datetime.min)

    return sender_logs, sender_counts


# Route to fetch logs and return as JSON
@app.route('/logs', methods=['GET'])
def fetch_logs():
    all_logs = {}

    for server in sftp_servers:
        logs = fetch_logs_from_server(server)
        sender_logs, sender_counts = process_logs(logs)

        all_logs[server['name']] = {
            'logs': sender_logs,
            'counts': sender_counts
        }

    return jsonify(all_logs)


# Route to fetch logs and render an HTML report
@app.route('/logs/html', methods=['GET'])
def fetch_logs_html():
    all_logs = {}

    for server in sftp_servers:
        logs = fetch_logs_from_server(server)
        sender_logs, sender_counts = process_logs(logs)

        all_logs[server['name']] = {
            'logs': sender_logs,
            'counts': sender_counts
        }

    return render_template('report.html', all_logs=all_logs)


if __name__ == '__main__':
    app.run(debug=True)
