import { artifacts, ethers, run } from "hardhat";
import { ModelsInstance } from "../typechain-types";

const Models = artifacts.require("Models");
const FDCHub = artifacts.require("@flarenetwork/flare-periphery-contracts/coston/IFdcHub.sol:IFdcHub");

// Simple hex encoding
function toHex(data) {
    var result = "";
    for (var i = 0; i < data.length; i++) {
        result += data.charCodeAt(i).toString(16);
    }
    return result.padEnd(64, "0");
}

const { JQ_VERIFIER_URL_TESTNET, JQ_API_KEY, VERIFIER_URL_TESTNET, VERIFIER_PUBLIC_API_KEY_TESTNET, DA_LAYER_URL_COSTON } = process.env;

const TX_ID = "0xe28502595518c91d8b65392af5abe27ab81f819e9083f5d37c1c85958dec09d7";

// The address of the contract
const MODEL_LIST_ADDRESS = "0x86861573AAe42FBD7F0BE0A0EDC1f727A787e207"; 

// Constants for voting rounds
const firstVotingRoundStartTs = 1658429955;
const votingEpochDurationSeconds = 90;


// Code to deploy the contract. Not needed anymore
async function deploy() {
    const list: ModelsInstance = await Models.new();

    console.log("Char list deployed at:", list.address);
    // verify 
    const result = await run("verify:verify", {
        address: list.address,
        constructorArguments: [],
    })
    return result;
}

/*deployMainList().then((data) => {
   process.exit(0);
});*/


async function prepareRequest(url: string, update_id: string,  modelId: string = "cifar10") {
    const attestationType = "0x" + toHex("IJsonApi");
    const sourceType = "0x" + toHex("WEB2");
    const requestData = {
        "attestationType": attestationType,
        "sourceId": sourceType,
        "requestBody": {
            "url": url+"/validate?model_id="+modelId+"&update_id="+update_id,
            "postprocessJq": `{model_id: .model_id, update_id: .update_id}`,
        "abi_signature": `{
          \"components\": [
            {
              \"internalType\": \"string\",
              \"name\": \"model_id\",
              \"type\": \"string\"
            },
            {
              \"internalType\": \"string\",
              \"name\": \"update_id\",
              \"type\": \"string\"
            }
          ],
          \"internalType\": \"struct DataTransportObject\",
          \"name\": \"dto\",
          \"type\": \"tuple\"
        }`
        }
    };

    // Print JSON.stringify(requestData),
    //console.log(JSON.stringify(requestData));

    const response = await fetch(
        `${JQ_VERIFIER_URL_TESTNET}JsonApi/prepareRequest`,
        {
            method: "POST",
            headers: {
                "X-API-KEY": JQ_API_KEY,
                "Content-Type": "application/json",
            },
            body: JSON.stringify(requestData),
        },
    );

    const data = response.json();
    return data;
}

// Code to prepare the request
/*
prepareRequest().then((data) => {
    console.log("Prepared request:", data);
    process.exit(0);
});*/



async function submitRequest(url: string, update_id: string, modelId: string = "cifar10") {
    const requestData = await prepareRequest(url, update_id, modelId);

    const modelList: ModelsInstance = await Models.at(MODEL_LIST_ADDRESS);


    const fdcHUB = await FDCHub.at(await modelList.getFdcHub());

    // Call to the FDC Hub protocol to provide attestation.
    const tx = await fdcHUB.requestAttestation(requestData.abiEncodedRequest, {
        value: ethers.parseEther("1").toString(),
    });
    console.log("Submitted request:", tx.tx);

    // Get block number of the block containing contract call
    const blockNumber = tx.blockNumber;
    const block = await ethers.provider.getBlock(blockNumber);

    // Calculate roundId
    const roundId = Math.floor(
        (block!.timestamp - firstVotingRoundStartTs) / votingEpochDurationSeconds,
    );
    /*console.log(
        `Check round progress at: https://coston-systems-explorer.flare.rocks/voting-epoch/${roundId}?tab=fdc`,
    );*/
    return roundId;
}

/*submitRequest().then((data) => {
    console.log("Submitted request:", data);
    process.exit(0);
});*/


//const TARGET_ROUND_ID = 896134; // 0

async function getProof(roundId: number, url: string, update_id: string, modelId: string = "cifar10") {
    const request = await prepareRequest(url, update_id, modelId);
    const proofAndData = await fetch(
        `${DA_LAYER_URL_COSTON}fdc/get-proof-round-id-bytes`,
        {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                // "X-API-KEY": API_KEY,
            },
            body: JSON.stringify({
                votingRoundId: roundId,
                requestBytes: request.abiEncodedRequest,
            }),
        },
    );

    return await proofAndData.json();
}

/*getProof(TARGET_ROUND_ID)
    .then((data) => {
        console.log("Proof and data:");
        console.log(JSON.stringify(data, undefined, 2));
    })
    .catch((e) => {
        console.error(e);
    });*/


async function submitProof(roundId: number, url: string, update_id: string, modelId: string = "cifar10") {
    const dataAndProof = await getProof(roundId, url, update_id, modelId);
    //console.log(dataAndProof);
    const modelList = await Models.at(MODEL_LIST_ADDRESS);

    const tx = await modelList.addLocalUpdate({
        merkleProof: dataAndProof.proof,
        data: dataAndProof.response,
    });
    //console.log(tx.tx);
    //console.log(await modelList.getAllModels());
}

// Call the contract to create a model with a string identifier
async function createModel(modelId: string) {
    const modelList = await Models.at(MODEL_LIST_ADDRESS);
    const tx = await modelList.createModel(modelId);
    console.log(tx.tx);
}

// Example usage
/*createModel("cifar10")
    .then(() => {
        console.log("Model created successfully");
        process.exit(0);
    })
    .catch((e) => {
        console.error(e);
        process.exit(1);
    });*/

async function get_all_model_updates(modelId: string) {
    const modelList = await Models.at(MODEL_LIST_ADDRESS);
    const updates = await modelList.getAllModelUpdates(modelId);
    return updates;
}

// Parse the command line arguments:
//.addParam("url", "The URL of the TTP (ngrok)")
// .addParam("updateId", "The update ID - the digest of the model update")
// .addOptionalParam("modelId", "The model ID - the string identifier of the model")
// .addOptionalParam("roundId", "The round ID - the round ID of the voting round")
// .addParam("command", "The command to run")
async function main(url: string, updateId: string, modelId: string = "cifar10", roundId: string, command: string) {
    // Switch on the command
    switch (command) {
        case "prepareRequest":
            await prepareRequest(url, updateId, modelId);
            break;
        case "submitRequest":
            await submitRequest(url, updateId, modelId);
            break;
        case "getProof":
            await getProof(parseInt(roundId), url, updateId, modelId);
            break;
        case "submitProof":
            await submitProof(parseInt(roundId), url, updateId, modelId);
            break;
        case "createModel":
            await createModel(modelId);
            break;
        case "get_all_model_updates":
            const updates = await get_all_model_updates(modelId);
            break;
        case "deploy":
            const address = await deploy();
            console.log("Deployed contract address:", address);
            break;
        default:
            throw new Error(`Unknown command: ${command}`);
    }
}

// Export the main function as the default export
export default main;