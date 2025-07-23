"""
GraphQL Types for Blockchain Energy Metrics

Defines GraphQL data types representing:
- Energy usage of individual blockchain transactions.
- Daily aggregated energy consumption.

These types are used as response objects in the query schema.
"""
import strawberry

@strawberry.type
class TransactionEnergy:
    """
    A data type representing the energy consumption of a single blockchain transaction.

    Attributes:
        tx_hash (str): The hash of the transaction.
        size (int): The size of the transaction in bytes.
        energy_kwh (float): The estimated energy consumed by the transaction in kilowatt-hours.
    """
    tx_hash: str
    size: int
    energy_kwh: float

@strawberry.type
class DailyEnergy:
    """
    A data type representing the total energy consumption for the last N days.

    Attributes:
        date (str): The date of the energy usage in YYYY-MM-DD format.
        total_energy_kwh (float): The total estimated energy consumed on that day in kilowatt-hours.
    """
    date: str
    total_energy_kwh: float
