from fastapi import FastAPI
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from fastapi.testclient import TestClient
from api.v1 import routes
import sys
sys.dont_write_bytecode = True

app = FastAPI(debug=True)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

app.include_router(routes.router)

@app.get("/")
def read_root():
    return {"Hello": "World"}

# client = TestClient(app, base_url="http://127.0..0.1:5000")

# uvicorn.run(app, host="127.0.0.1", port=5000)
# if __name__ == "__main__":
#     uvicorn.run("main:app", host="127.0.0.1", port=5000, reload=True)