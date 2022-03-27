// contracts/Collection_Advanced.sol
// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";

contract Collection_For_IOT is ERC721URIStorage {
    uint256 public tokenCounter;

    constructor() ERC721("IOTTEST", "IOT") {
        tokenCounter = 0;
    }

    function createCollectible() public {
        uint256 newTokenId = tokenCounter;
        _safeMint(msg.sender, newTokenId);
        tokenCounter = tokenCounter + 1;
    }

    // Mapping "tokenID" to "metadata TokenURIs".
    // This helping OPENSEA to view our NTF according to the format: https://testnets.opensea.io/assets/{contract address}/{}

    function mapTokenURI(uint256 _tokenId, string memory _tokenURI) public {
        require(
            _isApprovedOrOwner(_msgSender(), _tokenId),
            "ERC721: caller is not owner no approved"
        );
        _setTokenURI(_tokenId, _tokenURI);
    }
}
