import pandas as pd
import pytest
from roles_migration.transform import _date, _text

def test_text_normalization():
    assert _text("  admin ")=="admin"
    assert _text("  ") is None

def test_date_parsing():
    assert str(_date("2025-01-01"))=="2025-01-01"
    assert _date("not-a-date") is None
