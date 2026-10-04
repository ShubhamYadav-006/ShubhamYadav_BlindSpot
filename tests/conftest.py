import sys
from pathlib import Path
import pytest

# Ensure backend directory is in sys.path for test imports
backend_dir = Path(__file__).resolve().parent.parent / "backend"
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

from app.services.rate_limit import rate_limiter


@pytest.fixture(autouse=True)
def reset_rate_limiter_state():
    """Automatically resets in-memory rate limiter before and after every test."""
    rate_limiter.reset()
    yield
    rate_limiter.reset()
