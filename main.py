from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Flight Discount Recommender is running"}