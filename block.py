# Defines the Block class: data structure for storing each block in the blockchain. 
# Handles packing/unpacking binary data.

# block.py
import struct
import time
import uuid

class Block:
    FORMAT = "32s d 32s 32s 12s 12s 12s I"

    def __init__(self, prev_hash, timestamp, case_id, evidence_id,
        state, creator, owner, data):
        self.prev_hash = prev_hash
        self.timestamp = timestamp
        self.case_id = case_id
        self.evidence_id = evidence_id
        self.state = state.encode().ljust(12, b'\0')
        self.creator = creator.encode().ljust(12, b'\0')
        self.owner = owner.encode().ljust(12, b'\0')
        self.data = data.encode() + b'\0'
        self.data_length = len(self.data)

    def pack(self):
        header = struct.pack(
            self.FORMAT,
            self.prev_hash,
            self.timestamp,
            self.case_id,
            self.evidence_id,
            self.state,
            self.creator,
            self.owner,
            self.data_length
        )
        return header + self.data

    @staticmethod
    def unpack(binary_data):
        header = binary_data[:struct.calcsize(Block.FORMAT)]
        fields = struct.unpack(Block.FORMAT, header)
        data = binary_data[struct.calcsize(Block.FORMAT):][:fields[7]]
        return Block(*fields[:7], data.rstrip(b'\0').decode())