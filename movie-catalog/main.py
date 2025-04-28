import uvicorn
from fastapi import FastAPI, Request

app = FastAPI(
    title="Movie Catalog",
)


@app.get("/")
async def root(
    request: Request,
):
    docs_url = request.url.replace(path="/docs")
    return {
        "message": "This is the root of the movie catalog API",
        "docs": str(docs_url),
    }
