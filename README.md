# Simple Blockchain

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
