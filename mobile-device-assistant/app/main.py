import os
from fastapi import FastAPI,HTTPException
from dotenv import load_dotenv
from openai import OpenAI
from app.schema.device import SearchRequest,SearchResponse,ExtractRequest,ExtractResponse,SearchResult
from app.services.extraction import extract_device,ExtractionError
from app.services.search import hybrid_search



SUSPICIOUS_PHRASES =[
    "ignore previous",
    "ignore all previous",
    "ignore the above",
    "disregard previous",
    "system prompt",
    "you are now",
    "reveal your instructions",
    "act as",
    "jailbreak",
]

load_dotenv()
client = OpenAI(api_key=os.getenv("api_key"))
app = FastAPI(title="Mobile Device Assistant")
def is_suspicious(text:str)->bool:
    lowered = text.lower()
    return any(phrase in lowered for phrase in SUSPICIOUS_PHRASES)

@app.post("/extract", response_model=ExtractResponse)
async def extract(request:ExtractRequest):
    if is_suspicious(request.text):
        raise HTTPException(status_code=400, detail="Suspicious input rejected.")
    try:
        return extract_device(request.text)
    except ExtractionError as e:
        raise HTTPException(status_code=502, detail=str(e))


@app.post("/search", response_model=SearchResponse)
async def search(request:SearchRequest):
    results = hybrid_search(request.q, k=3)
    return SearchResponse(
        results=[SearchResult(document=doc, score=score) for doc, score in results]
    )
