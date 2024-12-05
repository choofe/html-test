import os
import openai
from fastapi import FastAPI, Query
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Initialize FastAPI app
app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace "*" with specific domains in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load OpenAI API key from environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")
if not openai.api_key:
    raise ValueError("OpenAI API key not set. Please set the OPENAI_API_KEY environment variable.")

# Mock data
body_parts = ["head", "chest", "stomach"]
organs = {
    "head": ["brain", "eyes", "ears"],
    "chest": ["lung", "heart", "kidney"],
    "stomach": ["liver", "intestine", "pancreas"],
}
symptoms = {
    "lung": ["pain", "shortness of breath", "coughing"],
    "heart": ["chest pain", "palpitations", "dizziness"],
    "kidney": ["back pain", "nausea", "frequent urination"],
}

# Serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def read_root():
    """Serve the main HTML file."""
    return FileResponse("static/index.html")

@app.get("/body-parts")
def get_body_parts():
    """Return a list of body parts."""
    return body_parts

@app.get("/organs")
def get_organs(body_part: str = Query(..., description="Body part name")):
    """Return a list of organs based on the selected body part."""
    return organs.get(body_part, [])

@app.get("/symptoms")
def get_symptoms(organ: str = Query(..., description="Organ name")):
    """Return a list of symptoms for the selected organ."""
    return symptoms.get(organ, [])

# Initialize Async OpenAI Client
aclient = openai.AsyncClient()

class DiagnosisRequest(BaseModel):
    symptoms: list[str]

@app.post("/diagnose")
async def get_diagnosis(request: DiagnosisRequest):
    """Generate a list of possible diagnoses based on symptoms."""
    try:
        # Prepare the GPT prompt
        prompt = f"The following symptoms were reported: {', '.join(request.symptoms)}. What are the possible medical diagnoses for these symptoms? Provide a list of possible conditions with a brief explanation for each."

        # Call OpenAI's GPT API asynchronously
        response = await aclient.completions.create(
            model="gpt-3.5-turbo",
            prompt=prompt,
            max_tokens=500,
            temperature=0.7
        )

        # Extract the GPT response
        diagnoses = response.choices[0].text.strip()
        return {"diagnoses": diagnoses}
    except Exception as e:
        return {"error": str(e)}
