from aocd import get_data

year, day = [int(v) for v in __file__.split("/")[-3:-1]]
input = "2333133121414131402"


input = get_data(day=day, year=year)


class DiskBlock:
    def __init__(self, id, size, empty, prev_block):
        self.id = id
        self.size = size
        self.empty = empty
        self.prev_block = prev_block
        self.next_block = None

    def __repr__(self):
        return str("." if self.id is None else self.id) * self.size

class Disk:
    def __init__(self, input):
        id = 0
        empty = False
        prev_block = None
        self.first_block = None
        for c in input:
            size = int(c)
            db = DiskBlock(None if empty else id, size, empty, prev_block)
            if prev_block:
                prev_block.next_block = db

            if not self.first_block:
                self.first_block = db
            if not empty:
                id += 1
            prev_block = db
            empty = not empty

        self.last_block = db


    def condensate(self):
        first_empty_block = self.first_block.next_block
        block_to_move = self.last_block
        while True:
            if block_to_move.size > first_empty_block.size:
                block_to_move.size -= first_empty_block.size
                first_empty_block.id = block_to_move.id
                first_empty_block.empty = False
                first_empty_block = first_empty_block.next_block.next_block
                if not first_empty_block or not first_empty_block.empty:
                    break

                if not first_empty_block.empty:
                    raise ValueError("Empty block expected!")
            elif block_to_move.size == first_empty_block.size:
                first_empty_block.id = block_to_move.id
                first_empty_block.empty = False
                first_empty_block = first_empty_block.next_block.next_block
                if not first_empty_block or not first_empty_block.empty:
                    break

                # Detach
                block_to_move.prev_block.next_block = None
                block_to_move = block_to_move.prev_block
                if block_to_move.empty:
                    block_to_move = block_to_move.prev_block
                block_to_move.next_block = None
            else: # <
                split_empty_block = DiskBlock(None, first_empty_block.size - block_to_move.size, True, first_empty_block)
                split_empty_block.next_block = first_empty_block.next_block
                first_empty_block.next_block = split_empty_block

                first_empty_block.id = block_to_move.id
                first_empty_block.empty = False
                first_empty_block.size = block_to_move.size
                first_empty_block = split_empty_block

                block_to_move = block_to_move.prev_block
                if block_to_move.empty:
                    block_to_move = block_to_move.prev_block
                block_to_move.next_block = None

        self.last_block = block_to_move

    def defragment(self):
        block_to_move = self.last_block
        while block_to_move.id > 1:
            target_block = self.first_block
            while (not target_block.empty or target_block.size < block_to_move.size) and target_block.id != block_to_move.id:
                target_block = target_block.next_block

            next_id = block_to_move.id - 1
            if target_block.empty and target_block.size >= block_to_move.size:
                if target_block.size > block_to_move.size:
                    split_empty_block = DiskBlock(None, target_block.size - block_to_move.size, True,
                                                  target_block)
                    split_empty_block.next_block = target_block.next_block
                    target_block.next_block = split_empty_block

                target_block.id = block_to_move.id
                target_block.empty = False
                target_block.size = block_to_move.size

                block_to_move.id = None
                block_to_move.empty = True

            while not block_to_move.id or block_to_move.id != next_id:
                block_to_move = block_to_move.prev_block

        # not important not bothering to update
        self.last_block = None

    @property
    def checksum(self):
        result = 0
        db = self.first_block
        ix = 0
        while db:
            dbv = (db.id or 0) * sum(range(ix, ix + db.size))
            result += dbv
            ix += db.size
            db = db.next_block
        return result

    def __repr__(self):
        result = ""
        db = self.first_block
        while db:
            result += str(db)
            db = db.next_block

        return result

d = Disk(input)
d.condensate()
print(d.checksum)

d = Disk(input)
d.defragment()
print(d)
print(d.checksum)
