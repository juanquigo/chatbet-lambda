from typing import Annotated

from pydantic import BaseModel, Field

SPANISH_LANGUAGE_CODE = 13


class DigitainOddsRequest(BaseModel):
    match_id: Annotated[int, Field(ge=-2_147_483_648, le=2_147_483_647)]
    tournament_id: Annotated[int, Field(ge=-2_147_483_648, le=2_147_483_647)]
    language_code_id: Annotated[int, Field(ge=-2_147_483_648, le=2_147_483_647)] = SPANISH_LANGUAGE_CODE
