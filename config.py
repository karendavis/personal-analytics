from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    TOP_MASK_PERCENTAGE_START: float
    TOP_MASK_PERCENTAGE_END: float
    BOTTOM_MASK_PERCENTAGE_START: float

    class Config:
        env_file = ".env"
        extra = "allow"


config = Settings()
