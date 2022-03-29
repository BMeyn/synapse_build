
import pytest

from src.demo.main import sample

def test_sample():
  res = sample()
  assert res == 'Hello World'
