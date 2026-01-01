const hre = require("hardhat");

async function main() {
    const PoECRegistry = await hre.ethers.getContractFactory("PoECRegistry");
    const registry = await PoECRegistry.deploy();

    await registry.waitForDeployment();

    console.log("PoECRegistry deployed to:", await registry.getAddress());
}

main().catch((error) => {
    console.error(error);
    process.exitCode = 1;
});
