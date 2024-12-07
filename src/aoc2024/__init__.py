import pkgutil
from pathlib import Path

days = [d.name for d in pkgutil.iter_modules([str(p) for p in Path(__file__).parent.iterdir()])]
