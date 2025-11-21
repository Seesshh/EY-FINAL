from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello World"}

@app.get("/test")
def test():
    return {"test": "success"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
