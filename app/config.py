import os
from pathlib import Path
from pydantic import BaseModel

class Settings(BaseModel):
    data_dir: Path = Path(os.getenv("BBWW_DATA_DIR", str(Path(__file__).resolve().parents[1] / "data")))
    environment: str = os.getenv("BBWW_ENV", "development")
    api_label: str = "BBWW Commerce Integration Gateway"
    # Local workstation prototype; read docs/SECURITY.md before deploying to shared environments.
    allow_origins: list[str] = ["http://localhost:3000", "http://127.0.0.1:3000"]

settings = Settings()
