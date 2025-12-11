from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from uuid import uuid4

app = FastAPI(title="Service A - Results API")

RESULTS_DB = {}

class AnalysisResult(BaseModel):
  id: str | None = None
  image_url: str
  people_count: int

@app.post("/results", response_model=AnalysisResult)
def save_result(result: AnalysisResult):
  if result.id is None:
    result.id = str(uuid4())
  RESULTS_DB[result.id] = result
  return result

@app.get("/results", response_model=List[AnalysisResult])
def list_results():
  return list(RESULTS_DB.values())
