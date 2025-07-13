import requests
import time
from functools import lru_cache
from .schema import TransactionEnergy, DailyEnergy

ENERGY_PER_BYTE_KWH = 4.56
BASE_URL = "https://blockchain.info"

@lru_cache(maxsize=128)
def get_block_by_hash(block_hash):
    url = f"{BASE_URL}/rawblock/{block_hash}?cors=true"
    resp = requests.get(url, timeout=10)
    resp.raise_for_status()
    return resp.json()

def get_blocks_by_day(timestamp):
    url = f"{BASE_URL}/blocks/{timestamp}?format=json&cors=true"
    resp = requests.get(url, timeout=10)
    resp.raise_for_status()
    return resp.json()

def get_transactions_by_address(address, limit=50, offset=0):
    url = f"{BASE_URL}/rawaddr/{address}?limit={limit}&offset={offset}&cors=true"
    resp = requests.get(url, timeout=10)
    resp.raise_for_status()
    return resp.json().get('txs', [])

def energy_per_transaction_for_block(block_hash):
    block = get_block_by_hash(block_hash)
    results = []
    for tx in block.get('tx', []):
        size = tx.get('size', 0)
        energy = size * ENERGY_PER_BYTE_KWH
        results.append(TransactionEnergy(
            tx_hash=tx.get('hash'),
            size=size,
            energy_kwh=energy
        ))
    return results

def total_energy_per_day_last_x_days(x):
    now = int(time.time())
    results = []
    for i in range(x):
        day_timestamp = now - i * 86400
        blocks = get_blocks_by_day(day_timestamp * 1000)
        total_energy = 0
        for block in blocks:
            block_data = get_block_by_hash(block['hash'])
            for tx in block_data.get('tx', []):
                size = tx.get('size', 0)
                total_energy += size * ENERGY_PER_BYTE_KWH
            break
        results.append(DailyEnergy(
            date=time.strftime('%Y-%m-%d', time.gmtime(day_timestamp)),
            total_energy_kwh=total_energy
        ))
    return results

def total_energy_for_wallet(address):
    total_energy = 0
    offset = 0
    while True:
        txs = get_transactions_by_address(address, limit=50, offset=offset)
        if not txs:
            break
        for tx in txs:
            size = tx.get('size', 0)
            total_energy += size * ENERGY_PER_BYTE_KWH
        if len(txs) < 50:
            break
        offset += 50
    return total_energy