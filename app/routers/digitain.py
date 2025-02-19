from fastapi import APIRouter, Depends

from app.schemas import DigitainOddsRequest
from app.services.odds_service import get_odds

router = APIRouter()


@router.get("/odds")
async def digitain_odds(params: DigitainOddsRequest = Depends()):
    return await get_odds("digitain", **params.model_dump(exclude_none=True))
