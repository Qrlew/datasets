import os.path
import importlib.resources as pkg_resources
from datasets import sources

def test_financial():
    assert os.path.exists('financial', pkg_resources.files(sources) / 'financial' / 'financial.sql')