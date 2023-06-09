from fastapi import FastAPI

app = FastAPI()


@app.get("/api/v1/check_status")
def check_status():
    return {"message": "Hello where!"}
