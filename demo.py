import subprocess
import os
import signal
import sys
import time
import requests
import json
from threading import Thread
# Dummy implementations for Smart Contract interactions (replace with your actual logic)
class SmartContract:
    def list_models(self):
        # Replace with your actual smart contract interaction
        # Example:  return ["model_a", "model_b", "model_c"]
        print("Querying smart contract for available models...")
        time.sleep(1)  # Simulate network latency
        return ["model_a", "model_b", "model_c"]
    def get_transaction_status(self, tx_hash):
        # Replace with your actual smart contract interaction
        # Example: return "pending", "approved", or "rejected"
        print(f"Querying smart contract for transaction status: {tx_hash}")
        time.sleep(1)  # Simulate network latency
        # Simulate different states for demonstration
        if int(time.time()) % 3 == 0:
            return "pending"
        elif int(time.time()) % 3 == 1:
            return "approved"
        else:
            return "rejected"
    def train_model(self, model_name, dataset_partition):
        print(f"Simulating smart contract call for training request on model {model_name} on parition {dataset_partition}")
        time.sleep(1)
        # Replace with actual call and return a dummy transaction hash for now.
        return "0x" + os.urandom(32).hex() # Generate a random hex string
    def validate_update(self, model_update_data):
        print(f"Simulating smart contract call for update validation of model {model_update_data}")
        time.sleep(1)
        # Replace this with actual validation logic and smart contract interaction
        # Return a dummy transaction hash
        return "0x" + os.urandom(32).hex()

# --- Flask Server (in a separate process) ---
def run_flask_server():
    """Starts the Flask server in a separate process."""
    flask_app_path = "flask_server.py"  # Path to your Flask app file
    # check flask_server.py exists
    if not os.path.exists(flask_app_path):
        with open(flask_app_path, "w") as f:
            f.write("""
from flask import Flask, request, jsonify
app = Flask(__name__)
@app.route('/train', methods=['POST'])
def train():
    model_name = request.json.get('model_name')
    dataset_partition = request.json.get('dataset_partition')
    #replace with you training procedure
    print(f"Received training request for model: {model_name}, partition: {dataset_partition}")
    return jsonify({"message": f"Training started for {model_name} on {dataset_partition}"}), 200
if __name__ == '__main__':
    app.run(debug=True, port=5000, use_reloader=False)  # Disable reloader in subprocess

            """)
    process = subprocess.Popen([sys.executable, flask_app_path])
    return process.pid

