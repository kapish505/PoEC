const hre = require("hardhat");

async function main() {
    const ProofAnchor = await hre.ethers.getContractFactory("ProofAnchor");
    const proofAnchor = await ProofAnchor.deploy();

    await proofAnchor.waitForDeployment();

    console.log(
        `ProofAnchor deployed to ${proofAnchor.target}`
    );
}

main().catch((error) => {
    console.error(error);
    process.exitCode = 1;
});
