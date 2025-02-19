from .base_mapper import BaseMapper

RESULT_STAKE_ID = 1
HANDICAP_STAKE_ID = 2
OVER_UNDER_STAKE_ID = 3
SPANISH_LANGUAGE_CODE = "13"


class DigitainMapper(BaseMapper):
    def pair_stakes(self, stakes):
        stake_dict = {}
        paired_stakes = []

        for stake in stakes:
            SS, ARG, CD = stake["SS"], stake["ARG"], stake["CD"]
            if SS:
                key = (SS, abs(ARG), CD)
                pair_key = (SS, abs(ARG), 1 if CD == 2 else 2)
            else:
                key = (SS, ARG, CD)
                pair_key = (SS, ARG, 1 if CD == 2 else 2)

            if pair_key in stake_dict:
                paired_stakes.append((stake_dict.pop(pair_key), stake))
            else:
                stake_dict[key] = stake

        return paired_stakes

    def calculate_main_market(self, paired_stakes):
        calculated_factors = {}
        for index, pair in enumerate(paired_stakes):
            calculated_factors[index] = abs(pair[0]["FCR"] - pair[1]["FCR"])
        min_index = min(calculated_factors, key=calculated_factors.get)
        return paired_stakes[min_index]

    def get_result_stake(self, stake):
        return {
            "result": {
                "homeTeam": {
                    "name": stake[1]["NM"][SPANISH_LANGUAGE_CODE],
                    "profit": stake[1]["PPF"],
                    "odds": stake[1]["FCR"],
                    "betId": stake[1]["ID"],
                },
                "awayTeam": {
                    "name": stake[2]["NM"][SPANISH_LANGUAGE_CODE],
                    "profit": stake[2]["PPF"],
                    "odds": stake[2]["FCR"],
                    "betId": stake[2]["ID"],
                },
                "tie": {
                    "name": stake[0]["NM"][SPANISH_LANGUAGE_CODE],
                    "profit": stake[0]["PPF"],
                    "odds": stake[0]["FCR"],
                    "betId": stake[0]["ID"],
                },
            },
        }

    def get_over_under_stake(self, stake):
        paired_stakes = self.pair_stakes(stake)
        calculated_stakes = self.calculate_main_market(paired_stakes)
        mapped_data = {}
        for stake in calculated_stakes:
            mapped_stake = {
                "name": f"{stake['NM'].get(SPANISH_LANGUAGE_CODE, '')} {stake['ARG']}",
                "profit": stake["PPF"],
                "odds": stake["FCR"],
                "betId": stake["ID"],
            }

            if stake["CD"] == 1:
                mapped_data["over"] = mapped_stake
            elif stake["CD"] == 2:
                mapped_data["under"] = mapped_stake

        return {"over_under": mapped_data}

    def get_handicap_stake(self, stake):
        paired_stakes = self.pair_stakes(stake)
        calculated_stakes = self.calculate_main_market(paired_stakes)
        mapped_data = {}
        for stake in calculated_stakes:
            mapped_stake = {
                "name": f"{stake['NM'].get(SPANISH_LANGUAGE_CODE, '')} {stake['ARG']}",
                "profit": stake["PPF"],
                "odds": stake["FCR"],
                "betId": stake["ID"],
            }

            if stake["CD"] == 1:
                mapped_data["homeTeam"] = mapped_stake
            elif stake["CD"] == 2:
                mapped_data["awayTeam"] = mapped_stake

        return {"handicap": mapped_data}

    def map_odds(self, data):
        stakes = data["grouped_stks"]
        return {
            "success": True,
            "main_market": "result",
            **self.get_result_stake(stakes[RESULT_STAKE_ID]),
            "result_regular_time": None,
            "score": None,
            "both_teams_to_score": None,
            "double_chance": None,
            **self.get_over_under_stake(stakes[OVER_UNDER_STAKE_ID]),
            **self.get_handicap_stake(stakes[HANDICAP_STAKE_ID]),
            "half_time_total": None,
            "half_time_result": None,
            "half_time_handicap": None,
            "win": None,
        }
