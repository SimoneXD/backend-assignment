"""
GraphQL Query Resolvers for Blockchain Energy Metrics

This module defines the GraphQL schema and query fields for accessing
blockchain-related energy consumption data. It uses Strawberry to define
a GraphQL API layer over the core blockchain energy utility functions.

Query Fields:
- energy_per_transaction: Energy usage per transaction in a specific block.
- total_energy_last_days: Daily total energy usage for the past X days.
- total_wallet_energy: Total energy used by all transactions of a wallet address.
"""
from typing import List
import strawberry
from .schema import TransactionEnergy, DailyEnergy
from .blockchain_energy_utils import (
    energy_per_transaction_for_block,
    total_energy_per_day_last_x_days,
    total_energy_for_wallet
)

@strawberry.type
class Query:
    """
    GraphQL query root for blockchain energy data.

    This class defines the root-level GraphQL fields that expose
    energy calculations related to blockchain data, including per transaction,
    daily totals, and wallet-level aggregates.
    """
    @strawberry.field
    def energy_per_transaction(self, block_hash: str) -> List[TransactionEnergy]:
        """
        Get estimated energy consumption for each transaction in a block.

        Args:
            block_hash (str): The hash of the block.

        Returns:
            List[TransactionEnergy]: A list of TransactionEnergy dataclass instances with 
            transaction hash, size in bytes, and estimated energy in kWh.
        """
        return energy_per_transaction_for_block(block_hash)

    @strawberry.field
    def total_energy_last_days(self, days: int) -> List[DailyEnergy]:
        """
        Get total energy consumed for the last N days.

        Args:
            days (int): Number of days to look back.

        Returns:
            List[DailyEnergy]: A list of DailyEnergy dataclass instances containing the date 
        and energy consumption in kWh.
        """
        return total_energy_per_day_last_x_days(days)

    @strawberry.field
    def total_wallet_energy(self, address: str) -> float:
        """
        Get total energy consumption for a given wallet address.

        Args:
            address (str): Wallet address.

        Returns:
            float: Total energy consumed by transactions of the wallet.
        """
        return total_energy_for_wallet(address)

schema = strawberry.Schema(query=Query)
