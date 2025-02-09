## Flare-FL: Federated Learning on the Flare Chain through the use of the Flare Data Connector
Submission for the `AI track`, `Flare`'s track `1` & `2`, and the `NERDo Awards` from `DeSci` at the `ETHOxford Hackathon 2025` by [@marcellomaugeri](https://github.com/marcellomaugeri).

![Flare-FL Logo](./img/Flare-FL.jpg)
Disclaimer: the project is not affiliated with Flare, but the logo was greatly inspired since it is a submission for the Flare track. As a consequence, the logo is a derivative work of the Flare logo and it is not intended to be used for commercial purposes.

### Abstract
`Flare-FL` is a decentralized Federated Learning (FL) framework that uses the `Flare` chain and the `Flare Data Connector` to decentralize the training process with the objective of improving the security of the model and the privacy of the clients.

A user, called `Client`, can train a model on its local data. Then, it sends the model update to a `trusted third party (TTP)`. The `TTP` calculates a `SHA256` digest of the model and stores it in a db.

At this point, the `Client` can submit an `Attestation Request` to the `Attestation Providers`. The request contains the `SHA256` digest of the model update. The `Attestation Providers` queries the `TTP` to verify that the model update does not degrade the global model. According to the result, the `Attestation Providers` vote to approve or reject the request.
If the request is approved, the model update will be stored on the `Flare` chain.

The `TTP` is responsible for storing and maintaining the global model. For the sake of simplicity, currently the global model is fixed and not updated. However, the `TTP` can be extended easily to employ a strategy to update the global model (e.g. FedAvg).

### Contribution

The contribution of this project is two-fold:
1. `Federated Learning` inherently suffers from model poisoning attacks when malicious clients submit adversarial updates. The `Attestation Providers` act as validators to ensure that the model update is not malicious, by querying the `TTP` to verify that the model update does not degrade the global model.
2. The `Flare Data Connector` is used to store the model update digests on the `Flare` chain. This allows to decentralize the training process, improving the integrity of the model while preserving the privacy of the clients (as the training data is not shared).

### Limitations and Future Work
In the current implementation, the `Attestation Providers` simply query the `TTP` to verify the model update. However, in future works the `Attestation Providers` could be extended to employ more and different strategies to evaluate the model update.
For example, one `Attestation Provider` could use a detection algorithm to detect adversarial updates, while another `Attestation Provider` could use a different algorithm.
Another functionality that could be added is the institution of a `DAO` to choose which users are authorized to be `Attestation Providers` or request attestations.
The possibilities are endless and the `Flare` chain provides a solid foundation to build upon.


### Glossary and Entities
- `Client`: The client is the entity that trains the model on its local data.
- `Attestation Request`: The Attestation Request is a request submitted by the client to the Attestation Providers. It contains the local model of the client.
- `Attestation Provider`: The Attestation Provider is the entity that evaluates the Attestation Request. It queries the TTP to verify that the model update does not degrade the global model.
- `Trusted Third Party (TTP)`: The TTP is the entity that stores and maintains the global model. It is responsible for verifying that the model update does not degrade the global model.

### Repository Structure

TO DO AT THE END

### Demo

TO DO AT THE END -> Embed a youtube video

### Installation

TO DO

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

### Feedback about my experience with building on Flare.
I have been buzzling in blockchains only for a few months, and I have to say that building on Flare was a valuable experience. Despite being able to read Solidity code fluently, it was thanks to their starter kit that I was able to write and deploy my first (serious) smart contract.
My main difficulty was to understand what was happening on the `Attestation Provider` side, as the source code was not -- initially -- provided. However, the Flare team was very helpful and provided me a snippet. I cannot wait to see the future implementations of the `Attestation Providers`, in particular the feature which allows to run a specific code. If you know, you know.

### References
- [Flare Data Connector Whitepaper](https://flare.network/wp-content/uploads/FDC_WP_14012025.pdf)
- [The Flare Network Whitepaper](https://flare.network/wp-content/uploads/Flare-White-Paper-v2.pdf)
- [Flare Developer Hub](https://dev.flare.network/)
- [Hardhat Starter Kit](https://github.com/flare-foundation/flare-hardhat-starter)
- [Defending Against Poisoning Attacks in Federated Learning With Blockchain](https://doi.org/10.1109/TAI.2024.3376651)

### Acknowledgements
I would like to thank the Flare team for all the support and for developing the Flare chain and the Flare Data Connector, as well as organizing the two workshops. I would like to thank the DeSci team for providing me `Peter`, an AI assistant to whom I shared my thoughts and ideas. I would like to thank the ETHOxford Hackathon organizers for organizing this event and for the opportunity to participate. Finally, I would like to thank myself for the hard work, the dedication and the sleep I lost to build this project.