from datetime import datetime

from sqlmodel import SQLModel, Field

from enum import Enum


class TokenChoice(str, Enum):
    BITCOIN = "bitcoin"
    ETHEREUM = "ethereum"
    RIPPLE = "ripple"
    CARDANO = "cardano"
    SOLANA = "solana"


class CryptoToken(SQLModel, table=True):
    __tablename__ = 'crypto_token'

    id: int | None = Field(primary_key=True, default=None)
    token_name: TokenChoice = Field(max_length=1000)
    price: float = Field(gt=0)
    created_at: datetime = Field(default_factory=datetime.utcnow)
