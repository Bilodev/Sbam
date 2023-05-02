from dataclasses import dataclass


@dataclass
class Token:
    source: str
    line: int
    token: str

    def __repr__(self) -> str:
        return (f'({self.line}, {self.token!r})')
