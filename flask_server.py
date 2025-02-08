
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

            