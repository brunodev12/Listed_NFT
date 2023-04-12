from web3 import Web3
import os

polygon_endpoint = os.environ.get('POLYGON_RPC')
contract_address_weth = os.environ.get('WETH_CONTRACT_ADDRESS')
web3 = Web3(Web3.HTTPProvider(polygon_endpoint))

def get_WETH_balance(address):
    
    contract_abi = (
        '[{"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}]'
        )

    contract = web3.eth.contract(Web3.to_checksum_address(contract_address_weth), abi=contract_abi)
    weth_balance = contract.functions.balanceOf(address).call()
    return weth_balance
