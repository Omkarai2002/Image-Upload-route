from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from report_controller import router as report_router
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="GPU Backend API")

# Update these to match your frontend
origins = [
    "https://dev.zypher.nxtqube.com",
    "https://test.zypher.nxtqube.com",
    "https://ai.nxtqube.com",
    "http://localhost:3000",
    "http://localhost:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(report_router, prefix="/api", tags=["Reports"])


@app.get("/")
def root():
    return {"message": "GPU Backend Running!"}
