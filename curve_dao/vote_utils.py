import boa
from typing import Dict, List, Tuple
from curve_dao.addresses import get_dao_voting_contract
from curve_dao.ipfs import get_ipfs_hash_from_description
import os
from dotenv import load_dotenv

load_dotenv()


def make_vote(target, actions, description):
    """Prepares EVM script and creates an on-chain AragonDAO vote.

    Args:
        target (dict): ownership / parameter / emergency
        actions (list(tuple)): ("target addr", "fn_name", *args)
        vote_creator (str): msg.sender address
        description (str): Description of the on-chain governance proposal

    Returns:
        str: vote ID of the created vote.
    """

    aragon_voting = boa.from_etherscan(target["voting"], name="AragonVoting", api_key=os.getenv("ETHERSCAN_API_KEY"))

    #vote_creator = boa.env.eoa
    #assert aragon_voting.canCreateNewVote(vote_creator), "dev: user cannot create new vote"

    evm_script = prepare_vote_script(target, actions)
    print("EVM script:", evm_script)
    
    ipfs_hash = get_ipfs_hash_from_description(description)
    print("IPFS hash:", ipfs_hash)


    with boa.env.prank("0x7a16fF8270133F063aAb6C9977183D9e72835428"):
        tx = aragon_voting.newVote(
            evm_script,
            f"ipfs: {ipfs_hash}",
            False,
            False,
        )

    return tx 



def prepare_vote_script(target: Dict, actions: List[Tuple]):
    """Generates EVM script to be executed by AragonDAO contracts.

    Args:
        target (dict): CURVE_DAO_OWNERSHIP / CURVE_DAO_PARAMS / EMERGENCY_DAO
        actions (list(tuple)): ("target addr", "fn_name", *args)

    Returns:
        str: Generated EVM script.
    """
    aragon_agent = boa.from_etherscan(target["agent"], name="AragonAgent", api_key=os.getenv("ETHERSCAN_API_KEY"))
    aragon_voting = boa.from_etherscan(target["voting"], name="AragonVoting", api_key=os.getenv("ETHERSCAN_API_KEY"))

    evm_script = bytes.fromhex("00000001")

    for action in actions:
        address, fn_name, *args = action
        contract = boa.from_etherscan(address=address, name="TargetContract", api_key=os.getenv("ETHERSCAN_API_KEY"))
        contract_function = getattr(contract, fn_name)
        
        calldata = contract_function.prepare_calldata(*args)
        agent_calldata = aragon_agent.execute.prepare_calldata(address, 0, calldata)
        
        length = bytes.fromhex(hex(len(agent_calldata.hex()) // 2)[2:].zfill(8))
        evm_script = evm_script + bytes.fromhex(aragon_agent.address[2:]) + length + agent_calldata


    return evm_script