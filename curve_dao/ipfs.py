import os
import requests


def get_ipfs_hash_from_description(description: str):
    """Uploads vote description to IPFS via Pinata and returns the IPFS hash.

    NOTE: Needs environment variables for Pinata IPFS access. Please
    set up an IPFS project to generate API key and API secret!
    """
    headers = {
        "pinata_api_key": os.getenv("PINATA_API_KEY"),
        "pinata_secret_api_key": os.getenv("PINATA_SECRET_API_KEY")
    }
    response = requests.post(
        "https://api.pinata.cloud/pinning/pinJSONToIPFS",
        json={"pinataContent": {"text": description}},
        headers=headers
    )
    assert (
        200 <= response.status_code < 400
    ), f"POST to IPFS failed: {response.status_code}"
    return response.json()["IpfsHash"]