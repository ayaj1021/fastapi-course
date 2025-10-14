
# from pydantic_settings  import BaseSettings, SettingsConfigDict

# class Settings(BaseSettings):
#     database_hostname: str
#     database_port: int
#     database_password: str
#     database_name: str
#     database_username: str
#     secret_key: str
#     algorithm: str
#     access_token_expire_minutes: int

#     model_config = SettingsConfigDict(env_file=".env")



#     class Config:
#         env_file = '.env'
#         env_file_encoding = "utf-8"


# settings = Settings()


from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class Settings(BaseSettings):
    database_hostname: str = Field(..., env="DATABASE_HOSTNAME")
    database_port: int = Field(..., env="DATABASE_PORT")
    database_password: str = Field(..., env="DATABASE_PASSWORD")
    database_name: str = Field(..., env="DATABASE_NAME")
    database_username: str = Field(..., env="DATABASE_USERNAME")
    secret_key: str = Field(..., env="SECRET_KEY")
    algorithm: str = Field(..., env="ALGORITHM")
    access_token_expire_minutes: int = Field(..., env="ACCESS_TOKEN_EXPIRE_MINUTES")

    # ✅ Pydantic v2 style
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = Settings()
