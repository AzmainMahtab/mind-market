from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root_get():
    return {"YEEEBOI !"}
