# Manages the blockchain: loading, saving, verifying, adding/checking evidence, and enforcing rules. 
# Uses Block, encryption, and user_auth

import os
import hashlib
from block import Block
from encryption import encrypt_uuid, encrypt_item_id
import time

BLOCKCHAIN_FILE = "blockchain.dat"

class Blockchain:
    def __init__(self):
        self.blocks = []
        if os.path.exists(BLOCKCHAIN_FILE):
            self.load_blocks()

    def load_blocks(self):
        with open(BLOCKCHAIN_FILE, 'rb') as f:
            while True:
                chunk = f.read(128)
                if not chunk:
                    break
                block = Block.unpack(chunk + f.read(1024))  # adjust if needed
                self.blocks.append(block)

    def save_block(self, block):
        with open(BLOCKCHAIN_FILE, 'ab') as f:
            f.write(block.pack())
        self.blocks.append(block)

    def init(self):
        if not os.path.exists(BLOCKCHAIN_FILE):
            print("Creating genesis block...")
            genesis = Block(
                b"0" * 32,
                0,
                b"0" * 32,
                b"0" * 32,
                "INITIAL",
                "\0" * 12,
                "\0" * 12,
                "Initial block"
            )
            self.save_block(genesis)
        else:
            print("Genesis block already exists.")

    def get_last_hash(self):
        last_block = self.blocks[-1]
        return hashlib.sha256(last_block.pack()).digest()

    def add_evidence(self, case_id, item_id, creator):
        eid_enc = encrypt_item_id(int(item_id))
        cid_enc = encrypt_uuid(case_id)
        block = Block(
            self.get_last_hash(),
            time.time(),
            cid_enc,
            eid_enc,
            "CHECKEDIN",
            creator,
            creator,
            f"Item {item_id} added to case {case_id}"
        )
        self.save_block(block)
        print(f"Item {item_id} added.")

    def checkout(self, item_id):
        print(f"Item {item_id} checked out. (stub)")

    def checkin(self, item_id):
        print(f"Item {item_id} checked in. (stub)")

    def show_cases(self):
        print("Cases (stub)")

    def show_items(self, case_id):
        print(f"Items for case {case_id} (stub)")

    def show_history(self, case_id=None, item_id=None, num_entries=None, reverse=False):
        print("History (stub)")

    def remove_item(self, item_id, reason):
        print(f"Removed item {item_id} for reason: {reason} (stub)")

    def verify(self):
        print("Verifying blockchain...")
        for i in range(1, len(self.blocks)):
            prev_hash = hashlib.sha256(self.blocks[i-1].pack()).digest()
            if self.blocks[i].prev_hash != prev_hash:
                print(f"Block {i} has invalid hash link.")
                return False
        print("Blockchain is valid.")
        return True