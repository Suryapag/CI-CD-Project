from flask import Flask, render_template, request
import subprocess

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run-script', methods=['POST'])
def run_script():
    # Run the shell script
    result = subprocess.run(['wsl', './script.sh'], capture_output=True, text=True)
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
        response_time = ping(host, timeout=2)
        
        if response_time is None:
            return jsonify({"status": "down", "host": host, "message": "Host is not reachable"}), 200
        else:
            return jsonify({"status": "up", "host": host, "response_time": response_time}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
