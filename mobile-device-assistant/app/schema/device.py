from pydantic import BaseModel,ValidationError, Field,field_validator
from typing import Literal

class Device(BaseModel):
    brand: str = Field(..., description="Brand of the device")
    model: str = Field(..., description="Model of the device")
    specs: dict[str, str] = Field(..., description="Specifications of the device")
    release_year: int = Field(..., description="Release year of the device")
    price_tier: Literal["budget", "mid-range", "flagship"] = Field(..., description="Price tier of the device")

class ExtractRequest(BaseModel):
    text: str = Field(...,max_length=500, description="Input text for specification extraction")

class ExtractResponse(BaseModel):
    brand: str = Field(..., description="Brand of the device")
    model: str = Field(..., description="Model of the device")
    specs: dict[str, str] = Field(..., description="Specifications of the device")
    release_year: int = Field(..., description="Release year of the device")
    price_tier: Literal["budget", "mid-range", "flagship"] = Field(..., description="Price tier of the device")

class SearchRequest(BaseModel):
    q: str = Field(..., description="Input for device search")

class SearchResult(BaseModel):
    document: str = Field(..., description="Document containing device information")
    score: float = Field(..., description="One ranked result")

class SearchResponse(BaseModel):
    results: list[SearchResult] = Field(..., description="List of search results")