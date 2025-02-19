from __future__ import annotations

from typing import Annotated, Union

from pydantic import BaseModel, Field

SPANISH_LANGUAGE_CODE = 13


class DigitainOddsRequest(BaseModel):
    match_id: Annotated[int, Field(ge=-2_147_483_648, le=2_147_483_647)]
    tournament_id: Annotated[int, Field(ge=-2_147_483_648, le=2_147_483_647)]
    language_code_id: Annotated[int, Field(ge=-2_147_483_648, le=2_147_483_647)] = SPANISH_LANGUAGE_CODE


class Stake(BaseModel):
    name: str
    profit: Union[float, None]
    odds: float
    betId: int


class Result(BaseModel):
    homeTeam: Stake
    awayTeam: Stake
    tie: Stake


class OverUnder(BaseModel):
    over: Stake
    under: Stake


class Handicap(BaseModel):
    homeTeam: Stake
    awayTeam: Stake


class DigitainOddsResponse(BaseModel):
    status: str
    main_market: str
    result: Result
    result_regular_time: None
    score: None
    both_teams_to_score: None
    double_chance: None
    over_under: OverUnder
    handicap: Handicap
    half_time_total: None
    half_time_result: None
    half_time_handicap: None
    win: None
