import requests
from urllib.parse import urlparse
from block import Block

class Blockchain():
    def __init__(self):
        self.blocks = []
        self.transactions = []
        self.nodes = set()
        genesis_block = Block(index=0, prev_hash='00000000', nonce=0)
        self.blocks.append(genesis_block)
    
    @property
    def to_json(self):
        return [block.to_json for block in self.blocks]

    @property
    def last_block(self):
        return self.blocks[-1]

    def add_block(self, block):
        self.blocks.append(block)
    
    def mine_new_block(self):
        last_block = self.last_block
        nonce = self.proof_of_work(last_block)
        block = Block(
            index = len(self.blocks),
            prev_hash = last_block.hash,
            nonce = nonce,
            transactions=self.transactions
        )
        self.transactions = []
        self.blocks.append(block)
        return block
    
    def new_transaction(self, sender, recipient, amount):
        self.transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
        })

        return len(self.blocks)

    def proof_of_work(self, last_block):
        nonce = 0
        guess_hash = last_block.guess_hash(nonce)
        while guess_hash[:2] != "00":
            nonce += 1
            guess_hash = last_block.guess_hash(nonce)
        return nonce
    
    def register_node(self, address):
        parsed_url = urlparse(address)
        if parsed_url.netloc:
            self.nodes.add(parsed_url.netloc)
        elif parsed_url.path:
            self.nodes.add(parsed_url.path)
        else:
            raise ValueError('Invalid URL')


    def valid_chain(self, chain):
        index = 0
        last_block = Block(**chain[index])
        while index < len(chain):
            index += 1
            block = Block(**chain[index])
            if block.prev_hash != last_block.hash:
                return False
            guess_hash = last_block.guess_hash(block.nonce)
            if guess_hash[:2] != "00":
                return False
            last_block = block

        return True
    
    def resolve_conflicts(self):
        neighbours = self.nodes
        new_blocks = None

        max_length = len(self.blocks)

        for node in neighbours:
            response = requests.get(f'http://{node}/chain')

            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']

                if length > max_length and self.valid_chain(chain):
                    max_length = length
                    new_blocks = chain

        if new_blocks:
            self.blocks = new_blocks
            return True

        return False