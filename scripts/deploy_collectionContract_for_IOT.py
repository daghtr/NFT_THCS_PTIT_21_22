from brownie import accounts, network, config, Collection_For_IOT
from scripts.reusable_scripts import get_account


def main():
    # account = get_account()
    account = accounts.add(config["wallets"]["from_key"])
    collectionAdvanced_contract = Collection_For_IOT.deploy(
        {"from": account},
        publish_source=False,
    )
