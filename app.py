from flask import Flask, render_template, jsonify, redirect, url_for, request 
import ping3 as ping
import subprocess
import platform

app = Flask(__name__)

network_metrics={}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    # Example: Validate the login credentials (this is just a simple check)
    if username != 'a' and password != '3':
        # If login is successful, redirect to a new page (e.g., dashboard)
        return redirect(url_for('main'))
    else:
        # If login fails, redirect back to the login page
        return redirect(url_for('login_form'))

# Route for the dashboard (the page to redirect after successful login)
@app.route('/main')
def main():
    return render_template('main.html')

@app.route('/run-script', methods=['POST'])
def run_script():
    # Run the shell script
    result = subprocess.run(['C:/Program Files/Git/bin/bash.exe', './script.sh'], capture_output=True, text=True)
    output = result.stdout  # Capture the output
    return output  # Send the output back to the front end

# Define an API endpoint to monitor the network status of a server
@app.route('/monitor', methods=['GET'])
def monitor():
    try:
        # Get the IP or hostname from the request arguments (e.g., ?host=8.8.8.8)
        host = request.args.get('host', None)
        
        if not host:
            return jsonify({"error": "Host is required"}), 400

        # Ping the host to check its availability
        response_time = ping.ping(host, timeout=2)
        
        if response_time is None:
            return jsonify({"status": "down", "host": host, "message": "Host is not reachable"}), 200
        else:
            return jsonify({"status": "up", "host": host, "response_time": response_time}), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Define an API endpoint to perform traceroute
@app.route('/traceroute', methods=['GET'])
def traceroute():
    try:
        # Get the IP or hostname from the request arguments (e.g., ?host=google.com)
        host = request.args.get('host', None)

        if not host:
            return jsonify({"error": "Host is required"}), 400
        
        # Use 'tracert' for Windows and 'traceroute' for Unix-based systems
        traceroute_command = ["tracert", host] if platform.system() == "Windows" else ["traceroute", host]
        result = subprocess.run(traceroute_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        if result.returncode == 0:
            return jsonify({"status": "success", "traceroute_output": result.stdout.splitlines()}), 200
        else:
            return jsonify({"status": "error", "error_message": result.stderr}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
# API endpoint to get stored metrics
@app.route('/metrics', methods=['GET'])
def get_metrics():
    return jsonify(network_metrics), 200  # Return the stored metrics
    

if __name__ == '__main__':
    app.run(debug=True)
