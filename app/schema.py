import strawberry

@strawberry.type
class TransactionEnergy:
    tx_hash: str
    size: int
    energy_kwh: float

@strawberry.type
class DailyEnergy:
    date: str
    total_energy_kwh: float