from __future__ import annotations
from app.templates.styles import head_styles
from app.templates.scripts import body_scripts


def base_layout(
        title: str,
        body_content: str,
        *,
        extra_head: str = "",
) -> str:
    head = (
            '<meta charset="UTF-8" />'
            '<meta name="viewport" content="width=device-width, initial-scale=1.0" />'
            f"<title>{title}</title>"
            + head_styles()
            + extra_head
    )

    return (
        "<!DOCTYPE html>"
        '<html lang="en">'
        f"<head>{head}</head>"
        f"<body>{body_content}{body_scripts()}</body>"
        "</html>"
    )