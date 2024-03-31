from typing import List
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    top_mask_percentage_start: float
    top_mask_percentage_end: float
    bottom_mask_percentage_start: float
    application_names: List[str]

    class Config:
        env_file = ".env"
        extra = "allow"


config = Settings()
