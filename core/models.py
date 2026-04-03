
from dataclasses import dataclass, field

@dataclass
class Verb:
    id: int
    english: str
    v2: str
    v3: str
    irregular: bool
    russian: str
    example: str = ''
    # example: str = field(default='')


@dataclass
class UserProgress:
    verb_id: int
    status: str = "new"
    next_review: str = ""
    consecutive_errors: int = 0
    consecutive_correct: int = 0

