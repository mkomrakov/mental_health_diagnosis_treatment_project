import pandas as pd
import logging
import uvicorn
import os
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from dotenv import dotenv_values
import numpy as np


class FormData(BaseModel):
        age: int
        gender: str
        diagnosis: str
        symptom_severity: int
        mood_score: int
        sleep_quality: int
        physical_activity: int
        therapy_type: str
        treatment_duration: int
        stress_level: int
        outcome: str
        treatment_progress: int



class MentalDataBackend:
    def __init__(self):
        self.setup_logging()
        self.app = FastAPI()
        self.setup_routes()
        self.PATH = dotenv_values('.env')['PATH']


    def setup_logging(self):
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)


    def setup_routes(self):
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"]
        )

        @self.app.post("/api/submit/")
        async def submit_data(data: FormData):
            return await self.submit_data(data)


        @self.app.get('/')
        async def main():
            return {'message': "Hello from FastAPI."}


    async def submit_data(self, data: FormData):
        self.logger.info(f"Received data: {data}")

        if not os.path.exists(self.PATH):
            raise FileNotFoundError(f"File not found")

        df = pd.read_csv(self.PATH)

        last_person_id = df["Patient ID"].max()
        new_person_id = last_person_id + 1 if not pd.isnull(last_person_id) else 1
        
        new_data = {
            "Patient ID": int(new_person_id),
            "Gender": data.gender,
            "Age": data.age,
            "Diagnosis": data.diagnosis,
            "Symptom Severity (1-10)": data.symptom_severity,
            "Sleep Quality (1-10)": data.sleep_quality,
            "Physical Activity (hrs/week)": data.physical_activity,
            "Therapy Type": data.therapy_type,
            "Treatment Duration (weeks)": data.treatment_duration,
            "Stress Level (1-10)": data.stress_level,
            "Outcome": data.outcome,
            "Treatment Progress (1-10)": data.treatment_progress
        }
        self.logger.info(f"Received data: {new_data}")
        ordered_columns = ["Patient ID", "Gender", "Age", "Diagnosis", "Symptom Severity (1-10)", "Sleep Quality (1-10)", "Physical Activity (hrs/week)", "Therapy Type", "Treatment Duration (weeks)", "Stress Level (1-10)", "Outcome", "Treatment Progress (1-10)"]
        print(df.columns.tolist())
        print(new_data)
        df = pd.concat([df, pd.DataFrame([new_data], columns=ordered_columns)], ignore_index=True)
        df.to_csv(self.PATH, index=False)

        return {"message": "Data taken successfully!", "data":new_data}

    def run(self):
        # start FastAPI
        uvicorn.run(self.app, host='0.0.0.0', port=8000)


if __name__ == '__main__':
    backend = MentalDataBackend()
    backend.run()
