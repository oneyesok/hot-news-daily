"""邮件发送模块."""

import logging
import smtplib
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import List

from hot_news_daily.config import SmtpConfig

logger = logging.getLogger(__name__)


def build_content(sections: List[tuple]) -> str:
    """将各来源的标题列表拼接为邮件正文."""
    lines = [
        "📊 今日科技热点",
        f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "",
    ]
    for label, items in sections:
        lines.append(f"=== {label} ===")
        lines.extend(items)
        lines.append("")
    return "\n".join(lines)


def send_email(cfg: SmtpConfig, content: str) -> None:
    """通过 QQ 邮箱 SMTP 发送邮件."""
    msg = MIMEMultipart()
    msg["From"] = cfg.sender_email
    msg["To"] = cfg.receiver_email
    msg["Subject"] = f"📊 今日科技热点 {datetime.now().strftime('%Y-%m-%d %H:%M')}"

    msg.attach(MIMEText(content, "plain", "utf-8"))

    try:
        with smtplib.SMTP_SSL(cfg.server, cfg.port, timeout=30) as server:
            server.login(cfg.sender_email, cfg.password)
            server.sendmail(cfg.sender_email, cfg.receiver_email, msg.as_string())
        logger.info("邮件发送成功 → %s", cfg.receiver_email)
    except smtplib.SMTPException as e:
        logger.error("邮件发送失败: %s", e)
        raise
