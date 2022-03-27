#!/usr/bin/python3
from brownie import accounts, network, config, Collection_For_IOT
from scripts.reusable_scripts import OPENSEA_FORMAT, get_account


def main():
    print(f"Working on {network.show_active()}")
    # account = get_account()
    account = accounts.add(config["wallets"]["from_key"])
    advanced_collectible = Collection_For_IOT[-1]
    number_of_tokenID = advanced_collectible.tokenCounter()
    print(f"You have {number_of_tokenID} tokenIds")
    with open("./metadata/metadata_link.txt") as f:
        metadata_link_read = f.readlines()
    for token_id in range(number_of_tokenID):
        if not advanced_collectible.tokenURI(token_id).startswith("https://"):
            tx = advanced_collectible.mapTokenURI(
                token_id, metadata_link_read[token_id], {"from": account}
            )
            print(
                f"You can view your NFT at {OPENSEA_FORMAT.format(advanced_collectible.address, token_id)}"
            )
            tx.wait(1)
