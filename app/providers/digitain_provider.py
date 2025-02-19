import asyncio

from fastapi import HTTPException

from app.providers.base_provider import BaseProvider
from app.services.http_client import HTTPClient, get_http_client
from app.settings import get_settings

PROVIDER_NAME = "digitain"


class DigitainProvider(BaseProvider):
    def __init__(self) -> None:
        """Initialize the DigitainProvider with settings."""
        settings = get_settings()
        self.provider_settings = settings["providers"][PROVIDER_NAME]

    async def _fetch_stake(
        self,
        client: HTTPClient,
        tournament_id: int,
        stake_id: int,
        language_code_id: int,
    ) -> dict[str]:
        params = {
            "lIds": language_code_id,
            "tIds": tournament_id,
            "sttIds": stake_id,
        }
        response = await client.request("get", "/getMatches", params=params)
        return {"sttId": stake_id, "matches": response["result"]}

    async def get_odds(self, match_id: int, tournament_id: int, language_code_id: int) -> dict[str]:
        """Asynchronously fetches and returns the odds for a specific match.

        Args:
            match_id (int): The ID of the match to fetch odds for.
            tournament_id (int): The ID of the tournament the match belongs to.
            language_code_id (int): The language code ID for localization.

        Returns:
            dict[str]: A dictionary containing the success status, filtered match details,
                       grouped stakes by sttId, and the language code ID.

        Raises:
            HTTPException: If the match is not found.

        """
        async with get_http_client(self.provider_settings["base_url"]) as client:
            tasks = [self._fetch_stake(client, tournament_id, sttId, language_code_id) for sttId in [1, 2, 3]]
            results = await asyncio.gather(*tasks)
            filtered_match = next(
                filter(lambda match: match["ID"] == match_id, results[0]["matches"]),
                None,
            )

            if filtered_match is None:
                raise HTTPException(status_code=404, detail="Match not found")

            grouped_stks = {}
            for result in results:
                match = next(
                    filter(lambda match: match["ID"] == match_id, result["matches"]),
                    None,
                )
                grouped_stks[result["sttId"]] = match["STKS"] if match and "STKS" in match else []

            return {
                "filtered_match": filtered_match,
                "grouped_stks": grouped_stks,
                "language_code_id": language_code_id,
            }
