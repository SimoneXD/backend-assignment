from unittest.mock import patch

from app.blockchain_energy_utils import (
    get_transaction_energy,
    energy_per_transaction_for_block,
    total_energy_per_day_last_x_days,
    total_energy_for_wallet,
    ENERGY_PER_BYTE_KWH
)
from app.schema import TransactionEnergy, DailyEnergy

# Sample data
MOCK_TX = {'hash': 'tx123', 'size': 250}
MOCK_BLOCK = {'tx': [MOCK_TX, {'hash': 'tx456', 'size': 300}]}
MOCK_BLOCKS = [{'hash': 'block1'}]
MOCK_ADDR_TXS_RESPONSE = {'txs': [{'hash': 'txA', 'size': 200}, {'hash': 'txB', 'size': 300}]}


def test_get_transaction_energy():
    tx_energy = get_transaction_energy(MOCK_TX)
    assert isinstance(tx_energy, TransactionEnergy)
    assert tx_energy.tx_hash == 'tx123'
    assert tx_energy.size == 250
    assert tx_energy.energy_kwh == 250 * ENERGY_PER_BYTE_KWH


@patch("app.blockchain_energy_utils.request", return_value=MOCK_BLOCK)
def test_energy_per_transaction_for_block(mock_request):
    result = energy_per_transaction_for_block("dummy_hash")
    assert len(result) == 2
    assert result[0].tx_hash == 'tx123'
    assert result[1].tx_hash == 'tx456'
    assert result[0].energy_kwh == 250 * ENERGY_PER_BYTE_KWH


@patch("app.blockchain_energy_utils.request")
@patch("app.blockchain_energy_utils.energy_per_transaction_for_block")
def test_total_energy_per_day_last_x_days(mock_energy_per_block, mock_request):
    mock_request.return_value = MOCK_BLOCKS
    mock_energy_per_block.return_value = [
        TransactionEnergy(tx_hash="tx1", size=100, energy_kwh=456.0)
    ]
    result = total_energy_per_day_last_x_days(2)
    assert len(result) == 2
    assert isinstance(result[0], DailyEnergy)
    assert result[0].total_energy_kwh == 456.0


@patch("app.blockchain_energy_utils.request")
def test_total_energy_for_wallet(mock_request):
    # Simulate two pages: one with data, one empty
    mock_request.side_effect = [
        {'txs': [{'hash': 'txA', 'size': 100}, {'hash': 'txB', 'size': 200}]},
        {'txs': []}
    ]
    result = total_energy_for_wallet("some_address")
    expected = (100 + 200) * ENERGY_PER_BYTE_KWH
    assert result == expected
