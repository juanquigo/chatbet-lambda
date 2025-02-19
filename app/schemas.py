from pydantic import BaseModel, Field


class DigitainOddsRequest(BaseModel):
    mId: int = Field(None, examples=["25275355"])
    tId: int = Field(None, examples=["4584"])
