# Sensorfact Blockchain Energy API

This project provides a Flask-based GraphQL API for extracting and analyzing energy usage data from the Bitcoin blockchain.  
It uses [Strawberry GraphQL](https://strawberry.rocks/) and queries the [blockchain.info](https://blockchain.info/) public APIs.

---

## Features

- **Energy per transaction for a block**
- **Total energy per day for the last X days**
- **Total energy for all transactions by a wallet address**
- **Caching for repeated API calls**

---

## API Endpoints

### GraphQL Playground

- **URL:** `http://localhost:5000/graphql`

### Example GraphQL Queries

#### 1. Energy per transaction for a block

```graphql
query {
  energyPerTransaction(blockHash: "000000000000000000024c163dc82cd22a1163f5fc19bdf3dc80e3a9be9427ce") {
    txHash
    size
    energyKwh
  }
}
```

#### 2. Total energy per day for last X days

```graphql
query {
  totalEnergyLastDays(days: 2) {
    date
    totalEnergyKwh
  }
}
```

#### 3. Total energy for all transactions by a wallet address

```graphql
query {
  totalWalletEnergy(address: "1AJbsFZ64EpEfS5UAjAfcUG8pH8Jn3rn1F")
}
```

---

## How to Run

### 1. Install dependencies

```sh
pip install -r requirements.txt
```

### 2. Start the server

```sh
flask run
```

The API will be available at [http://localhost:5000/graphql](http://localhost:5000/graphql).

---

## Testing

Unit tests are provided in the `test/` directory.  
To run tests:

```sh
pytest
```

---

