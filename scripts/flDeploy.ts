import "@nomicfoundation/hardhat-verify";
import { artifacts, ethers, run } from 'hardhat';
import { ModelsContract } from '../typechain-types';
const Models: ModelsContract = artifacts.require('Models');


async function main() {
    const [deployer] = await ethers.getSigners();

    console.log("Deploying contracts with the account:", deployer.address);

    const args: any[] = []
    const modelContract = await Models.new(...args);
    console.log("ModelsContract deployed to:", modelContract.address);
    try {

        const result = await run("verify:verify", {
            address: modelContract.address,
            constructorArguments: args,
        })

        console.log(result)
    } catch (e: any) {
        console.log(e.message)
    }
    console.log("Deployed contract at:", modelContract.address)

}
main().then(() => process.exit(0))