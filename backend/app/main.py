from fastapi import FastAPI

app = FastAPI(
    title="DGCA FDTL Compliance System",
    version="1.0"
)

@app.get("/")
def root():
    return {"message": "DGCA FDTL system running"}