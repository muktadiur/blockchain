import json
import hashlib
from time import time

class Block():
    def __init__(self, index, prev_hash, nonce, transactions=None):
        self.index = index
        self.prev_hash = prev_hash
        self.nonce = nonce
        self.timestamp = time()
        if transactions is None:
            transactions = []
        self.transactions = transactions
    
    def hash(self): 
        key = f'{self.index}{self.prev_hash}{self.nonce}{self.timestamp}{self.transactions}'.encode()
        return hashlib.sha256(key).hexdigest()
    
    def add_transactions(self, sender, recipient, amount):
        self.transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
        })
    
    def guess_hash(self, new_index):
        guess = f'{self.index}{new_index}{self.hash()}'.encode()
        return hashlib.sha256(guess).hexdigest()
    
    def __repr__(self):
        return json.dumps(self.__dict__)
    
