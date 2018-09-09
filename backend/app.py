import requests
from uuid import uuid4
from flask import Flask, jsonify, request
from blockchain import Blockchain
from block import Block

app = Flask(__name__)

recipient = str(uuid4()).replace('-', '')

blockchain = Blockchain()


@app.route('/mine', methods=['GET'])
def mine():
    block = blockchain.mine_new_block()
    response = {
        'message': "New Block Forged",
        'index': block.index,
        'transactions': block.transactions,
        'nonce': block.nonce,
        'prev_block_hash': block.prev_hash
    }
    return jsonify(response), 200


@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    values = request.get_json()

    required = ['sender', 'recipient', 'amount']
    if not all(k in values for k in required):
        return 'Missing values', 400

    index = blockchain.new_transaction(values['sender'], values['recipient'], values['amount'])

    response = {'message': f'Transaction will be added to Block {index}'}
    return jsonify(response), 201


@app.route('/', methods=['GET'])
@app.route('/chain', methods=['GET'])
def full_chain():
    block_to_json = [{
        'index': block.index, 
        'prev_hash': block.prev_hash,
        'nonce': block.nonce,
        'transactions': block.transactions
    } for block in blockchain.blocks]
    response = {
        'chain': block_to_json,
        'length': len(blockchain.blocks),
    }
    return jsonify(response), 200


@app.route('/nodes/register', methods=['POST'])
def register_nodes():
    values = request.get_json()

    nodes = values.get('nodes')
    if nodes is None:
        return "Error: Please supply a valid list of nodes", 400

    for node in nodes:
        blockchain.register_node(node)

    response = {
        'message': 'New nodes have been added',
        'total_nodes': list(blockchain.nodes),
    }
    return jsonify(response), 201


@app.route('/nodes/resolve', methods=['GET'])
def consensus():
    replaced = blockchain.resolve_conflicts()

    if replaced:
        response = {
            'message': 'Our chain was replaced',
            'new_chain': blockchain.blocks
        }
    else:
        response = {
            'message': 'Our chain is authoritative',
            'chain': blockchain.blocks
        }

    return jsonify(response), 200


if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=5000, type=int, help='listen on a port')
    parser.add_argument('-d', '--debug', default=True, type=bool, help='debug mode True/False')
    args = parser.parse_args()
    port = args.port
    debug = args.debug
    app.run(host='0.0.0.0', port=port, debug=debug)
