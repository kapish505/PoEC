// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/**
 * @title ProofAnchor
 * @dev Stores hashes of datasets and analysis results to prove existence and integrity at a specific time.
 */
contract ProofAnchor {
    
    struct Anchor {
        bytes32 contentHash;
        uint256 timestamp;
        address submitter;
        string metadata; // CID or other reference
    }

    mapping(bytes32 => Anchor) public anchors;
    
    event Anchored(bytes32 indexed contentHash, uint256 timestamp, address indexed submitter, string metadata);

    /**
     * @dev Anchors a hash to the blockchain.
     * @param _contentHash The SHA-256 hash of the content (dataset, graph, or result).
     * @param _metadata Optional metadata like IPFS CID or JSON string.
     */
    function anchorHash(bytes32 _contentHash, string memory _metadata) public {
        require(anchors[_contentHash].timestamp == 0, "Hash already anchored");

        anchors[_contentHash] = Anchor({
            contentHash: _contentHash,
            timestamp: block.timestamp,
            submitter: msg.sender,
            metadata: _metadata
        });

        emit Anchored(_contentHash, block.timestamp, msg.sender, _metadata);
    }

    /**
     * @dev Verifies if a hash exists.
     * @param _contentHash The hash to verify.
     */
    function verifyHash(bytes32 _contentHash) public view returns (bool, uint256, address, string memory) {
        Anchor memory anchor = anchors[_contentHash];
        if (anchor.timestamp == 0) {
            return (false, 0, address(0), "");
        }
        return (true, anchor.timestamp, anchor.submitter, anchor.metadata);
    }
}
