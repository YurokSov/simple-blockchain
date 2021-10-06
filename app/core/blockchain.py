from __future__ import annotations
import json
from typing import Dict, List, Set, Union
from dataclasses import dataclass
from datetime import datetime
import time
import hashlib
import urllib.request
import urllib.error
import http.client
import logging


class Blockchain:

    @dataclass
    class Message:
        content: Dict[str, Union[str, int, float]]

    @dataclass
    class Transaction:
        source: str
        destination: str
        message: Blockchain.Message

    @dataclass
    class Block:
        index: int
        timestamp: datetime
        proof: int
        prevhash: str
        transactions: List[Blockchain.Transaction]

        def all(self: Blockchain.Block):
            return (self.index, self.timestamp, self.proof, self.prevhash, tuple(self.transactions))

        def __str__(self):
            return 'shit'

    def __init__(self: Blockchain) -> None:
        self._chain: List[Blockchain.Block] = list()
        self._pending_transactions: List[Blockchain.Transaction] = list()
        self._nodes: Set[str] = set()

        self._chain.append(Blockchain.Block(
            index=0, timestamp=time.time(), proof=0, prevhash='', transactions=list()))

    def add_block(self: Blockchain, proof: int) -> Blockchain.Block:
        block = Blockchain.Block(
            index=self.new_index,
            timestamp=time.time(),
            transactions=self._pending_transactions.copy(),
            proof=proof,
            prevhash=self._hash(self.top),
        )
        self._pending_transactions.clear()
        self._chain.append(block)
        return block

    def add_transaction(self: Blockchain, source, destination, message) -> int:
        self._pending_transactions.append(
            Blockchain.Transaction(
                source=source, destination=destination, message=message)
        )
        return self.top.index + 1

    def mine_block(self: Blockchain):
        proof: int = 0
        while not Blockchain._checkproof(proof, self.top.proof):
            proof += 1
        return proof

    def resolve_conflict(self: Blockchain) -> bool:
        maxlen = len(self._chain)
        bestchain = None
        for node in self._nodes:
            request = urllib.request.Request(
                ''.join(['http://', node, '/blockchain/chain']))
            try:
                resp: http.client.HTTPResponse = urllib.request.urlopen(request)
            except urllib.error.URLError as err:
                logging.warning('Node %s not reachable', node)
                continue
            if resp.getcode() != 200:
                continue
            content = json.loads(resp.read().decode())
            chain = [Blockchain.Block(**block_dict) for block_dict in content]
            if len(chain) > maxlen and Blockchain._verify_chain(chain):
                maxlen = len
                bestchain = chain
        if bestchain != None:
            self._chain = bestchain
            return True
        return False

    @staticmethod
    def _checkproof(proof: int, prevproof: int) -> bool:
        checkstr = ''.join([str(prevproof), str(proof)])
        hashed = hashlib.sha256(checkstr.encode()).hexdigest()
        return hashed[:4] == '0000'

    @staticmethod
    def _verify_chain(chain: List[Blockchain.Block]) -> bool:
        for p, c in zip(chain, chain[1:]):
            if Blockchain._hash(p) != c.prevhash or not Blockchain._checkproof(c.proof, p.proof):
                return False
        return True

    @staticmethod
    def _hash(block: Blockchain.Block) -> str:
        return hashlib.sha256(str(block.all()).encode()).hexdigest()

    @property
    def top(self: Blockchain) -> Blockchain.Block:
        return self._chain[-1]

    @property
    def new_index(self: Blockchain) -> int:
        return self._chain[-1].index + 1
