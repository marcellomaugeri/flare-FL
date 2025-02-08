// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import {ContractRegistry} from "@flarenetwork/flare-periphery-contracts/coston/ContractRegistry.sol";

// Dummy import to get artifacts for IFDCHub
import {IFdcHub} from "@flarenetwork/flare-periphery-contracts/coston/IFdcHub.sol";
import {IFdcRequestFeeConfigurations} from "@flarenetwork/flare-periphery-contracts/coston/IFdcRequestFeeConfigurations.sol";

import {IJsonApiVerification} from "@flarenetwork/flare-periphery-contracts/coston/IJsonApiVerification.sol";
import {IJsonApi} from "@flarenetwork/flare-periphery-contracts/coston/IJsonApi.sol";

//import "@openzeppelin/contracts/utils/cryptography/MerkleProof.sol";

struct Model {
    string identifier;
    bytes weights;
}

struct DataTransportObject {
    string name;
    bytes weights;
    string error;
}

contract Models {
    mapping(string => Model) public models;
    string[] public modelIds;

    function isJsonApiProofValid(
        IJsonApi.Proof calldata _proof
    ) public view returns (bool) {
        // Inline the check for now until we have an official contract deployed
        return
            ContractRegistry.auxiliaryGetIJsonApiVerification().verifyJsonApi(
                _proof
            );
    }

    function addModel(IJsonApi.Proof calldata data) public {
        require(isJsonApiProofValid(data), "Invalid proof");

        DataTransportObject memory dto = abi.decode(
            data.data.responseBody.abi_encoded_data,
            (DataTransportObject)
        );

        // Require error to be empty
        require(bytes(dto.error).length == 0, "Error in data");

        // TODO: Check if model already exists? Not sure if this is needed, the API already does it

        // Perform the model update by storing the weights

        Model memory model = Model({
            identifier: dto.name,
            weights: dto.weights
        });
        models[dto.name] = model;
        modelIds.push(dto.name);
    }

    function createModel(string memory identifier, bytes memory weights) public {
        Model memory model = Model({
            identifier: identifier,
            weights: weights
        });
        models[identifier] = model;
        modelIds.push(identifier);
    }

    function getAllModels() public view returns (Model[] memory) {
        Model[] memory allModels = new Model[](modelIds.length); // Create an array in memory

        for (uint i = 0; i < modelIds.length; i++) {
            allModels[i] = models[modelIds[i]]; // Retrieve the model using the ID
        }  
        return allModels;
    }

    function getModel(string memory identifier) public view returns (Model memory) {
        return models[identifier];
    }

    function getFdcHub() external view returns (IFdcHub) {
        return ContractRegistry.getFdcHub();
    }

    function getFdcRequestFeeConfigurations()
        external
        view
        returns (IFdcRequestFeeConfigurations)
    {
        return ContractRegistry.getFdcRequestFeeConfigurations();
    }
}
