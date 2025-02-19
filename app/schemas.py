from pydantic import BaseModel, Field
from typing import Annotated

SPANISH_LANGUAGE_CODE = 13


class DigitainOddsRequest(BaseModel):
    mId: Annotated[int, Field(ge=-2_147_483_648, le=2_147_483_647)]
    tId: Annotated[int, Field(ge=-2_147_483_648, le=2_147_483_647)]
    lId: Annotated[int, Field(ge=-2_147_483_648, le=2_147_483_647)] = (
        SPANISH_LANGUAGE_CODE
    )
