## Flare-FL: Federated Learning on the Flare Chain through the use of the Flare Data Connector
Submission for the `AI track`, `Flare`'s track `1` & `2`, and the `NERDo Awards` from `DeSci` at the `ETHOxford Hackathon 2025` by [@marcellomaugeri](https://github.com/marcellomaugeri).

### Awards 
- `NERDo Awards` for the `most likely to disrupt` project.

![Flare-FL Logo](./img/Flare-FL.jpg)

Disclaimer: the project is not affiliated with Flare, but the logo was greatly inspired since it is a submission for the Flare track. As a consequence, the logo is a derivative work of the Flare logo and it is not intended to be used for commercial purposes.

### Abstract
`Flare-FL` is a decentralized Federated Learning (FL) framework that uses the `Flare` chain and the `Flare Data Connector` to decentralize the training process with the objective of improving the security of the model and the privacy of the clients.

A user, called `Client`, can train a model on its local data. Then, it sends the model update to a `trusted third party (TTP)`. The `TTP` calculates a `SHA256` digest of the model and stores it in a db.

At this point, the `Client` can submit an `Attestation Request` to the `Attestation Providers`. The request contains the `SHA256` digest of the model update. The `Attestation Providers` queries the `TTP` to verify that the model update does not degrade the global model. According to the result, the `Attestation Providers` vote to approve or reject the request.
If the request is approved, the model update will be stored on the `Flare` chain.

The `TTP` is responsible for storing and maintaining the global model. For the sake of simplicity, currently the global model is fixed and not updated. However, the `TTP` can be extended easily to employ a strategy to update the global model (e.g. FedAvg).

### Workflow
![Flare-FL Workflow](./img/Workflow.png)

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

### Repository Summary

```
.
├── contracts
│   ├── FlareFL.sol # The FlareFL smart contract, the core of the project
|
├── scripts
│   ├── FlareFL.ts # The script to deploy and use the FlareFL smart contract
|
├── src
│   ├── client_module # The client module to communicate with the TTP)
│   ├── server # The TTP which validates and store the model updates (flask server)
|   ├── openapi.yaml # The OpenAPI specification of the TTP
|
├── demo.py # The demo script to show how the project works
```

### Getting started

1. Clone the repository
```console
git clone https://github.com/marcellomaugeri/flare-FL
cd flare-FL
```

2. Install Python dependencies
```console
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

3. Install hardhat, yarn and node.

4. Install the node dependencies
```console
npm install
```

5. Setup the `.env` file (Change the `PRIVATE_KEY` in the `.env` file to your wallet private key, and the `JQ_API_KEY` to `flare-oxford-2025`)
```console
mv .env.example .env
```

6. Compile the project
```console
npx hardhat compile
```

7. Install the client module
```console
cd src/client_module
poetry build -f wheel
pip install dist/*.whl
```

8. Install ngrok (dependent on the OS) and perform the initial setup

### Demo
The demo is designed to show how the project works.
1. At the beginning, it will spawn the `TTP` server (flask server) and a ngrok tunnel (to expose the TTP to the validators).
2. Then, it will run a simulation where the client trains a model and submits an attestation request to the validators.
3. The validators will query the TTP to verify the model update and vote to approve or reject the request.
4. Finally, the client will submit the model update to the Flare chain.
5. Once done, the client will query the Flare chain to get all the model updates and will aggregate them to its local model.
6. Then, it performs a round of testing to evaluate the performance of the model.

### To-do list
- Refactor the server as there is duplicated code (`mlmodels`, `data` and `utils`).
- Rewrite the tests (they are not working with latest changes).

### Ideas for the future
- Implement a strategy to maintain a global model (e.g. FedAvg).
- Design a DAO to choose the Attestation Providers.
- Implement a detection validator to detect adversarial updates.
- Provide incentives to the Attestation Providers and the participants.
- Replace the TTP with a decentralized solution (Flare is working on a feature to run a specific code).

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