from brownie import accounts, network, config, Collection_For_IOT
from scripts.reusable_scripts import (
    get_account,
    get_contract,
)
from metadata.sample_metadata import metadata_template
from pathlib import Path
import requests
import json
import os

# Metadata is TokenURI


def upload_to_ipfs(filepath):
    # read file as binary (rb)
    with Path(filepath).open("rb") as fp:
        file_binary = fp.read()
        # upload ...
        # download command-line for IPFS (follow instructions: https://docs.ipfs.io/install/command-line/#official-distributions)
        # check out https://docs.ipfs.io/reference/http/api/#api-v0-add for code instruction
        # ipfs_url = "http://127.0.0.1:5001" -> ipfs daemon: running our own node -> then be able to upload
        # if our own node goes down, no one can see the NFT img or access NFT Metadata
        ipfs_url = "http://127.0.0.1:5001"
        endpoint = "/api/v0/add"
        response = requests.post(
            ipfs_url + endpoint,
            files={"file": file_binary},
            headers=None,
        )
        print("http post: done")
        ipfs_hash = response.json()["Hash"]
        # "./img/PUG.png" -> "PUG.png"
        filename = filepath.split("/")[-1:][0]
        file_uri = f"https://ipfs.io/ipfs/{ipfs_hash}?filename={filename}"
        print(file_uri)
        return file_uri


def upload_to_pinata(filepath):
    PINATA_BASE_URL = "https://api.pinata.cloud/"
    endpoint = "pinning/pinFileToIPFS"
    headers = {
        "pinata_api_key": config["pinata"]["api_key"],
        "pinata_secret_api_key": config["pinata"]["api_secret_key"],
    }
    filename = filepath.split("/")[-1:][0]
    # read file as binary (rb)
    with Path(filepath).open("rb") as fp:
        image_binary = fp.read()
        response = requests.post(
            PINATA_BASE_URL + endpoint,
            files={"file": (filename, image_binary)},
            headers=headers,
        )
    print(response.json())


def main_for_upload_PINATA():
    advanced_collectible = Collection_For_IOT[-1]
    # loop through all tokens and figure out the metadata for each of them
    number_of_TokenID = advanced_collectible.tokenCounter()
    print(f"You have created {number_of_TokenID} collectibles!")
    list_file = os.listdir("./img")
    image_name = [x.split(".")[0] for x in list_file]
    for token_id in range(number_of_TokenID):
        metadata_file_name_path = (
            f"./metadata/{network.show_active()}/{image_name[token_id]}.json"
        )
        upload_to_pinata(metadata_file_name_path)  # upload metadata to Pinata
        image_path = "./img/" + image_name[token_id] + ".png"
        image_uri = upload_to_pinata(image_path)  # upload metadata to Pinata


def main_for_upload_IPFS():
    advanced_collectible = Collection_For_IOT[-1]
    # loop through all tokens and figure out the metadata for each of them
    number_of_TokenID = advanced_collectible.tokenCounter()
    print(f"You have created {number_of_TokenID} collectibles!")
    list_file = os.listdir("./img")
    image_name = [x.split(".")[0] for x in list_file]
    for token_id in range(number_of_TokenID):
        metadata_file_name_path = (
            f"./metadata/{network.show_active()}/{image_name[token_id]}.json"
        )
        collectible_metadata = metadata_template
        if Path(metadata_file_name_path).exists():
            print(f"{metadata_file_name_path} already exists! Delete it to overwrite")
        else:
            print(f"Creating Metadata file: {metadata_file_name_path}")
            collectible_metadata["name"] = image_name[token_id]
            collectible_metadata["description"] = f"{image_name[token_id]} HD District"
            image_path = "./img/" + image_name[token_id] + ".png"
            print("chuan bi upload to ipfs")
            image_uri = upload_to_ipfs(image_path)  # upload image to ipfs
            print("Upload to ipfs: done")
            collectible_metadata["imageURI"] = image_uri
            with open(metadata_file_name_path, "w") as file:
                json.dump(collectible_metadata, file)
            ipfs_metadata_link = upload_to_ipfs(metadata_file_name_path)  # upload metadata to ipfs
            with open("./metadata/metadata_link.txt", "a") as f:
                print(ipfs_metadata_link, file=f)


def main():
    print("Options for uploading metadata and image:")
    x = int(input())
    if x == 1:
        main_for_upload_IPFS()
    if x == 2:
        main_for_upload_PINATA()
