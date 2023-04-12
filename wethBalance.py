from web3 import Web3
from decouple import config

polygon_endpoint = config('POLYGON_RPC')
web3 = Web3(Web3.HTTPProvider(polygon_endpoint))
contract_address_weth = config('WETH_CONTRACT_ADDRESS')

def get_WETH_balance(address):
    
    contract_abi = (
        '[{"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}]'
        )

    contract = web3.eth.contract(Web3.to_checksum_address(contract_address_weth), abi=contract_abi)
    weth_balance = contract.functions.balanceOf(address).call()
    return weth_balance