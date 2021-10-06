from typing import List
from fastapi import APIRouter
import uuid
import json

from app.core import blockchain
from app.core.blockchain import Blockchain
from app.schemas.transaction import Transaction

router = APIRouter(
    prefix='/blockchain',
    tags=['blockchain'],
)

node_info = dict()
blockchain = Blockchain()


@router.on_event('startup')
async def node_startup():
    global node_info
    node_info['uuid'] = uuid.uuid1().__str__()


@router.get('/mine')
async def mine():
    proof = blockchain.mine_block()
    message = {
        'type': 'transfer',
        'object': 'coin',
        'amount': 1,
    }
    blockchain.add_transaction(
        source=None,
        destination=node_info['uuid'],
        message=Blockchain.Message(content=message),
    )
    block = blockchain.add_block(proof=proof)
    return {
        'success': True,
        'index': block.index,
        'timestamp': block.timestamp,
        'proof': block.proof,
        'prevhash': block.prevhash,
        'transactions': block.transactions,
    }


@router.post('/transactions/new')
def add_transaction(transaction: Transaction):
    index = blockchain.add_transaction(**transaction.dict())
    return {'success': True, 'block_index': index}


@router.get('/chain')
async def get_chain():
    return blockchain._chain


@router.get('/nodes/all')
async def get_nodes():
    return blockchain._nodes


@router.post('/nodes/register')
async def register_nodes(new_nodes: List[str]):
    prev_size = len(blockchain._nodes)
    blockchain._nodes.update(new_nodes)
    new_size = len(blockchain._nodes)
    if new_size > prev_size:
        return {'message': f'successfully added {new_size - prev_size} new nodes'}
    return {'message': 'no new nodes added'}


@router.get('/nodes/resolve')
async def resolve_conflicts():
    if blockchain.resolve_conflict():
        return {
            'message': 'chain was updated'
        }
    return {
        'message': 'chain is already up to date'
    }