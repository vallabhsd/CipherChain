import hashlib
import json
import time


class Block:
    def __init__(self, index, data, previous_hash, timestamp=None):
        self.index = index
        self.data = data
        self.previous_hash = previous_hash
        self.timestamp = timestamp or time.time()
        self.nonce = 0
        self.hash = self.mine()

    def compute_hash(self):
        block_content = {
            "index": self.index,
            "data": self.data,
            "previous_hash": self.previous_hash,
            "timestamp": self.timestamp,
            "nonce": self.nonce,
        }
        block_string = json.dumps(block_content, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()

    def mine(self, difficulty=4):
        prefix = "0" * difficulty
        while True:
            candidate = self.compute_hash()
            if candidate.startswith(prefix):
                return candidate
            self.nonce += 1


class Blockchain:
    DIFFICULTY = 4

    def __init__(self, chain_file="chain.json"):
        self.chain_file = chain_file
        self.chain = []
        self.load_chain()

        if not self.chain:
            self._create_genesis_block()

    def _create_genesis_block(self):
        genesis = Block(
            index=0,
            data="GENESIS",
            previous_hash="0" * 64,
        )
        self.chain.append(genesis)
        self.save_chain()

    def add_block(self, document_hash):
        previous_block = self.chain[-1]

        new_block = Block(
            index=len(self.chain),
            data=document_hash,
            previous_hash=previous_block.hash,
        )

        self.chain.append(new_block)
        self.save_chain()
        return new_block

    def find_hash(self, document_hash):
        for block in self.chain:
            if block.data == document_hash:
                return block
        return None

    def is_valid(self):
        prefix = "0" * self.DIFFICULTY

        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i - 1]

            if current.hash != current.compute_hash():
                return False

            if current.previous_hash != previous.hash:
                return False

            if not current.hash.startswith(prefix):
                return False

        return True

    def save_chain(self):
        with open(self.chain_file, "w") as f:
            json.dump([{
                "index": b.index,
                "data": b.data,
                "previous_hash": b.previous_hash,
                "timestamp": b.timestamp,
                "nonce": b.nonce,
                "hash": b.hash
            } for b in self.chain], f, indent=2)

    def load_chain(self):
        try:
            with open(self.chain_file, "r") as f:
                data = json.load(f)

            self.chain = []

            for block_data in data:
                block = Block.__new__(Block)
                block.index = block_data["index"]
                block.data = block_data["data"]
                block.previous_hash = block_data["previous_hash"]
                block.timestamp = block_data["timestamp"]
                block.nonce = block_data["nonce"]
                block.hash = block_data["hash"]
                self.chain.append(block)

        except FileNotFoundError:
            self.chain = []

    def print_chain(self):
        print("\n" + "=" * 60)
        print("  CIPHERCHAIN — Blockchain Ledger")
        print("=" * 60)

        for block in self.chain:
            print(f"\n  Block #{block.index}")
            print(f"  Data        : {block.data}")
            print(f"  Prev Hash   : {block.previous_hash[:20]}...")
            print(f"  Block Hash  : {block.hash[:20]}...")
            print(f"  Nonce       : {block.nonce}")

        print("\n" + "=" * 60)
        print(f"  Chain valid : {self.is_valid()}")
        print("=" * 60 + "\n")