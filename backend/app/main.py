from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from .summarizer import Summarizer
from fastapi.middleware.cors import CORSMiddleware

class SummarizeRequest(BaseModel):
    text: str
    max_length: int = 130
    min_length: int = 30

app = FastAPI(title="AI Text Summarizer")

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize summarizer (CPU by default, set device=0 for GPU)
summ = Summarizer(model_name="sshleifer/distilbart-cnn-12-6", device=-1)

@app.post("/summarize")
async def summarize(req: SummarizeRequest):
    try:
        if not req.text or len(req.text.strip()) == 0:
            raise HTTPException(status_code=400, detail="Empty text")
        summary = summ.summarize(req.text, max_length=req.max_length, min_length=req.min_length)
        return {"summary": summary}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
