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
    string model_id;
    string[] update_ids;
}

struct DataTransportObject {
    string model_id;
    string update_id;
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

    function addLocalUpdate(IJsonApi.Proof calldata data) public {
        require(isJsonApiProofValid(data), "Invalid proof");

        DataTransportObject memory dto = abi.decode(
            data.data.responseBody.abi_encoded_data,
            (DataTransportObject)
        );

        // Require that the model exists and the update_id unique
        require(
            bytes(models[dto.model_id].model_id).length > 0,
            "Model does not exist"
        );

        bool updateExists = false;
        for (uint i = 0; i < models[dto.model_id].update_ids.length; i++) {
            if (keccak256(abi.encodePacked(models[dto.model_id].update_ids[i])) == keccak256(abi.encodePacked(dto.update_id))) {
                updateExists = true;
                break;
            }
        }
        require(!updateExists, "Update already exists");

        // Append the update_id to the update_ids array
        models[dto.model_id].update_ids.push(dto.update_id);
    }

    function createModel(string memory model_id) public {
        // If the model already exists, do not allow it to be updated
        require(bytes(models[model_id].model_id).length == 0, "Model already exists");

        Model memory model = Model({
            model_id: model_id,
            update_ids: new string[](0)
        });
        models[model_id] = model;
        modelIds.push(model_id);
    }

    function getAllModels() public view returns (Model[] memory) {
        Model[] memory allModels = new Model[](modelIds.length); // Create an array in memory

        for (uint i = 0; i < modelIds.length; i++) {
            allModels[i] = models[modelIds[i]]; // Retrieve the model using the ID
        }  
        return allModels;
    }

    function getModel(string memory model_id) public view returns (Model memory) {
        require(bytes(models[model_id].model_id).length > 0, "Model does not exist");
        return models[model_id];
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

    //Empty, but needed to obtain the abi specification
    function setDataTransportObject(DataTransportObject memory dto) public {
    }
    
}
