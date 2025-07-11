from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import torch
import numpy as np
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import os

app = FastAPI()

class TextInput(BaseModel):
    text: str

class BatchInput(BaseModel):
    texts: List[str]

# Load model globally
model_name = "nlptown/bert-base-multilingual-uncased-sentiment"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)
model.eval()

def analyze(text: str):
    inputs = tokenizer.encode_plus(text, return_tensors="pt", truncation=True, max_length=512)
    inputs = {k: v.to(device) for k, v in inputs.items()}
    with torch.no_grad():
        outputs = model(**inputs)
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

@app.get("/")
def root():
    return {"message": "API is live"}

@app.post("/analyze_single")
def analyze_single(input: TextInput):
    return analyze(input.text)

@app.post("/analyze_batch")
def analyze_batch(input: BatchInput):
    return [analyze(text) for text in input.texts]

# Only for local development
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("sentiment_api:app", host="0.0.0.0", port=port)
