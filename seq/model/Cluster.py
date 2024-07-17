from __future__ import annotations

from collections import deque

import numpy as np

from .Chunk import Chunk


class Cluster:
  path: deque

  max_start: int
  min_end: int

  def __init__(self, init_chunk: list[Chunk]):
    self.path: deque[Chunk] = deque(init_chunk)
    self.max_start = min([chunk.end for chunk in self.path]) - 1
    self.min_end = max([chunk.start for chunk in self.path]) + 1

  def __len__(self):
    return len(self.path)

  def __getitem__(self, key):
    return self.path[key]

  @property
  def left(self):
    return self.path[0]

  @property
  def right(self):
    return self.path[-1]

  @property
  def height(self):
    return sum([chunk.height for chunk in self.path])

  @property
  def start(self):
    return min([chunk.start for chunk in self.path])

  @property
  def end(self):
    return max([chunk.end for chunk in self.path])

  @property
  def width(self):
    return self.end - self.start

  @property
  def size(self):
    return sum([chunk.size for chunk in self.path])

  @property
  def shape(self):
    return self.height, self.width

  @property
  def sequlet(self):
    canvas = np.zeros(self.shape)

    current_index = 0
    for chunk in self.path:
      canvas[
        current_index : current_index + chunk.height,
        chunk.start - self.start : chunk.end - self.start,
      ] = chunk.subsequence
      current_index += chunk.height
    return canvas

  def can_draw(self, canvas: np.ndarray) -> bool:
    if canvas.shape != self.shape:
      raise ValueError(
        f"Canvas shape must match cluster shape: {canvas.shape} != {self.shape}"
      )
    sequlet = self.sequlet

    if np.all(canvas[sequlet != 0] == 0):
      return True
    return False

  def draw(self, canvas: np.ndarray) -> None:
    if canvas.shape != self.shape:
      raise ValueError("Canvas shape must match cluster shape")
    sequlet = self.sequlet

    canvas[sequlet != 0] = sequlet[sequlet != 0]

  def __repr__(self) -> str:
    return f"Cluster(shape: {self.shape}, size: {self.size})"

  def can_appendleft(self, chunk: Chunk):
    return chunk.end >= self.min_end and self.max_start >= self.min_end

  def can_append(self, chunk: Chunk):
    return chunk.start <= self.max_start and self.max_start >= self.min_end

  def appendleft(self, chunk: Chunk):
    self.path.appendleft(chunk)
    self.max_start = min(self.max_start, chunk.end)

  def append(self, chunk: Chunk):
    self.path.append(chunk)
    self.min_end = max(self.min_end, chunk.start)