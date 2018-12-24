import json
import hashlib
from time import time

class Block():
    def __init__(self, index, prev_hash, nonce, timestamp=None, transactions=None):
        self.index = index
        self.prev_hash = prev_hash
        self.nonce = nonce
        self.timestamp = time() if timestamp is None else timestamp
        self.transactions = [] if transactions is None else transactions
    
    @property
    def to_json(self):
        return {
        'index': self.index, 
        'prev_hash': self.prev_hash,
        'nonce': self.nonce,
        'timestamp': self.timestamp,
        'transactions': self.transactions
    }

    @property
    def hash(self): 
        key = f'{self.index}{self.prev_hash}{self.nonce}{self.timestamp}{self.transactions}'.encode()
        return hashlib.sha256(key).hexdigest()
    
    def add_transactions(self, sender, recipient, amount):
        self.transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
        })
    
    def guess_hash(self, new_nonce):
        guess = f'{self.nonce}{new_nonce}{self.hash}'.encode()
        return hashlib.sha256(guess).hexdigest()
    
    
    
