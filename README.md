# Simple Blockchain based on https://hackernoon.com/learn-blockchains-by-building-one-117428612f46

## How to run the code

```pip install -r requirements.txt```

```python app.py -p 5000```

## GET the blockchain

```curl -X GET http://localhost:5000/chain```

```

{
  "chain": [
    {
      "index": 0,
      "nonce": 0,
      "prev_hash": "00000000",
      "transactions": []
    }
  ],
  "length": 1
}

```

## Add new transaction

```curl -X POST -H "Content-Type: application/json" -d '{"sender": "Muktadiur","recipient": "Sajib","amount": 10}' http://localhost:5000/transactions/new```

```
{
  "message": "Transaction will be added to Block 1"
}
```

## Mine transactions

```curl -X GET http://localhost:5000/mine```

```
{
  "index": 2,
  "message": "New Block Forged",
  "nonce": 239,
  "prev_block_hash": "738796c8a7629f37246adf1e3c97c964ef718bcc8130271be06e61271f052088",
  "transactions": [
    {
      "amount": 10,
      "recipient": "Sajib",
      "sender": "Muktadiur"
    }
  ]
}

```

## Register a new node

```
Run anoter instance of the application on port: 5001
python app.py -p 5001

```

```curl -X POST -H "Content-Type: application/json" -d '{"nodes": ["http://0.0.0.0:5001/"]}' http://localhost:5000/nodes/register```

```
{
  "message": "New nodes have been added",
  "total_nodes": [
    "0.0.0.0:5001"
  ]
}

```

```
Check the the chain: http://localhost:5001/chain
Add some transaction to http://localhost:5001/transactions/new
```

## Update the chain from blockchain nodes

```curl -X GET http://localhost:5000/nodes/resolve```

```
{
    "message": "Our chain was replaced",
    "new_chain": [
        {
            "index": 0,
            "nonce": 0,
            "prev_hash": "00000000",
            "timestamp": 1545682188.972287,
            "transactions": []
        },
        {
            "index": 1,
            "nonce": 435,
            "prev_hash": "800c072babd905002204d24968d71e6150e178f6415b16bfd28d34f57964e5f9",
            "timestamp": 1545682215.978256,
            "transactions": [
                {
                    "amount": 2,
                    "recipient": "2",
                    "sender": "muktadiur"
                }
            ]
        }
    ]
}

```
