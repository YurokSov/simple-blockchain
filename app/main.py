from fastapi import FastAPI

from .routers import words, blockchain

app = FastAPI()
app.include_router(words.router)
app.include_router(blockchain.router)

nouns = list()
adjectives = list() 


@app.get('/')
async def root():
    print(nouns[:10])
    return {"message": "Goodbye, World!"}


