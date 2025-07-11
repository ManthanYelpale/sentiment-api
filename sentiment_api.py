from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional
import torch
import numpy as np
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import os

app = FastAPI()

class TextInput(BaseModel):
    text: str
    language: Optional[str] = "en"  # Default language is English

class BatchInput(BaseModel):
    texts: List[str]
    language: Optional[str] = "en"

# Load both models
ml_model_name = "nlptown/bert-base-multilingual-uncased-sentiment"
ml_tokenizer = AutoTokenizer.from_pretrained(ml_model_name)
ml_model = AutoModelForSequenceClassification.from_pretrained(ml_model_name)

hi_model_name = "ai4bharat/indic-bert-sentiment"
hi_tokenizer = AutoTokenizer.from_pretrained(hi_model_name)
hi_model = AutoModelForSequenceClassification.from_pretrained(hi_model_name)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
ml_model.to(device).eval()
hi_model.to(device).eval()

def analyze_multilingual(text: str):
    inputs = ml_tokenizer.encode_plus(text, return_tensors="pt", truncation=True, max_length=512)
    inputs = {k: v.to(device) for k, v in inputs.items()}
    with torch.no_grad():
        outputs = ml_model(**inputs)
        probs = torch.softmax(outputs.logits, dim=1).cpu().numpy()[0]
        stars = int(np.argmax(probs)) + 1
        if stars <= 2:
            label = "negative"
        elif stars == 3:
            label = "neutral"
        else:
            label = "positive"
        return {
            "1_star": float(probs[0]),
            "2_star": float(probs[1]),
            "3_star": float(probs[2]),
            "4_star": float(probs[3]),
            "5_star": float(probs[4]),
            "predicted_stars": stars,
            "label": label
        }

def analyze_hindi(text: str):
    inputs = hi_tokenizer(text, return_tensors="pt", truncation=True, max_length=512)
    inputs = {k: v.to(device) for k, v in inputs.items()}
    with torch.no_grad():
        logits = hi_model(**inputs).logits
        probs = torch.softmax(logits, dim=1).cpu().numpy()[0]
        label = ["negative", "neutral", "positive"][np.argmax(probs)]
        return {
            "neg": float(probs[0]),
            "neu": float(probs[1]),
            "pos": float(probs[2]),
            "label": label
        }

def route_analysis(text: str, language: str):
    if language.lower() in ["hi", "hindi"]:
        return analyze_hindi(text)
    return analyze_multilingual(text)

@app.get("/")
def root():
    return {"message": "Multilingual Sentiment API is live"}

@app.post("/analyze_single")
def analyze_single(input: TextInput):
    return route_analysis(input.text, input.language)

@app.post("/analyze_batch")
def analyze_batch(input: BatchInput):
    return [route_analysis(text, input.language) for text in input.texts]

# Only for local development
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("sentiment_api:app", host="0.0.0.0", port=port)
