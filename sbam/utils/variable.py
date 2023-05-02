from dataclasses import dataclass

@dataclass
class Variable:
    type_: str
    value: str
    name: str

