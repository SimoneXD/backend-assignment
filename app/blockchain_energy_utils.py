"""
Blockchain Energy Estimator

This module provides utility functions to interact with the Blockchain API
to retrieve block and transaction data and estimate the energy consumption 
(kWh) based on transaction sizes.
"""
from typing import List
import time
from functools import lru_cache
import requests
from .schema import TransactionEnergy, DailyEnergy

ENERGY_PER_BYTE_KWH = 4.56
BASE_URL = "https://blockchain.info"

@lru_cache(maxsize=128)
def request(url: str) -> dict:
    """
    Make a GET request to the specified URL and return the JSON response.

    Args:
        url (str): The URL to request.

    Returns:
        dict: JSON response from the API.
    """
    #TODO: exponential backoff in case of retries
    resp = requests.get(url, timeout=10)
    resp.raise_for_status()
    return resp.json()

def get_transaction_energy(tx: dict) -> TransactionEnergy:
    """
    Calculate energy usage for a single transaction.

    Args:
        tx (dict): Transaction data containing size in bytes.

    Returns:
        TransactionEnergy: A dataclass instance with transaction hash, size in bytes, 
        and estimated energy in kWh.
    """
    size = tx.get('size', 0)
    energy = size * ENERGY_PER_BYTE_KWH
    return TransactionEnergy(
        tx_hash=tx.get('hash'),
        size=size,
        energy_kwh=energy
    )

def energy_per_transaction_for_block(block_hash: str) -> List[TransactionEnergy]:
    """
    Calculate energy usage for each transaction in a specific block.

    Args:
        block_hash (str): The hash of the block.

    Returns:
        list[TransactionEnergy]: A list of TransactionEnergy dataclass instances with 
        transaction hash, size in bytes, and estimated energy in kWh.
    """
    url = f"{BASE_URL}/rawblock/{block_hash}?cors=true"
    block = request(url)
    results = []
    for tx in block.get('tx', []):
        results.append(get_transaction_energy(tx))
    return results

def total_energy_per_day_last_x_days(x:int) -> List[DailyEnergy]:
    """
    Calculate the total energy consumed per day over the last X days.

    Args:
        x (int): Number of past days to include.

    Returns:
        list[DailyEnergy]: A list of DailyEnergy dataclass instances containing the date 
        and total energy consumption in kWh.
    """
    now = int(time.time())
    results = []
    for i in range(x):
        day_timestamp = now - i * 86400
        timestamp_milliseconds = day_timestamp * 1000
        url = f"{BASE_URL}/blocks/{timestamp_milliseconds}?format=json&cors=true"
        blocks = request(url)
        total_energy = 0
        for block in blocks:
            block_hash = block.get('hash')
            if not block_hash:
                continue
            energy = energy_per_transaction_for_block(block_hash)
            for tx_energy in energy:
                total_energy += tx_energy.energy_kwh
            # Only process the first block of the day
            # because too many requests will trigger rate limit.
            break
        results.append(DailyEnergy(
            date=time.strftime('%Y-%m-%d', time.gmtime(day_timestamp)),
            total_energy_kwh=total_energy
        ))
    return results

def total_energy_for_wallet(address: str) -> float:
    """
    Estimate the total energy consumption for all transactions of a wallet address.

    Args:
        address (str): The wallet address.

    Returns:
        float: Total estimated energy in kWh for all transactions.
    """
    total_energy = 0
    offset = 0
    limit = 50
    while True:
        url = f"{BASE_URL}/rawaddr/{address}?limit={limit}&offset={offset}&cors=true"
        txs = request(url).get('txs', [])
        if not txs:
            break
        for tx in txs:
            total_energy += get_transaction_energy(tx).energy_kwh
        if len(txs) < 50:
            break
        offset += 50
    return total_energy
