
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

app = FastAPI()

class TextInput(BaseModel):
    text: str

class BatchInput(BaseModel):
    texts: List[str]

@app.on_event("startup")
def load_model():
    global tokenizer, model, device
    model_name = "cardiffnlp/twitter-roberta-base-sentiment"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSequenceClassification.from_pretrained(model_name)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)
    model.eval()

def analyze(text: str):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, max_length=512)
    inputs = {k: v.to(device) for k, v in inputs.items()}
    with torch.no_grad():
        outputs = model(**inputs)
        probs = torch.softmax(outputs.logits, dim=1).cpu().numpy()[0]
        compound = float(probs[2] - probs[0])
        label = "positive" if probs[2] > probs[0] else "negative" if probs[0] > probs[2] else "neutral"
        return {
            "neg": float(probs[0]),
            "neu": float(probs[1]),
            "pos": float(probs[2]),
            "compound": compound,
            "label": label
        }

@app.post("/analyze_single")
def analyze_single(input: TextInput):
    return analyze(input.text)

@app.post("/analyze_batch")
def analyze_batch(input: BatchInput):
    return [analyze(text) for text in input.texts]
