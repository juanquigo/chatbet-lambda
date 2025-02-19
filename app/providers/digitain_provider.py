import asyncio

from app.services.http_client import get_http_client
from app.settings import get_settings

PROVIDER_NAME = "digitain"
SPANISH_LANGUAGE_CODE = 13


class DigitainProvider:
    def __init__(self):
        settings = get_settings()
        self.provider_settings = settings["providers"][PROVIDER_NAME]

    async def _fetch_stake(self, client, tId, sttId):
        params = {
            "lIds": SPANISH_LANGUAGE_CODE,
            "tIds": tId,
            "sttIds": sttId,
        }
        response = await client.request("get", "/getMatches", params=params)
        return {"sttId": sttId, "matches": response["result"]}

    async def get_odds(self, mId, tId):
        async with get_http_client(self.provider_settings["base_url"]) as client:
            tasks = [self._fetch_stake(client, tId, sttId) for sttId in [1, 2, 3]]
            results = await asyncio.gather(*tasks)
            filtered_match = next(
                filter(lambda match: match["ID"] == mId, results[0]["matches"]), None,
            )
            grouped_stks = {}
            for result in results:
                match = next(
                    filter(lambda match: match["ID"] == mId, result["matches"]), None,
                )
                grouped_stks[result["sttId"]] = (
                    match["STKS"] if match and "STKS" in match else []
                )

            return {
                "success": True,
                "filtered_match": filtered_match,
                "grouped_stks": grouped_stks,
            }
