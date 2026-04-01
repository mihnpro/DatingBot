from dataclasses import dataclass

@dataclass
class ProcessLikeCommand:
    from_user_id: int
    to_user_id: int