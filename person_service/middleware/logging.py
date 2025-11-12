import tempfile
from pathlib import Path


def pick_log_dir(base_dir: Path, env_dir: str) -> Path:
    if env_dir:
        p = Path(env_dir)
        try:
            p.mkdir(parents=True, exist_ok=True)
            return p
        except Exception:
            # если задали, но создать нельзя — падаем в проектный каталог
            pass

    # по умолчанию — ./logs рядом с проектом (работает в CI/Windows)
    p = base_dir / env_dir
    try:
        p.mkdir(parents=True, exist_ok=True)
        return p
    except Exception:
        # крайний вариант — системный tmp
        p = Path(tempfile.gettempdir()) / "service-logs"
        p.mkdir(parents=True, exist_ok=True)
        return p
