from web3 import Web3
from decouple import config
import json
from dateutil.parser import parse
from getId import get_id
from getSignature import get_signature
from wethBalance import get_WETH_balance
from mail import send_email

polygon_endpoint = config('POLYGON_RPC')
address = config('ADDRESS')
address = Web3.to_checksum_address(address)
private_key = config('PRIVATE_KEY')

w3 = Web3(Web3.HTTPProvider(polygon_endpoint))

contract_address = config('CONTRACT_ADDRESS')

contract_abi = (
    '[{"inputs": [{"components": [{"internalType": "address","name": "considerationToken","type": "address"},{"internalType": "uint256","name": "considerationIdentifier","type": "uint256"},{"internalType": "uint256","name": "considerationAmount","type": "uint256"},{"internalType": "address payable","name": "offerer","type": "address"},{"internalType": "address","name": "zone","type": "address"},{"internalType": "address","name": "offerToken","type": "address"},{"internalType": "uint256","name": "offerIdentifier","type": "uint256"},{"internalType": "uint256","name": "offerAmount","type": "uint256"},{"internalType": "enumBasicOrderType","name": "basicOrderType","type": "uint8"},{"internalType": "uint256","name": "startTime","type": "uint256"},{"internalType": "uint256","name": "endTime","type": "uint256"},{"internalType": "bytes32","name": "zoneHash","type": "bytes32"},{"internalType": "uint256","name": "salt","type": "uint256"},{"internalType": "bytes32","name": "offererConduitKey","type": "bytes32"},{"internalType": "bytes32","name": "fulfillerConduitKey","type": "bytes32"},{"internalType": "uint256","name": "totalOriginalAdditionalRecipients","type": "uint256"},{"components": [{"internalType": "uint256","name": "amount","type": "uint256"},{"internalType": "address payable","name": "recipient","type": "address"}],"internalType": "structAdditionalRecipient[]","name": "additionalRecipients","type": "tuple[]"},{"internalType": "bytes","name": "signature","type": "bytes"}],"internalType": "structBasicOrderParameters","name": "parameters","type": "tuple"}],"name": "fulfillBasicOrder","outputs": [{"internalType": "bool","name": "fulfilled","type": "bool"}],"stateMutability": "payable","type": "function"}]'
    )

contract = w3.eth.contract(Web3.to_checksum_address(contract_address), abi=contract_abi)

with open("unClaimed_listed.json") as jsonfile:
    unClaimed_listed = json.load(jsonfile)

def buyToken(token_id, _nonce):

    data = get_id(token_id)
    if len(data['orders'])>0:
        nullAddress = '0x0000000000000000000000000000000000000000'

        considerationToken = data['orders'][0]['data']['consideration'][0]['token'][9:]
        considerationToken = w3.to_checksum_address(considerationToken)

        price = float(data['orders'][0]['makePrice'])

        if (considerationToken==nullAddress and price<26) or (considerationToken!=nullAddress and price <0.015):
            address_balance = w3.eth.get_balance(address) if considerationToken == nullAddress else get_WETH_balance(address)
            if address_balance/(10**18) < price:
                send_email("Insufficient balance to execute the transaction", "Insufficient balance")
            else:
                considerationIdentifier = int(data['orders'][0]['data']['consideration'][0]['identifierOrCriteria'])
                considerationAmount = int(data['orders'][0]['data']['consideration'][0]['startAmount'])
                offerer = data['orders'][0]['data']['consideration'][0]['recipient'][9:]
                offerer = w3.to_checksum_address(offerer)
                zone = data['orders'][0]['data']['zone'][9:]
                zone = w3.to_checksum_address(zone)
                offerToken = data['orders'][0]['data']['offer'][0]['token'][9:]
                offerToken = w3.to_checksum_address(offerToken)
                offerIdentifier = int(data['orders'][0]['data']['offer'][0]['identifierOrCriteria'])
                offerAmount = int(data['orders'][0]['data']['offer'][0]['startAmount'])
                #orderType = data['orders'][0]['data']['orderType']
                basicOrderType = 0 if considerationToken == nullAddress else 8
                startTime = data['orders'][0]['startedAt']
                object_datetime = parse(startTime)
                startTime = int(object_datetime.timestamp())
                endTime = data['orders'][0]['endedAt']
                object_datetime = parse(endTime)
                endTime = int(object_datetime.timestamp())
                zoneHash = data['orders'][0]['data']['zoneHash']
                salt = int(data['orders'][0]['salt'],16)
                offererConduitKey = data['orders'][0]['data']['conduitKey']
                fulfillerConduitKey = zoneHash if considerationToken == nullAddress else offererConduitKey
                totalOriginalAdditionalRecipients = len(data['orders'][0]['data']['consideration']) - 1

                j=0
                additionalRecipients = []
                for i in (data['orders'][0]['data']['consideration']):
                    if j > 0:
                        amount = int(data['orders'][0]['data']['consideration'][j]['startAmount'])
                        recipient = data['orders'][0]['data']['consideration'][j]['recipient'][9:]
                        recipient = w3.to_checksum_address(recipient)
                        dictionary = {'amount': amount, 'recipient':recipient}
                        additionalRecipients.append(dictionary)
                    j+=1

                id = data['orders'][0]['id'][8:]
                signature = get_signature(id)

                gas_price_wei = w3.eth.gas_price
                gas_price_matic = w3.from_wei(gas_price_wei, 'ether')    

                if (gas_price_matic * 500000)>1:
                    send_email("Very expensive gas to execute the transaction", "Expensive gas")
                else:
                    transaction = contract.functions.fulfillBasicOrder([
                        considerationToken,
                        considerationIdentifier,
                        considerationAmount,
                        offerer,
                        zone,
                        offerToken,
                        offerIdentifier,
                        offerAmount,
                        basicOrderType,
                        startTime,
                        endTime,
                        zoneHash,
                        salt,
                        offererConduitKey,
                        fulfillerConduitKey,
                        totalOriginalAdditionalRecipients,
                        additionalRecipients,
                        signature,
                        ]                                                                                           
                    ).build_transaction({
                        'from': address,
                        'gas': 500000,
                        'maxFeePerGas': gas_price_wei,
                        'maxPriorityFeePerGas': gas_price_wei,
                        'nonce': _nonce,
                        'value': w3.to_wei(price, 'ether') if considerationToken == nullAddress else 0,
                        'chainId': 137,
                    })

                    sign_txn = w3.eth.account.sign_transaction(transaction, private_key)

                    tx_hash = w3.eth.send_raw_transaction(sign_txn.rawTransaction)

                    send_email(f"hash:  {w3.to_hex(tx_hash)}", "Transaction sent")

                    return True


if len(unClaimed_listed)>0:
    nonce = w3.eth.get_transaction_count(address)
    for i in unClaimed_listed:
        success = buyToken(i['tokenId'], nonce)
        nonce += 1 if success else 0