import boa
from typing import Dict, List, Tuple
from curve_dao.addresses import get_dao_voting_contract
from curve_dao.ipfs import get_ipfs_hash_from_description
import os
from dotenv import load_dotenv

load_dotenv()



### ----- VOTE CREATION UTILS ----- ###

def get_evm_script(target, actions):
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

    evm_script = prepare_evm_script(target, actions)
    return evm_script



def prepare_evm_script(target: Dict, actions: List[Tuple]):
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




### ----- DECODING VOTES ----- ###

"""def get_vote_script(vote_type: str, vote_id: int) -> str:
    voting_contract_address = get_dao_voting_contract(vote_type)

    voting_contract = boa.from_etherscan(voting_contract_address["voting"], name="AragonVoting", api_key=os.getenv("ETHERSCAN_API_KEY"))
    #voting_contract = boa.load_abi("./contracts/Voting.json", name="AragonVoting")
    #voting_contract = voting_contract.at(voting_contract_address)

    vote = voting_contract.getVote(vote_id)
    print(vote)
    script = vote["script"]
    print(script)
    return script


get_vote_script("ownership", 100)"""