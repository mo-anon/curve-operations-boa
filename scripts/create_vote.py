import boa
import os
from typing import List, Tuple

from curve_dao.vote_utils import make_vote
from curve_dao.addresses import get_dao_voting_contract


def create_vote(target: str, actions: List[Tuple], description: str):
    """
    Function to create a on-chain Aragon DAO vote.

    Args:
        target (str): ownership / parameter
        actions (list(tuple)): ("target addr", "function_name", *args)
        description (str): description of the on-chain gov proposal 
    """

    boa.env.fork(f"https://eth-mainnet.g.alchemy.com/v2/{os.getenv("ALCHEMY_API_KEY")}")

    target = get_dao_voting_contract(target)

    tx = make_vote(
        target=target,
        actions=actions,
        description=description
    )


# example
create_vote(
    "ownership",
    [("0x0c0e5f2fF0ff18a3be9b835635039256dC4B4963", "set_gauge_implementation", "0x38D9BdA812da2C68dFC6aDE85A7F7a54E77F8325")],
    "Update gauge implementation for the Tricrypto-NG factory and set it to the same as for stableswap-ng and twocrypto-ng."
)