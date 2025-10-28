from pydantic import BaseModel, AmqpDsn, RedisDsn, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class RunConfig(BaseModel):
    host: str = "0.0.0.0"
    port: int = 8000
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


class CeleryAppConfig(BaseModel):
    main: str = "ocr"
    rabbitmq_user: str
    rabbitmq_password: str
    rabbitmq_host: str
    rabbitmq_port: int

    redis_host: str
    redis_port: int
    redis_db: int

    worker_concurrency: int = 6
    worker_prefetch_multiplier: int = 0
    result_expires: int = 3600

    @computed_field
    @property
    def broker(self) -> AmqpDsn:
        return AmqpDsn(
            url=f"amqp://{self.rabbitmq_user}:{self.rabbitmq_password}@{self.rabbitmq_host}:{self.rabbitmq_port}//",
        )

    @computed_field
    @property
    def backend(self) -> RedisDsn:
        return RedisDsn(
            url=f"redis://{self.redis_host}:{self.redis_port}/{self.redis_db}"
        )


class RedisConfig(BaseModel):
    host: str
    port: int
    db: int
    decode_responses: bool = True


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(".env.template", ".env"),
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="APP_CONFIG__",
    )
    run: RunConfig = RunConfig()
    celery: CeleryAppConfig
    redis: RedisConfig
    api_router: ApiRouterConfig = ApiRouterConfig()
    v1_router: V1RouterConfig = V1RouterConfig()
    ocr_router: OCRRouterConfig = OCRRouterConfig()
    ocr_image: OCRImageConfig = OCRImageConfig()


settings: Settings = Settings()
