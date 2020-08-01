from BlockChain import BlockChain
from Block import Block

blockchain = BlockChain()

print(">>>>> Before Mining...")
print(blockchain.chain)

last_block = blockchain.get_last_block
last_proof = last_block.proof
proof = blockchain.create_proof_of_work(last_proof)

# Sender "0" means that this node has mined a new block
# For mining the Block(or finding the proof), we must be awarded with some amount(in our case this is 1)

blockchain.create_new_transaction(
    sender="0",
    recipient="address_x",
    amount=1,
)

last_hash = last_block.get_block_hash()
block = blockchain.create_new_block(proof, last_hash)

print(">>>>> After Mining...")
print(blockchain.chain)
