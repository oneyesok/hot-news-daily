"""配置模块 — 所有配置项通过环境变量读取，不硬编码任何秘密."""

import os
from dataclasses import dataclass, field


@dataclass
class SmtpConfig:
    server: str = "smtp.qq.com"
    port: int = 465
    sender_email: str = field(
        default_factory=lambda: os.environ.get("SENDER_EMAIL", "")
    )
    password: str = field(
        default_factory=lambda: os.environ.get("SMTP_PASSWORD", "")
    )
    receiver_email: str = field(
        default_factory=lambda: os.environ.get("RECEIVER_EMAIL", "")
    )


@dataclass
class AppConfig:
    smtp: SmtpConfig = field(default_factory=SmtpConfig)


def load_config() -> AppConfig:
    cfg = AppConfig()
    if not cfg.smtp.sender_email or not cfg.smtp.password:
        raise RuntimeError(
            "SENDER_EMAIL 和 SMTP_PASSWORD 环境变量必须设置。"
            "复制 .env.example 为 .env 并填入真实值。"
        )
    return cfg
