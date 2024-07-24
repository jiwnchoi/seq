from typing import Any, Iterable

from seq.utils import jaccard_similarity


class Event:
  def __init__(self, value: Any, position: int, occurences: Iterable) -> None:
    self.position = position
    self.occurences = set(occurences)
    self.value = value

  def __hash__(self) -> int:
    return (self.position, self.value).__hash__()

  def __eq__(self, other: "Event") -> bool:
    return self.position == other.position and self.value == other.value

  def __repr__(self) -> str:
    return f"Token(Position={self.position}, Value={self.value}, # Occurences={len(self.occurences)})"

  def __str__(self) -> str:
    return self.__repr__()

  def diff(self, e: "Event") -> int:
    return jaccard_similarity(self.occurences, e.occurences)
