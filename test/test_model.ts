import { expect } from "chai";
import { ethers } from "hardhat";
import { Models, Models__factory } from "../typechain-types"; // Adjust path as needed

describe("Models Contract (TypeScript)", function () {
    let models: Models;

    beforeEach(async function () {
        const ModelsFactory = (await ethers.getContractFactory("Models")) as Models__factory;
        models = await ModelsFactory.deploy();
        await models.waitForDeployment(); // Use waitForDeployment() instead
    });

    it("Should create a new model", async function () {
        const modelName = "CIFAR10";
        const modelWeights = "0xa1b2c3d4"; // Example fixed byte weight (as a hex string)

        await models.createModel(modelName, modelWeights);

        // Get the model and check its properties
        const retrievedModel = await models.getModel(modelName);
        expect(retrievedModel.identifier).to.equal(modelName);
        expect(retrievedModel.weights).to.equal(modelWeights);

        // Check if the model ID was added to the array
        expect(await models.modelIds(0)).to.equal(modelName);
    });

    it("Should not overwrite an existing model with the same name", async function () {
        const modelName = "CIFAR10";
        const newWeights = "0x05060708";

        models.createModel(modelName, newWeights);

        await expect (models.createModel(modelName, newWeights)).to.be.revertedWith("Model already exists");
    });

    it("Should retrieve all models", async () => {
      const modelName1 = "CIFAR10";
      const modelWeights1 = "0xa1b2c3d4";
      const modelName2 = "MNIST";
      const modelWeights2 = "0x05060708";

      await models.createModel(modelName1, modelWeights1);
      await models.createModel(modelName2, modelWeights2);

      const allModels = await models.getAllModels();
      expect(allModels.length).to.equal(2);

      expect(allModels[0].identifier).to.equal(modelName1);
      expect(allModels[0].weights).to.equal(modelWeights1);
      expect(allModels[1].identifier).to.equal(modelName2);
      expect(allModels[1].weights).to.equal(modelWeights2);

    });

     it("Should return an empty Model struct for non-existent model", async () => {
        const nonExistentModelName = "NON_EXISTENT";
        await expect(models.getModel(nonExistentModelName)).to.be.revertedWith("Model does not exist");   
    });

    it("Should get the model by name", async () => {

        const modelName1 = "CIFAR10";
        const modelWeights1 = "0xa1b2c3d4";
        await models.createModel(modelName1, modelWeights1)

        const retrievedModel = await models.getModel(modelName1);

        //Check that we can get the model id
        expect(retrievedModel).to.not.be.null;
        
        //Check that the model has the correct name and weights
        expect(retrievedModel.identifier).to.equal(modelName1);
        expect(retrievedModel.weights).to.equal(modelWeights1);
    });

});