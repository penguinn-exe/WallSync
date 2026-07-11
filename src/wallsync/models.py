from collections import Counter
from dataclasses import dataclass, field


@dataclass
class CollectionStats:
    images: int = 0
    folders: int = 0
    total_size: int = 0

    formats: Counter = field(default_factory=Counter)
    resolutions: Counter = field(default_factory=Counter)

    corrupted: int = 0
