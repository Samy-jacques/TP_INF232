from __future__ import annotations
from app.templates import components as c
from app.templates.layout import base_layout


def _left_column() -> str:
    return (
            '<div style="display:flex;flex-direction:column;gap:20px;min-width:0;">'
            + c.scatter_panel()
            + c.charts_row()
            + "</div>"
    )


def _right_column() -> str:
    return (
            '<div style="display:flex;flex-direction:column;gap:18px;min-width:280px;max-width:380px;">'
            + c.submission_form()
            + c.stats_panel()
            + c.user_table()
            + "</div>"
    )


def _main() -> str:
    grid = c.div(
        _left_column() + _right_column(),
        style=(
            "display:flex;gap:24px;flex-wrap:wrap;align-items:flex-start;"
        ),
    )

    inner = c.metric_strip() + grid

    return (
        f'<main style="max-width:1280px;margin:0 auto;padding:32px 24px;">'
        f"{inner}</main>"
    )


def render() -> str:
    body = c.header() + _main() + c.toast()
    return base_layout("California Housing Analytics", body)