# --- Ngrok (in a separate process) ---
def run_ngrok():
    """Starts ngrok in a separate process."""
    try:
        # Use 'ngrok http 5000' and capture output to get the forwarding URL
        process = subprocess.Popen(["ngrok", "http", "5000"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # Wait briefly for ngrok to start and then try to get the URL
        time.sleep(2)  # Adjust as needed

        # Check if ngrok is still running.  If there's an error (like ngrok not installed),
        # it will likely exit very quickly.
        if process.poll() is not None:
            error_output = process.stderr.read().decode()
            print(f"Error starting ngrok: {error_output}")
            return None, None

        # A more robust way to get the URL is to use the ngrok API, if available.
        # This method avoids parsing the text output.
        try:
            response = requests.get("http://localhost:4040/api/tunnels")
            response.raise_for_status()  # Raise an exception for bad status codes
            tunnels = response.json()["tunnels"]
            public_url = tunnels[0]["public_url"] # Choose https
            print(f"Ngrok forwarding: {public_url} -> http://localhost:5000")
            return process.pid, public_url
        except (requests.RequestException, KeyError, IndexError) as e:
            print(f"Error getting ngrok URL: {e}")
            # Kill the process since we couldn't get the URL.
            os.kill(process.pid, signal.SIGTERM)
            return None, None


    except FileNotFoundError:
        print("Error: ngrok not found. Make sure it's installed and in your PATH.")
        return None, None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None, None

# --- Main Application Logic ---

class CommandLineApp:
    def __init__(self):
        self.flask_pid = None
        self.ngrok_pid = None
        self.ngrok_url = None
        self.smart_contract = SmartContract()
        self.start_servers()

    def start_servers(self):
        """Starts the Flask server and ngrok."""
        print("Starting Flask server...")
        self.flask_pid = run_flask_server()
        print(f"Flask server PID: {self.flask_pid}")

        print("Starting ngrok...")
        self.ngrok_pid, self.ngrok_url = run_ngrok()
        if self.ngrok_pid:
            print(f"Ngrok PID: {self.ngrok_pid}")

    def restart_servers(self):
        """Restarts the Flask server and ngrok."""
        self.kill_servers()
        time.sleep(2) # Wait for the processes to terminate
        self.start_servers()


    def kill_servers(self):
        """Kills the Flask server and ngrok processes."""
        if self.flask_pid:
            try:
                print(f"Killing Flask server (PID: {self.flask_pid})...")
                os.kill(self.flask_pid, signal.SIGTERM)  # Or signal.SIGKILL
            except ProcessLookupError:
                print("Flask server process not found.")
            self.flask_pid = None

        if self.ngrok_pid:
            try:
                print(f"Killing ngrok (PID: {self.ngrok_pid})...")
                os.kill(self.ngrok_pid, signal.SIGTERM)
            except ProcessLookupError:
                print("Ngrok process not found.")
            self.ngrok_pid = None


    def list_available_models(self):
        """Lists available models from the smart contract."""
        models = self.smart_contract.list_models()
        print("Available Models:")
        for model in models:
            print(f"- {model}")

    def train_model(self):
        """Initiates model training."""
        models = self.smart_contract.list_models()
        if not models:
            print("No models available to train.")
            return
        print("Available Models:")
        for i, model in enumerate(models):
            print(f"{i+1}. {model}")

        while True:
            try:
                model_choice = int(input("Enter the number of the model to train: "))
                if 1 <= model_choice <= len(models):
                    model_name = models[model_choice - 1]
                    break
                else:
                    print("Invalid model number. Please try again.")
            except ValueError:
                print("Invalid input. Please enter a number.")

        dataset_partition = input("Enter the dataset partition to use: ")

        if not self.ngrok_url:
            print("Ngrok URL not available.  Cannot send training request.")
            return

        # Send request to Flask server via ngrok
        try:
            url = f"{self.ngrok_url}/train"
            headers = {"Content-Type": "application/json"}
            data = {"model_name": model_name, "dataset_partition": dataset_partition}
            response = requests.post(url, headers=headers, data=json.dumps(data))
            response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
            print(response.json()["message"])

            # Now interact with smart contract after successful request to flask
            tx_hash = self.smart_contract.train_model(model_name, dataset_partition)
            print(f"Training request submitted.  Transaction hash: {tx_hash}")

        except requests.RequestException as e:
            print(f"Error sending training request: {e}")



    def validate_update(self):
        """Validates a model update."""
        model_update_data = input("Enter the model update data: ")  # Get update data
        tx_hash = self.smart_contract.validate_update(model_update_data)
        print(f"Validation request submitted. Transaction hash: {tx_hash}")


    def see_status(self):
        """Checks the status of a transaction."""
        tx_hash = input("Enter the transaction hash: ")
        status = self.smart_contract.get_transaction_status(tx_hash)
        print(f"Transaction status: {status}")


    def run(self):
        """Main loop to accept and process commands."""
        while True:
            print("\nAvailable Commands:")
            print("0. Restart the server")
            print("1. List available models")
            print("2. Train a model")
            print("3. Validate an update")
            print("4. See status")
            print("5. Exit")

            choice = input("Enter your choice: ")

            try:
                if choice == '0':
                    self.restart_servers()
                elif choice == '1':
                    self.list_available_models()
                elif choice == '2':
                    self.train_model()
                elif choice == '3':
                    self.validate_update()
                elif choice == '4':
                    self.see_status()
                elif choice == '5':
                    self.kill_servers()
                    print("Exiting...")
                    break
                else:
                    print("Invalid choice. Please try again.")
            except Exception as e:
                print(f"An error occurred: {e}")

if __name__ == "__main__":
    app = CommandLineApp()
    try:
        app.run()
    finally:
        app.kill_servers() # Ensure processes are killed on exit