"""Sends the composed digest via Gmail SMTP.

Not exercised by --dry-run runs, and not wired into the GitHub Actions
workflow until the dry-run output has been reviewed and approved -- see
the plan's verification steps.
"""

from __future__ import annotations

import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class EmailConfigError(RuntimeError):
    pass


def send_email(subject: str, html_body: str, text_body: str) -> None:
    address = os.environ.get("GMAIL_ADDRESS")
    app_password = os.environ.get("GMAIL_APP_PASSWORD")
    to_address = os.environ.get("GMAIL_TO")

    missing = [
        name
        for name, value in [
            ("GMAIL_ADDRESS", address),
            ("GMAIL_APP_PASSWORD", app_password),
            ("GMAIL_TO", to_address),
        ]
        if not value
    ]
    if missing:
        raise EmailConfigError(
            f"Missing required environment variable(s): {', '.join(missing)}"
        )

    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = address
    message["To"] = to_address
    message.attach(MIMEText(text_body, "plain"))
    message.attach(MIMEText(html_body, "html"))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(address, app_password)
        server.sendmail(address, [to_address], message.as_string())
