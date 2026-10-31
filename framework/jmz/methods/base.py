from dataclasses import dataclass, field
from typing import List, Dict, Any


@dataclass
class Method:
    name: str = ""
    chips: List[str] = field(default_factory=list)
    offline: bool = False
    needs_hardware: List[str] = field(default_factory=list)
    ios_max: float = 99.0
    description: str = ""

    def supports(self, chip: str, ios: float) -> bool:
        return chip in self.chips and ios <= self.ios_max

    def steps(self) -> List[str]:
        return []

    def run(self, device: Dict[str, Any]) -> Dict[str, Any]:
        raise NotImplementedError


class Registry:
    def __init__(self):
        self._m: List[Method] = []

    def add(self, m: Method):
        self._m.append(m)

    def all(self) -> List[Method]:
        return list(self._m)

    def pick(self, chip: str, ios: float) -> Method | None:
        for m in self._m:
            if m.supports(chip, ios):
                return m
        return None
