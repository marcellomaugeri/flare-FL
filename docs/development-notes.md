### Generate the server
```console
openapi-generator-cli generate -i openapi.yaml -g python-flask -o server
```

### Run the server
```console
cd server
python3 -m openapi_server
```

### Generate the client
```console
openapi-python-client generate --path ./openapi.yaml  --output-path ./client_module
cd client_module
poetry build -f wheel
pip install --force-reinstall dist/*.whl
```

### Run the contracts
```console
npx hardhat run scripts/FlareFL.ts --network coston
```

### Add a model into the contract
```console
npx hardhat run-script --command createModel --network coston
```

### Query all the available models
```console
npx hardhat run-script --command get_all_models --network coston
```

### Submit an Attestation Request
```console
npx hardhat run-script --url https://8f18-163-1-81-192.ngrok-free.app --updateid 08f3ff0f9b98a5dcc3eb4b2c580da8d7d7e72a588f3813f6e7c87b4dbed24c30 --modelid cifar10  --command submitRequest --network coston
```

### Verify the status of an Attestation Request (get proof)
```console
npx hardhat run-script --url https://8f18-163-1-81-192.ngrok-free.app --updateid 08f3ff0f9b98a5dcc3eb4b2c580da8d7d7e72a588f3813f6e7c87b4dbed24c30 --modelid cifar10 --roundid 896393 --command getProof --network coston
```

### Submit a model update
```console
npx hardhat run-script --url https://8f18-163-1-81-192.ngrok-free.app --updateid 08f3ff0f9b98a5dcc3eb4b2c580da8d7d7e72a588f3813f6e7c87b4dbed24c30 --modelid cifar10 --roundid 896393 --command submitProof --network coston
```