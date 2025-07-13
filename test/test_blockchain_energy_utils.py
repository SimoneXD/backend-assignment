import pytest
from unittest.mock import patch
from app import blockchain_energy_utils

@pytest.fixture
def mock_block():
    return {
        "tx": [
            {"hash": "c9bd458b72b465e28aaad09d440284faf42d949c9e7fe4e3dada79ef7d2941a4", "size": 206},
            {"hash": "00ffe5184952a7ce7d83e8cd8da01ecc6664409740f29d8c53b42b2438ed25cf", "size": 222},
            {"hash": "3f8a58b3273ce5c041f8894710fb8452e617a0ad46ea3d3ed49ea4cec208631e", "size": 192}
        ]
    }

@pytest.fixture
def mock_blocks_by_day():
    return [
        {"hash": "blockhash1"}
    ]

@pytest.fixture
def mock_block_for_day():
    return {
        "tx": [
            {"hash": "tx1", "size": 100},
            {"hash": "tx2", "size": 200}
        ]
    }

@pytest.fixture
def mock_tx_list():
    return [
        {"hash": "tx1", "size": 100},
        {"hash": "tx2", "size": 200}
    ]

def test_energy_per_transaction_for_block(mock_block):
    with patch("app.blockchain_energy_utils.get_block_by_hash", return_value=mock_block):
        results = blockchain_energy_utils.energy_per_transaction_for_block(
            "000000000000000000024c163dc82cd22a1163f5fc19bdf3dc80e3a9be9427ce"
        )
        assert len(results) == 3
        assert results[0].tx_hash == "c9bd458b72b465e28aaad09d440284faf42d949c9e7fe4e3dada79ef7d2941a4"
        assert results[0].size == 206
        assert pytest.approx(results[0].energy_kwh, 0.01) == 939.36
        assert results[1].tx_hash == "00ffe5184952a7ce7d83e8cd8da01ecc6664409740f29d8c53b42b2438ed25cf"
        assert results[1].size == 222
        assert pytest.approx(results[1].energy_kwh, 0.01) == 1012.32
        assert results[2].tx_hash == "3f8a58b3273ce5c041f8894710fb8452e617a0ad46ea3d3ed49ea4cec208631e"
        assert results[2].size == 192
        assert pytest.approx(results[2].energy_kwh, 0.01) == 875.52

def test_total_energy_per_day_last_x_days(mock_blocks_by_day, mock_block_for_day):
    with patch("app.blockchain_energy_utils.get_blocks_by_day", return_value=mock_blocks_by_day), \
        patch("app.blockchain_energy_utils.get_block_by_hash", return_value=mock_block_for_day):
        results = blockchain_energy_utils.total_energy_per_day_last_x_days(1)
        assert len(results) == 1
        expected_energy = (100 + 200) * blockchain_energy_utils.ENERGY_PER_BYTE_KWH
        assert results[0].total_energy_kwh == expected_energy

def test_total_energy_for_wallet(mock_tx_list):
    with patch("app.blockchain_energy_utils.get_transactions_by_address", return_value=mock_tx_list):
        total = blockchain_energy_utils.total_energy_for_wallet("dummyaddress")
        expected = (100 + 200) * blockchain_energy_utils.ENERGY_PER_BYTE_KWH
        assert total == expected
