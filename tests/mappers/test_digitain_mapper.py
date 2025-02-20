import pytest
from app.mappers.digitain_mapper import DigitainMapper


@pytest.fixture
def digitain_mapper():
    return DigitainMapper()


def test_pair_stakes(digitain_mapper):
    stakes = [
        {"SS": 1, "ARG": 2, "CD": 1},
        {"SS": 1, "ARG": -2, "CD": 2},
    ]

    paired = digitain_mapper.pair_stakes(stakes)

    assert len(paired) == 1
    assert paired[0][0]["CD"] == 1
    assert paired[0][1]["CD"] == 2


def test_calculate_main_market(digitain_mapper):
    paired_stakes = [
        ({"FCR": 1.8}, {"FCR": 1.9}),
        ({"FCR": 2.0}, {"FCR": 2.2}),
    ]

    best_stake = digitain_mapper.calculate_main_market(paired_stakes)

    assert best_stake == ({"FCR": 1.8}, {"FCR": 1.9})


def test_get_result_stake(digitain_mapper):
    stake = {
        1: {"NM": {"13": "Home"}, "PFF": 1.5, "FCR": 2.0, "ID": 101},
        2: {"NM": {"13": "Away"}, "PFF": 1.7, "FCR": 2.2, "ID": 102},
        0: {"NM": {"13": "Tie"}, "PFF": 1.6, "FCR": 2.1, "ID": 103},
    }

    result = digitain_mapper.get_result_stake(stake, "13")

    assert result["result"]["homeTeam"]["name"] == "Home"
    assert result["result"]["awayTeam"]["odds"] == 2.2
    assert result["result"]["tie"]["betId"] == 103


def test_map_odds(digitain_mapper):
    data = {
        "grouped_stks": {
            1: [
                {"NM": {"13": "Away"}, "PFF": 1.7, "FCR": 2.2, "ID": 102},
                {"NM": {"13": "Home"}, "PFF": 1.5, "FCR": 2.0, "ID": 101},
                {"NM": {"13": "Tie"}, "PFF": 1.6, "FCR": 2.1, "ID": 103},
            ],
            2: [
                {"NM": {"13": "Over"}, "SS": 1, "ARG": 2.5, "CD": 1, "PFF": 1.5, "FCR": 1.9, "ID": 201},
                {"NM": {"13": "Under"}, "SS": 1, "ARG": -2.5, "CD": 2, "PFF": 1.7, "FCR": 2.1, "ID": 202},
            ],
            3: [
                {"NM": {"13": "Home Handicap"}, "SS": 1, "ARG": 2.5, "CD": 1, "PFF": 1.5, "FCR": 1.9, "ID": 201},
                {"NM": {"13": "Away Handicap"}, "SS": 1, "ARG": -2.5, "CD": 2, "PFF": 1.7, "FCR": 2.1, "ID": 202},
                {"NM": {"13": "Home Handicap"}, "SS": 0, "ARG": 1.0, "CD": 1, "PFF": 1.5, "FCR": 1.9, "ID": 201},
                {"NM": {"13": "Away Handicap"}, "SS": 0, "ARG": 1.0, "CD": 2, "PFF": 1.7, "FCR": 2.1, "ID": 202},
            ],
        },
        "language_code_id": "13",
    }

    mapped_odds = digitain_mapper.map_odds(data)

    assert mapped_odds["status"] == "success"
    assert mapped_odds["main_market"] == "result"
    assert mapped_odds["result"]["homeTeam"]["name"] == "Home"
    assert "over_under" in mapped_odds
