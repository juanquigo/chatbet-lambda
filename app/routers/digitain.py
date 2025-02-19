from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from app.schemas import DigitainOddsRequest, DigitainOddsResponse
from app.services.odds_service import get_odds

router = APIRouter()


@router.get("/odds", response_model=DigitainOddsResponse)
async def digitain_odds(params: Annotated[dict, Depends(DigitainOddsRequest)]) -> JSONResponse:
    """Get digitain odds based on the provided parameters.

    Args:
        params (dict): The parameters for the odds request.

    Returns:
        dict: The odds data.

    """
    return await get_odds("digitain", **params.model_dump(exclude_none=True))
