from pydantic import BaseModel
from fastapi import APIRouter, status
import aiohttp
import asyncio


class CryptoTokenResponse(BaseModel):
    exchange: str
    price: float
    fee: int


class CryptoTokenRequest(BaseModel):
    token_list: list[CryptoTokenResponse]
    lowest_price: int
    highest_price: int


router = APIRouter()


async def fetch_aban_tether():
    """Fetch price from ABAN-TETHER exchange"""
    try:
        url = "https://api.abantether.com/api/v1/feecalculator/coin-info?side=sell&symbol=USDT"
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=aiohttp.ClientTimeout(total=10)) as response:
                if response.status == 200:
                    data = await response.json()
                    return CryptoTokenResponse(
                        exchange="ABAN-TETHER",
                        price=data['data']['irt_min_trade'],
                        fee=int(data['data']['irt_fee'])
                    )
    except Exception as e:
        print(f"Error fetching ABAN-TETHER: {e}")
    return None


async def fetch_nobitex():
    """Fetch price from NOBITEX exchange"""
    try:
        url = "https://apiv2.nobitex.ir/v3/orderbook/USDTIRT"
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=aiohttp.ClientTimeout(total=10)) as response:
                if response.status == 200:
                    data = await response.json()
                    return CryptoTokenResponse(
                        exchange="NOBITEX",
                        price=int(data['lastTradePrice']) / 10,
                        fee=0
                    )
    except Exception as e:
        return None


async def fetch_bitpin():
    """Fetch price from BITPIN exchange"""
    try:
        url = "https://api.bitpin.org/api/v1/mkt/tickers/"
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=aiohttp.ClientTimeout(total=10)) as response:
                if response.status == 200:
                    data = await response.json()
                    usdt_irt = next((item for item in data if item.get('symbol') == "USDT_IRT"), None)
                    if usdt_irt:
                        return CryptoTokenResponse(
                            exchange="BITPIN",
                            price=int(usdt_irt['price']),
                            fee=0
                        )
    except Exception as e:
        print(f"Error fetching BITPIN: {e}")
    return None


@router.get("/token_price", response_model=CryptoTokenRequest, status_code=status.HTTP_200_OK)
async def get_token_price(token_name: str = "USDT"):
    results = await asyncio.gather(
        fetch_aban_tether(),
        fetch_nobitex(),
        fetch_bitpin(),
        return_exceptions=True
    )

    token_list = [token for token in results if token is not None and isinstance(token, CryptoTokenResponse)]

    if not token_list:
        raise ValueError("No exchange data available")

    token_list.sort(key=lambda item: item.price)

    lowest = min(token_list, key=lambda item: item.price)
    highest = max(token_list, key=lambda item: item.price)

    print(f"Lowest: {lowest}")
    print(f"Highest: {highest}")

    return {
        "token_list": token_list,
        "lowest_price": int(lowest.price),
        "highest_price": int(highest.price)
    }
