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

const TX_ID =
    "0xae295f8075754f795142e3238afa132cd32930f871d21ccede22bbe80ae31f73";

const MODEL_LIST_ADDRESS = "0x5F7EfACc8e26938E8C25A7EAC72D14059f0E764c"; // coston2

async function deployMainList() {
    const list: ModelsInstance = await Models.new();

    console.log("Char list deployed at:", list.address);
    // verify 
    const result = await run("verify:verify", {
        address: list.address,
        constructorArguments: [],
    })
}

//deployMainList().then((data) => {
//   process.exit(0);
//});


async function prepareRequest() {
    const attestationType = "0x" + toHex("IJsonApi");
    const sourceType = "0x" + toHex("WEB2");
    const requestData = {
        "attestationType": attestationType,
        "sourceId": sourceType,
        "requestBody": {
            "url": "http://c3d1-163-1-81-192.ngrok-free.app/validate_model?model=cifar10&weights=%2FUsers%2Fmarcellomaugeri%2FDocuments%2Fflare-FL%2Fsrc%2Fdata%2Fcifar10%2Fcifar10_weights.weights.h5",
            "postprocessJq": `{name: .model, weights: .weights} + (if (.error == null or .error == "") then {error: ""} else {error: .error} end)`,
        "abi_signature": `{
          \"components\": [
            {
              \"internalType\": \"string\",
              \"name\": \"name\",
              \"type\": \"string\"
            },
            {
              \"internalType\": \"bytes\",
              \"name\": \"weights\",
              \"type\": \"bytes\"
            },
            {
              \"internalType\": \"string\",
              \"name\": \"error\",
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
    console.log(JSON.stringify(requestData));

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


prepareRequest().then((data) => {
    console.log("Prepared request:", data);
    process.exit(0);
});

const firstVotingRoundStartTs = 1658429955;
const votingEpochDurationSeconds = 90;

async function submitRequest() {
    const requestData = await prepareRequest();

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
    console.log(
        `Check round progress at: https://coston-systems-explorer.flare.rocks/voting-epoch/${roundId}?tab=fdc`,
    );
    return roundId;
}

//submitRequest().then((data) => {
//    console.log("Submitted request:", data);
//    process.exit(0);
//});


const TARGET_ROUND_ID = 894447; // 0

async function getProof(roundId: number) {
    const request = await prepareRequest();
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

// getProof(TARGET_ROUND_ID)
//     .then((data) => {
//         console.log("Proof and data:");
//         console.log(JSON.stringify(data, undefined, 2));
//     })
//     .catch((e) => {
//         console.error(e);
//     });


async function submitProof() {
    const dataAndProof = await getProof(TARGET_ROUND_ID);
    console.log(dataAndProof);
    const starWarsList = await Models.at(MODEL_LIST_ADDRESS);

    const tx = await starWarsList.addCharacter({
        merkleProof: dataAndProof.proof,
        data: dataAndProof.response,
    });
    console.log(tx.tx);
    console.log(await starWarsList.getAllCharacters());
}


/*submitProof()
    .then((data) => {
        console.log("Submitted proof");
        process.exit(0);
    })
    .catch((e) => {
        console.error(e);
    });*/
