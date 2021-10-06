from fastapi import APIRouter
from fastapi.params import Query
import names
import random
import csv


router = APIRouter(
    prefix='/words',
    tags=['words'],
)


@router.on_event('startup')
async def load_words():
    with open('resources/nouns.csv') as file:
        global nouns
        nouns = [word[0] for word in csv.reader(file)]
    
    with open('resources/adjectives.csv') as file:
        global adjectives
        adjectives = [word[0] for word in csv.reader(file)]


@router.get('/names')
async def get_names(amount: int = 0):
    return {"names": [names.get_full_name() for _ in range(amount)]}


@router.get('/nouns/all')
async def get_nouns():
    return {"content": nouns}


@router.get('/nouns/random')
async def get_nouns(amount: int = 10):
    return {"content": random.sample(nouns, amount)}


@router.get('/adjectives/all')
async def get_adjectives():
    return {"content": adjectives}


@router.get('/adjectives/random')
async def get_adjectives(amount: int = 10):
    return {"content": random.sample(adjectives, amount)}


@router.get('/nicknames/random')
async def get_nickname():
    return {"content": ' '.join((random.choice(adjectives), random.choice(nouns)))}