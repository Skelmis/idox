from pathlib import Path
from typing import Protocol, Iterator, Any


class SequenceT(Protocol):
    iter: Iterator[Any]

    async def get_next(self) -> str:
        """Returns the next sequence to use in a request"""
        return str(next(self.iter))

    def __next__(self):
        return str(next(self.iter))

    def __iter__(self):
        return self


class NumericSequence(SequenceT):
    def __init__(self, *, ending_number: int, starting_number: int = 0, jump: int = 1):
        self.starting: int = starting_number
        self.ending: int = ending_number
        self.jump: int = jump

        self.iter = iter(range(self.starting, self.ending, self.jump))


class FileSequence(SequenceT):
    def __init__(self, file_path: Path):
        self.iter = iter(file_path.read_text().split("\n"))
