import itertools
from typing import Protocol


class SequenceT(Protocol):
    async def get_next(self) -> str:
        """Returns the next sequence to use in a request"""
        raise NotImplementedError


class NumericSequence:
    def __init__(
        self,
        *,
        ending_number: int | None = None,
        starting_number: int = 0,
        jump: int = 1
    ):
        self.starting: int = starting_number
        self.ending: int = ending_number
        self.jump: int = jump

        self.iter = (
            itertools.count()
            if ending_number is None
            else iter(range(self.starting, self.ending, self.jump))
        )

    async def get_next(self) -> str:
        return str(next(self.iter))

    def __next__(self):
        return next(self.iter)

    def __iter__(self):
        return self
