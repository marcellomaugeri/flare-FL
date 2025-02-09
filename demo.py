import subprocess
import os
import signal
import sys
import time
import requests
import json
from src.models.cifar10 import get_model
from src.utils.cifar10_utils import load_data

from model_update_and_validation_api_client import Client
from model_update_and_validation_api_client.models import PostUpdateModelFromFileBodyModelId, PostUpdateModelBody, PostUpdateModelFromFileBodyModelId, PostUpdateModelResponse200
from model_update_and_validation_api_client.api.default import post_update_model
from model_update_and_validation_api_client.types import Response

@staticmethod
def print_red(message, end = '\n'): # color red
    sys.stderr.write('\x1b[1;31m' + message.strip() + '\x1b[0m' + end)

@staticmethod
def print_green(message, end = '\n'): # color green
    sys.stdout.write('\x1b[1;32m' + message.strip() + '\x1b[0m' + end)

@staticmethod
def print_yellow(message, end = '\n'): # color yellow
    sys.stderr.write('\x1b[1;33m' + message.strip() + '\x1b[0m' + end)

@staticmethod
def print_blue(message, end = '\n'): # color blue
    sys.stdout.write('\x1b[1;34m' + message.strip() + '\x1b[0m' + end)
    
@staticmethod
def print_bold(message, end = '\n'):
    sys.stdout.write('\x1b[1;37m' + message.strip() + '\x1b[0m' + end)

# --- Flask Server (in a separate process) ---
def run_flask_server() -> int:
    """Starts the Flask server in a separate process.
    Change the current path to src/server and then run python3 -m openapi_server"""
    # Change to the server directory
    current_dir = os.getcwd()
    server_dir = "src/server"
    os.chdir(server_dir)
    
    # Start the server in a separate process and close the stdin/stdout/stderr file descriptors
    process = subprocess.Popen([sys.executable, "-m", "openapi_server"], stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print_green(f"Flask server started with PID: {process.pid}")
    os.chdir(current_dir)  # Change back to the original directory
    return process.pid

# --- Ngrok (in a separate process) ---
def run_ngrok() -> tuple:
    """Starts ngrok in a separate process."""
    try:
        # Use 'ngrok http 5000' and capture output to get the forwarding URL
        process = subprocess.Popen(["ngrok", "http", "http://localhost:8080"], stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        # Wait 2 seconds for ngrok to start
        time.sleep(2)
        
        # Get the ngrok URL
        ngrok_url = requests.get("http://localhost:4040/api/tunnels").json()["tunnels"][0]["public_url"]
        
        print_green(f"ngrok started with PID: {process.pid}")
        print_green(f"ngrok URL: {ngrok_url}")
        return process.pid, ngrok_url

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
        self.models = []

    def restart_servers(self):
        """Restarts the Flask server and ngrok."""
        self.kill_servers()
        time.sleep(2) # Wait for the processes to terminate
        self.flask_pid = run_flask_server()
        self.ngrok_pid, self.ngrok_url = run_ngrok()

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
        # Run `npx hardhat run-script --command get_all_models --network coston` in a subprocess, wait for it and get the final line
        process = subprocess.Popen(["npx", "hardhat", "run-script", "--command", "get_all_models", "--network", "coston"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        if process.returncode != 0:
            print_red(f"Error: {stderr.decode()}")
            return
        
        # Get every model and create a list. The last line should be
        # [ 'cifar10' 'other_model' ]
        self.models = stdout.decode().splitlines()[-1].strip("[ ]").replace("'", "").split(", ")
        print("Available Models:")
        for i, model in enumerate(self.models):
            print_green(f"{i+1}. {model}")
        
    def train_model(self):
        """Initiates model training."""
        if not self.models:
            print("No models available to train. Press 1 to query the smart contract.")
            return
        print("Available Models:")
        for i, model in enumerate(self.models):
            print_green(f"{i+1}. {model}")

        while True:
            try:
                model_choice = int(input("Enter the number of the model to train: "))
                if 1 <= model_choice <= len(self.models):
                    model_name = self.models[model_choice - 1]
                    break
                else:
                    print("Invalid model number. Please try again.")
            except ValueError:
                print("Invalid input. Please enter a number.")

        print(model_name)
        
        partitions = [
            "src/data/cifar10/data_batch_1",
            "src/data/cifar10/data_batch_2",
            "src/data/cifar10/data_batch_3",
            "src/data/cifar10/data_batch_4",
            "src/data/cifar10/data_batch_5",
        ]
        
        for i, partition in enumerate(partitions):
            print_green(f"{i+1}. {partition}")

        while True:
            try:
                partition_choice = int(input("Enter the number of the model to train: "))
                if 1 <= partition_choice <= len(partitions):
                    partition_path = partitions[partition_choice - 1]
                    break
                else:
                    print("Invalid model number. Please try again.")
            except ValueError:
                print("Invalid input. Please enter a number.")
        
        model = get_model()
        features, labels = load_data(partition_path)
        model.fit(features, labels, epochs=1, batch_size=32)
        model.save_weights("/tmp/temp.weights.h5")
        # Run the training script in a subprocess        

    def validate_update(self):
        """Validates a model update."""
        client = Client("http://localhost:8080")
        
        with open("/tmp/temp.weights.h5", 'rb') as f:
            weights64 = f.read().hex()
            
        model_id = PostUpdateModelFromFileBodyModelId.CIFAR10
    
        request_body : PostUpdateModelBody = PostUpdateModelBody(model_id=model_id, hex_weights=weights64)
        
        response : Response = post_update_model.sync_detailed(client=client, body=request_body)
        
        if not isinstance(response.parsed, PostUpdateModelResponse200):
            print_red("Error: {response.status_code}")
        else:
            print_green(f"Update ID: {response.parsed.update_id} use it for validation")
            
        # npx hardhat run-script --command validate --updateId 08f3ff0f9b98a5dcc3eb4b2c580da8d7d7e72a588f3813f6e7c87b4dbed24c30 --modelId cifar10 --url https://1419-163-1-81-192.ngrok-free.app and print the last line received
        
        process = subprocess.Popen(["npx", "hardhat", "run-script", "--command", "validate", "--update_id", response.parsed.update_id, "--model_id", model_id, "--url", self.ngrok_url,  "--network", "coston"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        if process.returncode != 0:
            print_red(f"Error: {stderr.decode()}")
            return
        
        # Get every model and create a list. The last line should be
        # [ 'cifar10' 'other_model' ]
        print_green(f"Transaction: {stdout.decode().splitlines()[-1]}")
        


    def see_status(self):
        """Checks the status of a transaction."""
        tx_hash = input("Enter the transaction hash: ")
        status = self.smart_contract.get_transaction_status(tx_hash)
        print(f"Transaction status: {status}")


    def run(self):
        """Main loop to accept and process commands."""
        self.flask_pid = run_flask_server()
        
        self.ngrok_pid, self.ngrok_url = run_ngrok()
        
        while True:
            print("")
            print_bold("\nCommands:\n")
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
