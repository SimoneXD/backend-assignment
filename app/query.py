import strawberry
from typing import List
from .schema import TransactionEnergy, DailyEnergy
from .blockchain_energy_utils import (
    energy_per_transaction_for_block,
    total_energy_per_day_last_x_days,
    total_energy_for_wallet
)

@strawberry.type
class Query:
    @strawberry.field
    def energy_per_transaction(self, block_hash: str) -> List[TransactionEnergy]:
        return energy_per_transaction_for_block(block_hash)

    @strawberry.field
    def total_energy_last_days(self, days: int) -> List[DailyEnergy]:
        return total_energy_per_day_last_x_days(days)

    @strawberry.field
    def total_wallet_energy(self, address: str) -> float:
        return total_energy_for_wallet(address)
    
schema = strawberry.Schema(query=Query)