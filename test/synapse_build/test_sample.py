
import pytest

from src.synapse_build.main import sample

def test_sample():
  res = sample()
  assert res == 'Hello World'
