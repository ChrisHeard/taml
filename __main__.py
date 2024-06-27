from fastapi import FastAPI
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.middleware.cors import CORSMiddleware
from .routes.markets_routes import markets_router

def create_app():
    app = FastAPI()
    app.include_router(markets_router)
    app.add_middleware(GZipMiddleware, minimum_size=500)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://127.0.0.1:4200"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
    )
    return app

app = create_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
