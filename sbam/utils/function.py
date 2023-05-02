from dataclasses import dataclass

@dataclass
class Function:
    name: str
    args: list[tuple[str, str]]
