## Flare-FL

### Abstract
I present Flare-FL, a decentralized Federated Learning (FL) framework that uses the Flare chain and the Flare Data Connector to decentralize the training process with the objective of improving the security of the model and the privacy of the clients.

In particular, the Flare Data Connector allows user to submit an `Attestation Request`, which is evaluated by the `Attestation Providers`. The providers validate the request and vote to approve or reject it. If the request is approved, the partial updates (weights) are stored on the Flare chain. The global model is updated with the new weights thanks to the `Model Updater` smart contract.

Flare-FL allows to train a model across multiple clients, without sharing their data. The Flare chain is used to store the global model and the weights of the clients. The Flare Data Connector is used to store the data of the clients. The training process is divided into three phases: Collect, Choose, and Resolution. In the Collect phase, the client submits an Attestation Request to the Attestation Providers. In the Choose phase, the Attestation Providers choose which requests to accept. In the Resolution phase, the Attestation Providers evaluate the client's updated model and, if it is good enough, the new weights are stored on the Flare chain. The global model is updated with the new weights thanks to the Model Updater smart contract.
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
The client allows to generate 

```console
python 
```

### Install the frontend

```console
cd frontend
yarn install # requires yarn
yarn start
```

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

#### TO DO
- Refactor the server as there is duplicated code (`mlmodels`, `data` and `utils`).