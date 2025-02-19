from .base_mapper import BaseMapper

RESULT_STAKE_ID = 1
HANDICAP_STAKE_ID = 2
OVER_UNDER_STAKE_ID = 3
CODE_OF_STAKE_1 = 1
CODE_OF_STAKE_2 = 2


class DigitainMapper(BaseMapper):
    def pair_stakes(self, stakes: list) -> tuple:
        """Pairs stakes based on specific criteria.

        This method takes a list of stakes and pairs them based on their 'SS', 'ARG', and 'CD' values.
        If a stake has a corresponding pair in the list, both stakes are added to the paired_stakes list.
        If not, the stake is stored in a dictionary for future pairing.

        Args:
            stakes (list): A list of stakes, where each stake is a dictionary containing 'SS', 'ARG', and 'CD' keys.

        Returns:
            tuple: A tuple containing paired stakes. Each element in the tuple is a pair of stakes.

        """
        stake_dict = {}
        paired_stakes = []

        for stake in stakes:
            ss, arg, cd = stake["SS"], stake["ARG"], stake["CD"]
            if ss:
                key = (ss, abs(arg), cd)
                pair_key = (
                    ss,
                    abs(arg),
                    CODE_OF_STAKE_1 if cd == CODE_OF_STAKE_2 else 2,
                )
            else:
                key = (ss, arg, cd)
                pair_key = (ss, arg, CODE_OF_STAKE_1 if cd == CODE_OF_STAKE_2 else 2)

            if pair_key in stake_dict:
                paired_stakes.append((stake_dict.pop(pair_key), stake))
            else:
                stake_dict[key] = stake

        return paired_stakes

    def calculate_main_market(self, paired_stakes: tuple) -> tuple:
        """Calculate the main market from paired stakes.

        This method takes a tuple of paired stakes, calculates the absolute difference
        between the "FCR" values of each pair, and returns the pair with the smallest
        difference.

        Args:
            paired_stakes (tuple): A tuple containing pairs of stakes. Each pair is a tuple
                       of two dictionaries, where each dictionary contains an "FCR" key.

        Returns:
            tuple: The pair of stakes with the smallest absolute difference in "FCR" values.

        """
        calculated_factors = {}
        for index, pair in enumerate(paired_stakes):
            calculated_factors[index] = abs(pair[0]["FCR"] - pair[1]["FCR"])
        min_index = min(calculated_factors, key=calculated_factors.get)
        return paired_stakes[min_index]

    def get_result_stake(self, stake: dict[str], language_code_id: str) -> dict[str]:
        """Generate a dictionary containing the result stake information for home team, away team, and tie.

        Args:
            stake (dict[str]): A dictionary containing stake information with keys as integers (0, 1, 2)
                               and values as dictionaries with keys "NM", "PFF", "FCR", and "ID".
            language_code_id (str): The language code identifier used to extract the team names.

        Returns:
            dict[str]: A dictionary with the result stake information structured for home team, away team, and tie.

        """
        return {
            "result": {
                "homeTeam": {
                    "name": stake[1]["NM"][language_code_id],
                    "profit": stake[1]["PFF"],
                    "odds": stake[1]["FCR"],
                    "betId": stake[1]["ID"],
                },
                "awayTeam": {
                    "name": stake[2]["NM"][language_code_id],
                    "profit": stake[2]["PFF"],
                    "odds": stake[2]["FCR"],
                    "betId": stake[2]["ID"],
                },
                "tie": {
                    "name": stake[0]["NM"][language_code_id],
                    "profit": stake[0]["PFF"],
                    "odds": stake[0]["FCR"],
                    "betId": stake[0]["ID"],
                },
            },
        }

    def get_over_under_stake(
        self,
        stake: dict[str],
        language_code_id: str,
    ) -> dict[str]:
        """Process the given stake data to map over and under stakes with their respective details.

        Args:
            stake (dict[str]): A dictionary containing stake information.
            language_code_id (str): The language code identifier to fetch the name of the stake.

        Returns:
            dict[str]: A dictionary containing mapped over and under stake data.

        """
        paired_stakes = self.pair_stakes(stake)
        calculated_stakes = self.calculate_main_market(paired_stakes)
        mapped_data = {}
        for stake_item in calculated_stakes:
            mapped_stake = {
                "name": f"{stake_item['NM'].get(language_code_id, '')} {stake_item['ARG']}",
                "profit": stake_item["PFF"],
                "odds": stake_item["FCR"],
                "betId": stake_item["ID"],
            }

            if stake_item["CD"] == CODE_OF_STAKE_1:
                mapped_data["over"] = mapped_stake
            elif stake_item["CD"] == CODE_OF_STAKE_2:
                mapped_data["under"] = mapped_stake

        return {"over_under": mapped_data}

    def get_handicap_stake(self, stake: dict[str], language_code_id: str) -> dict[str]:
        """Calculate and map handicap stakes for a given stake and language code.

        Args:
            stake (dict[str]): A dictionary containing stake information.
            language_code_id (str): The language code identifier for localization.

        Returns:
            dict[str]: A dictionary containing the mapped handicap stakes with keys 'homeTeam' and 'awayTeam'.

        """
        paired_stakes = self.pair_stakes(stake)
        calculated_stakes = self.calculate_main_market(paired_stakes)
        mapped_data = {}
        for stake_item in calculated_stakes:
            mapped_stake = {
                "name": f"{stake_item['NM'].get(language_code_id, '')} {stake_item['ARG']}",
                "profit": stake_item["PFF"],
                "odds": stake_item["FCR"],
                "betId": stake_item["ID"],
            }

            if stake_item["CD"] == CODE_OF_STAKE_1:
                mapped_data["homeTeam"] = mapped_stake
            elif stake_item["CD"] == CODE_OF_STAKE_2:
                mapped_data["awayTeam"] = mapped_stake

        return {"handicap": mapped_data}

    def map_odds(self, data: dict[str]) -> dict[str]:
        """Map the given data to a dictionary containing various betting odds.

        Args:
            data (dict[str]): A dictionary containing the input data.
                      Expected keys are "grouped_stks" and "language_code_id".

        Returns:
            dict[str]: A dictionary containing the mapped betting odds with keys such as
                   "success", "main_market", "result", "over_under", "handicap", "result_regular_time", "score",
                   "both_teams_to_score", "double_chance", "half_time_total",
                   "half_time_result", "half_time_handicap", and "win".

        """
        stakes = data["grouped_stks"]
        language_code_id = str(data["language_code_id"])

        return {
            "status": "success",
            "main_market": "result",
            **self.get_result_stake(stakes[RESULT_STAKE_ID], language_code_id),
            "result_regular_time": None,
            "score": None,
            "both_teams_to_score": None,
            "double_chance": None,
            **self.get_over_under_stake(stakes[OVER_UNDER_STAKE_ID], language_code_id),
            **self.get_handicap_stake(stakes[HANDICAP_STAKE_ID], language_code_id),
            "half_time_total": None,
            "half_time_result": None,
            "half_time_handicap": None,
            "win": None,
        }
