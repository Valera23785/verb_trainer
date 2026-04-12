
from dataclasses import dataclass, field
from datetime import date
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
class VerbProgress:
    next_review: date
    status: str = "new" 
    consecutive_errors: int = 0
    consecutive_correct: int = 0
    total_correct: int = 0
    total_attempts: int = 0

@dataclass
class UserProgress:
    verbs: dict[int, VerbProgress] = field(default_factory=dict)
    last_session: date = field(default_factory=date.today)
    streak: int = 0