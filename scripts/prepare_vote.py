import boa
import os
from typing import List, Tuple

from curve_dao.vote_utils import get_evm_script
from curve_dao.addresses import get_dao_voting_contract
from curve_dao.ipfs import get_ipfs_hash_from_description


def prepare_vote(target: str, actions: List[Tuple], description: str):
    """
    Function to prepare a on-chain DAO vote. The function returns a evm script and the ipfs hash.

    Args:
        target (str): ownership / parameter
        actions (list(tuple)): ("target addr", "function_name", *args)
        description (str): description of the on-chain gov proposal 
    """

    boa.env.fork(f"https://eth-mainnet.g.alchemy.com/v2/{os.getenv("ALCHEMY_API_KEY")}")

    target = get_dao_voting_contract(target)

    # create evm script
    evm_script = get_evm_script(
        target,
        actions
    )
    print("EVM script:", evm_script)


    # create ipfs hash
    ipfs_hash = get_ipfs_hash_from_description(description)
    print("IPFS hash:", ipfs_hash)


# example
prepare_vote(
    "ownership",
    [("0x0c0e5f2fF0ff18a3be9b835635039256dC4B4963", "set_gauge_implementation", "0x38D9BdA812da2C68dFC6aDE85A7F7a54E77F8325")],
    "Update gauge implementation for the Tricrypto-NG factory and set it to the same as for stableswap-ng and twocrypto-ng."
)