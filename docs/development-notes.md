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