from pydantic import BaseModel, AmqpDsn, RedisDsn, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class RunConfig(BaseModel):
    host: str
    port: int
    reload: bool = True


class ApiRouterConfig(BaseModel):
    prefix: str = "/api"


class V1RouterConfig(BaseModel):
    prefix: str = "/v1"


class OCRRouterConfig(BaseModel):
    prefix: str = "/ocr"
    tags: list[str] = ["OCR"]
    upload_image_endpoint_path: str = "/upload-image"
    get_task_endpoint_path: str = "/get-task/{task_id}"


class OCRImageConfig(BaseModel):
    max_image_size: int = 1024 * 1024
    allowed_image_content_types: set[str] = {"image/jpeg", "image/png", "image/webp"}


class CustomCeleryTaskStates(BaseModel):
    ACCEPTED: str = "ACCEPTED"


class CeleryAppConfig(BaseModel):
    main: str = "ocr"

    worker_concurrency: int = 6
    worker_prefetch_multiplier: int = 0
    result_expires: int = 3600

    custom_states: CustomCeleryTaskStates = CustomCeleryTaskStates()


class RabbitMQConfig(BaseModel):
    user: str
    password: str
    host: str
    port: int

    @computed_field
    @property
    def url(self) -> AmqpDsn:
        return AmqpDsn(
            url=f"amqp://{self.user}:{self.password}@{self.host}:{self.port}//",
        )


class RedisConfig(BaseModel):
    host: str
    port: int
    backend_db: int
    cache_db: int
    decode_responses: bool = True

    @computed_field
    @property
    def backend_url(self) -> RedisDsn:
        return RedisDsn(url=f"redis://{self.host}:{self.port}/{self.backend_db}")

    @computed_field
    @property
    def cache_url(self) -> RedisDsn:
        return RedisDsn(url=f"redis://{self.host}:{self.port}/{self.cache_db}")


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(".env.template", ".env"),
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="APP_CONFIG__",
    )
    run: RunConfig
    celery: CeleryAppConfig = CeleryAppConfig()
    rabbitmq: RabbitMQConfig
    redis: RedisConfig
    api_router: ApiRouterConfig = ApiRouterConfig()
    v1_router: V1RouterConfig = V1RouterConfig()
    ocr_router: OCRRouterConfig = OCRRouterConfig()
    ocr_image: OCRImageConfig = OCRImageConfig()


settings: Settings = Settings()
