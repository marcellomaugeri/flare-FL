## Flare-FL
Federated Learning allows to train a model across multiple clients, without sharing their data. However, classical FL has some limitations, such as the need for a central server to coordinate the training process. Flare-FL is a decentralized FL framework that uses the Flare chain and the Flare Data Connector to decentralize the training process.

### Repository Structure

TO DO

### Workflow
0. The client downloads the global model (weights) from the Flare chain.
1. The client trains the model on its local data.
2. [Collect Phase] The client submits an `Attestation Request` (and pays the fee) to 
3. [Choose Phase] Each `Attestation Provider` chooses which requests to accept. In particular, the `Attestation Provider` call a remote API to evaluate the client's updated model.
4. [Resolution Phase] If the `Attestation Provider` accepts the request, i.e. the client's model is good enough, the new weights are stored on the Flare chain.
5. The global model is updated with the new weights thanks to the `Model Updater` smart contract.

### User Workflow
0. The client downloads the global model (weights) from the Flare chain.
1. The client trains the model on its local data.
2. The client submits an `Attestation Request` (and pays the fee).
3. The client waits for the request to be accepted.
4. Once the `Model Updater` smart contract updates the global model, the client can download the new weights.
Repeat from step 1.

### Run the Validator Server

#### Install Python dependencies
```console
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Install the client

```console
cd src/client_module
poetry build -f wheel
pip install dist/*.whl
```

### Run the client

```console
python 


## Flare Hardhat Starter Kit

**IMPORTANT!!**
The supporting library uses Openzeppelin version `4.9.3`, be careful to use the documentation and examples from that library version.

### Getting started

If you are new to Hardhat please check the [Hardhat getting started doc](https://hardhat.org/hardhat-runner/docs/getting-started#overview)

1. Clone and install dependencies:

   ```console
   git clone https://github.com/marcellomaugeri/flare-FL
   cd flare-FL
   npm install
   ```

2. Set up `.env` file

   ```console
   mv .env.example .env
   ```

3. Change the `PRIVATE_KEY` in the `.env` file to yours

4. Change the `JQ_API_KEY` to `flare-oxford-2025` in the `.env` file

4. Compile the project

    ```console
    npx hardhat compile
    ```

    This will compile all `.sol` files in your `/contracts` folder. It will also generate artifacts that will be needed for testing. Contracts `Imports.sol` import MockContracts and Flare related mocks, thus enabling mocking of the contracts from typescript.

5. Run Tests

    ```console
    npx hardhat test
    ```

6. Deploy

    Check the `hardhat.config.ts` file, where you define which networks you want to interact with. Flare mainnet & test network details are already added in that file.

    Make sure that you have added API Keys in the `.env` file

   ```console
   npx hardhat run scripts/tryDeployment.ts
   ```

## Resources

- [Flare Developer Hub](https://dev.flare.network/)
- [Hardhat Docs](https://hardhat.org/docs)

