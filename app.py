from flask import Flask, render_template, jsonify, redirect, url_for, request 
import ping3 as ping
import subprocess
import platform

app = Flask(__name__)

def ping_host(hostname):
    """Ping a host and return the result."""
    try:
        response = subprocess.run(
            ['ping', '-c', '4', hostname], 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE, 
            timeout=10  # Add a timeout in case the command hangs
        )
        if response.returncode == 0:
            return response.stdout.decode('utf-8')
        else:
            return f"Ping failed: {response.stderr.decode('utf-8')}"
    except subprocess.CalledProcessError as e:
        return f"Ping failed: {str(e)}"
    except Exception as e:
        return f"Error: {str(e)}"

def traceroute_host(hostname):
    """Perform traceroute and return the result."""
    try:
        response = subprocess.run(
            ['traceroute', hostname], 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE, 
            timeout=10  # Add a timeout in case the command hangs
        )
        if response.returncode == 0:
            return response.stdout.decode('utf-8')
        else:
            return f"Traceroute failed: {response.stderr.decode('utf-8')}"
    except subprocess.CalledProcessError as e:
        return f"Traceroute failed: {str(e)}"
    except Exception as e:
        return f"Error: {str(e)}"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    # Example: Validate the login credentials (this is just a simple check)
    if username == 'a' and password == '3':
        # If login is successful, redirect to a new page (e.g., dashboard)
        return redirect(url_for('main'))
    else:
        # If login fails, redirect back to the login page
        return redirect(url_for('monitor'))

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

@app.route('/monitor')
def monitor():
    """Render the network monitoring page."""
    return render_template('moniter.html')

@app.route('/network-monitor', methods=['GET'])
def network_monitor():
    """API endpoint to monitor network metrics (ping and traceroute)."""
    hostname = request.args.get('hostname', 'google.com')  # Default to google.com if no hostname is provided

    # Ping the host
    ping_result = ping_host(hostname)

    # Perform traceroute
    traceroute_result = traceroute_host(hostname)

    # Return results in JSON format
    return jsonify({
        'hostname': hostname,
        'ping': ping_result,
        'traceroute': traceroute_result
    })
    

if __name__ == '__main__':
    app.run(debug=True)
