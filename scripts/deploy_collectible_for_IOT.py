from brownie import accounts, network, config, Collection_For_IOT
from scripts.reusable_scripts import get_account, get_contract
import os


def main():
    # account = get_account()
    account = accounts.add(config["wallets"]["from_key"])
    l = os.listdir("./img")
    li = [x.split(".")[0] for x in l]
    Collectible_contract = Collection_For_IOT[-1]
    for x in range(len(li)):
        tx = Collectible_contract.createCollectible({"from": account})
        tx.wait(1)
        print("New TokenID is created")
    print(Collectible_contract.tokenCounter())
