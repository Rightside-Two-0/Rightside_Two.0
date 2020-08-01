import time
import hashlib

class Block(object):
    def __init__(self, index, proof, prev_hash , transactions):
        self.index = index
        self.proof = proof
        self.prev_hash = prev_hash
        self.transactions = transactions
        self.timestamp = time.time()

    def get_block_hash(self):
        block_string = '{}{}{}{}{}'.format(self.index, self.proof, self.prev_hash, self.transactions, self.timestamp)
        return hashlib.sha256(block_string.encode()).hexdigest()
