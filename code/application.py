from flask import Flask, url_for, render_template, request, redirect, make_response, abort, send_from_directory
import logging
import logging.handlers
import os
import sys
from time import gmtime, strftime
import json
import urllib.parse

app = Flask(__name__, template_folder='templates')
HONEYPOT = 60
available_paths = ['/forgot', '/login', '/dashboard', '/machine', '/status', '/users', '/administration', '/', '/static/css/style.css', '/static/img/user.png', '/robots.txt']

@app.before_request
def log_request():
    if not request.is_secure:
        url = request.url.replace('http://', 'https://', 1)
        code = 301
        return redirect(url, code=code)

    if request.path not in available_paths:
        data = {}
        data['client_ip'] = request.remote_addr
        data['client_port'] = request.environ['REMOTE_PORT']
        data['timestamp'] = get_timestamp()
        data['method'] = request.method
        data['path'] = request.path
        data['status_code'] = 404
        data['get_data'] = urllib.parse.urlencode(request.args)
        data['post_data'] = urllib.parse.urlencode(request.form)
        #data['user_agent'] = request.headers.get('User-Agent')
        logging.critical(json.dumps(data))
        print(data)


@app.route('/robots.txt')
def robots():
    data = {}
    data['client_ip'] = request.remote_addr
    data['client_port'] = request.environ['REMOTE_PORT']
    data['timestamp'] = get_timestamp()
    data['method'] = request.method
    data['path'] = request.path
    data['status_code'] = 200
    data['get_data'] = urllib.parse.urlencode(request.args)
    data['post_data'] = urllib.parse.urlencode(request.form)
    #data['user_agent'] = request.headers.get('User-Agent')
    logging.critical(json.dumps(data))
    print(data)
    return send_from_directory('/app/static', 'robots.txt')

@app.route('/', methods=['GET'])
def index():
    data = {}
    data['client_ip'] = request.remote_addr
    data['client_port'] = request.environ['REMOTE_PORT']
    data['timestamp'] = get_timestamp()
    data['method'] = request.method
    data['path'] = request.path
    data['status_code'] = 302
    data['get_data'] = urllib.parse.urlencode(request.args)
    data['post_data'] = urllib.parse.urlencode(request.form)
    #data['user_agent'] = request.headers.get('User-Agent')
    logging.critical(json.dumps(data))
    print(data)

    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        data = {}
        data['client_ip'] = request.remote_addr
        data['client_port'] = request.environ['REMOTE_PORT']
        data['timestamp'] = get_timestamp()
        data['method'] = request.method
        data['path'] = request.path
        data['status_code'] = 200
        data['get_data'] = urllib.parse.urlencode(request.args)
        data['post_data'] = urllib.parse.urlencode(request.form)
        #data['user_agent'] = request.headers.get('User-Agent')
        logging.critical(json.dumps(data))
        print(data)
        return render_template('login.html')
    else:
        data = {}
        data['web_username'] = request.form['username']
        data['web_password'] = request.form['password']
        data['client_ip'] = request.remote_addr
        data['client_port'] = request.environ['REMOTE_PORT']
        data['timestamp'] = get_timestamp()
        data['method'] = request.method
        data['path'] = request.path
        data['status_code'] = 401
        data['get_data'] = urllib.parse.urlencode(request.args)
        data['post_data'] = urllib.parse.urlencode(request.form)
        #data['user_agent'] = request.headers.get('User-Agent')
        logging.critical(json.dumps(data))
        print(data)

        return render_template('login.html', result="Incorrect credentials"), 401

@app.route('/forgot', methods=['GET'])
def forgot_get():
    data = {}
    data['client_ip'] = request.remote_addr
    data['client_port'] = request.environ['REMOTE_PORT']
    data['timestamp'] = get_timestamp()
    data['method'] = request.method
    data['path'] = request.path
    data['status_code'] = 302
    data['get_data'] = urllib.parse.urlencode(request.args)
    data['post_data'] = urllib.parse.urlencode(request.form)
    #data['user_agent'] = request.headers.get('User-Agent')
    logging.critical(json.dumps(data))
    print(data)

    return render_template('forgot.html', result=""), 200

@app.route('/forgot', methods=['POST'])
def forgot_post():
    data = {}
    data['forgot_email'] = request.form['email']
    data['client_ip'] = request.remote_addr
    data['client_port'] = request.environ['REMOTE_PORT']
    data['timestamp'] = get_timestamp()
    data['method'] = request.method
    data['path'] = request.path
    data['status_code'] = 302
    data['get_data'] = urllib.parse.urlencode(request.args)
    data['post_data'] = urllib.parse.urlencode(request.form)
    #data['user_agent'] = request.headers.get('User-Agent')
    logging.critical(json.dumps(data))
    print(data)

    return render_template('forgot.html', result="If this email exists in the database, you will receive an email with the link to change your password"), 200

@app.route('/dashboard')
def dashboard():
    send_restricted_folder_access()
    return redirect(url_for('login', code=401))

@app.route('/machine')
def machine():
    send_restricted_folder_access()
    return redirect(url_for('login', code=401))

@app.route('/status')
def status():
    send_restricted_folder_access()
    return redirect(url_for('login', code=401))

@app.route('/users')
def users():
    send_restricted_folder_access()
    return redirect(url_for('login', code=401))

@app.route('/administration')
def administration():
    send_restricted_folder_access()
    return redirect(url_for('login', code=401))

def send_restricted_folder_access():
    data = {}
    data['client_ip'] = request.remote_addr
    data['client_port'] = request.environ['REMOTE_PORT']
    data['timestamp'] = get_timestamp()
    data['method'] = request.method
    data['path'] = request.path
    data['status_code'] = 401
    data['get_data'] = urllib.parse.urlencode(request.args)
    data['post_data'] = urllib.parse.urlencode(request.form)
    #data['user_agent'] = request.headers.get('User-Agent')
    logging.critical(json.dumps(data))
    print(data)

def get_timestamp():
    timestamp = request.environ.get("time")
    timestamp_struct = gmtime(timestamp)
    timestamp_string = strftime("%Y-%m-%d %H:%M:%S", timestamp_struct)
    return timestamp_string
    
if __name__ == '__main__':
    logging.basicConfig(filename='/app/logs/honeypot.json', level=logging.CRITICAL, format='%(message)s')
    logger = logging.getLogger()
    logger.setLevel(logging.CRITICAL)
    logging.getLogger("werkzeug").setLevel(logging.ERROR)

    app.run(port=443, host='0.0.0.0', ssl_context=('/app/ssl/cert.pem', '/app/ssl/key.pem'))
