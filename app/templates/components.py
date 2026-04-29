from __future__ import annotations
 
 
def _attrs(**kwargs: str) -> str:
    """Convert keyword arguments to an HTML attribute string."""
    parts = []
    for k, v in kwargs.items():
        key = k.replace("_", "-").rstrip("-")
        parts.append(f'{key}="{v}"')
    return (" " + " ".join(parts)) if parts else ""
 
 
def tag(name: str, content: str = "", cls: str = "", **kwargs) -> str:
    """Wrap content in an HTML tag."""
    attrs = _attrs(**{"class": cls, **kwargs}) if cls else _attrs(**kwargs)
    return f"<{name}{attrs}>{content}</{name}>"
 
 
def div(content: str, cls: str = "", **kwargs) -> str:
    return tag("div", content, cls, **kwargs)
 
 
def p(content: str, cls: str = "", **kwargs) -> str:
    return tag("p", content, cls, **kwargs)
 
 
def span(content: str, cls: str = "", **kwargs) -> str:
    return tag("span", content, cls, **kwargs)
 
 
def h(level: int, content: str, cls: str = "", **kwargs) -> str:
    return tag(f"h{level}", content, cls, **kwargs)
 
 
def icon_bars() -> str:
    return """<svg width="16" height="16" viewBox="0 0 16 16" fill="none">
      <rect x="1" y="8" width="3" height="7" rx="1" fill="#00d4ff"/>
      <rect x="6" y="4" width="3" height="11" rx="1" fill="#00d4ff" opacity="0.7"/>
      <rect x="11" y="1" width="3" height="14" rx="1" fill="#00d4ff" opacity="0.45"/>
      <circle cx="13.5" cy="1.5" r="1.5" fill="#7fff6e"/>
    </svg>"""
 
 
def icon_download() -> str:
    return """<svg width="13" height="13" fill="none" stroke="currentColor"
        stroke-width="2" viewBox="0 0 24 24" style="display:inline-block;vertical-align:middle">
      <path d="M21 15v4a2 2 0 01-2 2H5a2 2 0 01-2-2v-4M7 10l5 5 5-5M12 15V3"/>
    </svg>"""
 
 
def section_label(text: str) -> str:
    return p(text, cls="label")
 
 
def card(content: str, cls: str = "", glow: bool = False, **kwargs) -> str:
    extra = " card--glow" if glow else ""
    return div(content, cls=f"card{extra} {cls}".strip(), **kwargs)
 
 
def mode_tab(label: str, mode: str, active: bool = False) -> str:
    active_cls = " active" if active else ""
    return (
        f'<button class="tab{active_cls}" data-mode="{mode}" '
        f'onclick="setMode(\'{mode}\')">{label}</button>'
    )
 
 
def header() -> str:
    logo = div(
        icon_bars(),
        cls="",
        style=(
            "width:32px;height:32px;border-radius:8px;display:flex;"
            "align-items:center;justify-content:center;"
            "background:linear-gradient(135deg,#00d4ff22,#00d4ff44);"
            "border:1px solid #00d4ff55;"
        ),
    )
    brand = div(
        h(1, "California Housing", cls="", style="color:#e8f0f8;font-weight:700;font-size:.9rem;line-height:1;")
        + p("Analytics Platform", cls="label", style="margin-top:3px;"),
    )
    logo_group = div(
        logo + brand,
        style="display:flex;align-items:center;gap:12px;",
    )
 
    tabs = div(
        mode_tab("Original", "original", active=True)
        + mode_tab("User", "user")
        + mode_tab("Combined", "combined"),
        cls="tab-group",
    )
 
    export_btn = (
        f'<button class="btn btn--ghost" onclick="exportCSV()">'
        f'{icon_download()} Export CSV</button>'
    )
 
    right = div(tabs + export_btn, style="display:flex;align-items:center;gap:12px;")
 
    inner = div(
        logo_group + right,
        style="max-width:1280px;margin:0 auto;padding:16px 24px;"
              "display:flex;align-items:center;justify-content:space-between;",
    )
 
    return (
        f'<header style="border-bottom:1px solid #1f2d47;position:sticky;top:0;'
        f'z-index:50;background:rgba(8,12,20,0.92);backdrop-filter:blur(12px);">'
        f"{inner}</header>"
    )
 
 
def metric_card(label: str, elem_id: str, color: str = "#00d4ff", sub: str = "") -> str:
    value_el = f'<p class="metric" id="{elem_id}" style="color:{color};">—</p>'
    sub_el   = p(sub, style="font-size:.72rem;color:#4a6080;margin-top:4px;") if sub else ""
    return card(
        section_label(label) + value_el + sub_el,
        style="padding:20px 22px;",
    )
 
 
def metric_strip() -> str:
    metrics = [
        metric_card("Total Samples",   "m-total", "#00d4ff", "data points loaded"),
        metric_card("User Points",     "m-user",  "#7fff6e", "submitted by you"),
        metric_card("R² Score",        "m-r2",    "#00d4ff", "goodness of fit"),
        metric_card("MSE",             "m-mse",   "#ffc947", "mean squared error"),
    ]
    return div(
        "".join(metrics),
        style=(
            "display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));"
            "gap:16px;margin-bottom:32px;"
        ),
    )
 
 
FEATURES: list[tuple[str, str]] = [
    ("MedInc",     "Median Income"),
    ("HouseAge",   "House Age"),
    ("AveRooms",   "Avg Rooms"),
    ("AveBedrms",  "Avg Bedrooms"),
    ("Population", "Population"),
    ("AveOccup",   "Avg Occupancy"),
    ("Latitude",   "Latitude"),
    ("Longitude",  "Longitude"),
]
 
 
def feature_select() -> str:
    options = "".join(
        f'<option value="{val}">{lbl}</option>'
        for val, lbl in FEATURES
    )
    return (
        f'<select class="input" id="feature-select" onchange="onFeatureChange()"'
        f' style="width:auto;min-width:150px;">{options}</select>'
    )
 
 
def equation_bar() -> str:
    def mono(elem_id: str, color: str) -> str:
        return f'<span id="{elem_id}" style="color:{color};font-family:\'DM Mono\',monospace;">—</span>'
 
    return div(
        span("ŷ =", style="color:#4a6080;")
        + " " + mono("reg-coef", "#00d4ff")
        + span(" · x + ", style="color:#4a6080;")
        + mono("reg-int", "#00d4ff")
        + span(" | ", cls="sep")
        + span("R²", style="color:#4a6080;")
        + " " + mono("reg-r2", "#7fff6e")
        + span(" MSE", style="color:#4a6080;margin-left:12px;")
        + " " + mono("reg-mse", "#ffc947"),
        cls="eq-bar",
        style="margin-bottom:16px;",
    )
 
 
def scatter_legend() -> str:
    def dot(color: str, label: str) -> str:
        return (
            f'<span style="display:inline-flex;align-items:center;gap:5px;">'
            f'<span class="legend-dot" style="background:{color};"></span>{label}</span>'
        )
 
    def line(color: str, label: str) -> str:
        return (
            f'<span style="display:inline-flex;align-items:center;gap:5px;">'
            f'<span class="legend-line" style="background:{color};"></span>{label}</span>'
        )
 
    return div(
        dot("rgba(0,212,255,0.6)", "Original data")
        + dot("#7fff6e", "User-added")
        + line("#ffc947", "Regression line"),
        cls="legend",
    )
 
 
def scatter_panel() -> str:
    title_row = div(
        div(
            section_label("Regression Analysis")
            + h(2, "Feature → House Value",
                style="color:#e8f0f8;font-weight:700;font-size:1rem;margin-top:4px;"),
            style="flex:1;",
        )
        + div(
            section_label("X Axis") + " " + feature_select(),
            style="display:flex;align-items:center;gap:8px;",
        ),
        style="display:flex;align-items:flex-start;justify-content:space-between;"
              "flex-wrap:wrap;gap:12px;margin-bottom:20px;",
    )
 
    canvas = '<div class="chart-wrap"><canvas id="scatterChart"></canvas></div>'
 
    return card(
        title_row + equation_bar() + canvas + scatter_legend(),
        style="padding:24px;",
    )
 
 
def bar_panel() -> str:
    header_row = (
        section_label("Feature Distribution")
        + h(2, "—", id="bar-title",
            style="color:#e8f0f8;font-weight:600;font-size:.9rem;margin-top:4px;margin-bottom:16px;")
    )
    canvas = '<div class="chart-wrap chart-wrap--sm"><canvas id="barChart"></canvas></div>'
    return card(header_row + canvas, style="padding:22px;")
 
 
def pie_panel() -> str:
    header_row = (
        section_label("Price Categories")
        + h(2, "House Value Segments",
            style="color:#e8f0f8;font-weight:600;font-size:.9rem;margin-top:4px;margin-bottom:16px;")
    )
    canvas = '<div class="chart-wrap chart-wrap--sm"><canvas id="pieChart"></canvas></div>'
    return card(header_row + canvas, style="padding:22px;")
 
 
def charts_row() -> str:
    inner = div(bar_panel(), style="flex:1;") + div(pie_panel(), style="flex:1;")
    return div(inner, style="display:flex;gap:20px;flex-wrap:wrap;")
 
 
def _labelled(label: str, input_html: str, hint: str = "") -> str:
    """Label + input + optional hint text, stacked."""
    hint_el = (
        f'<p style="font-size:.7rem;color:#4a6080;margin-top:3px;">{hint}</p>'
        if hint else ""
    )
    return (
        f'<div style="display:flex;flex-direction:column;gap:4px;">'
        f'<label style="font-size:.7rem;letter-spacing:.1em;text-transform:uppercase;'
        f'color:#4a6080;font-weight:600;">{label}</label>'
        f'{input_html}{hint_el}</div>'
    )
 
 
def _sel(name: str, options: list[tuple[str, str]], placeholder: str = "") -> str:
    """<select> element."""
    opts = (
        f'<option value="" disabled selected>{placeholder}</option>'
        if placeholder else ""
    )
    opts += "".join(f'<option value="{v}">{l}</option>' for v, l in options)
    return f'<select class="input" name="{name}" required>{opts}</select>'
 
 
def _dollar_input(name: str, placeholder: str, min_v: str, max_v: str,
                  step: str = "1000") -> str:
    """Number input with a $ prefix symbol."""
    return (
        '<div style="position:relative;">'
        '<span style="position:absolute;left:10px;top:50%;transform:translateY(-50%);'
        'color:#4a6080;font-family:var(--font-mono);font-size:.82rem;pointer-events:none;">$</span>'
        f'<input class="input" type="number" name="{name}" placeholder="{placeholder}" '
        f'min="{min_v}" max="{max_v}" step="{step}" required style="padding-left:24px;"/>'
        '</div>'
    )
 
 
def _pair(a: str, b: str) -> str:
    return div(a + b, style="display:grid;grid-template-columns:1fr 1fr;gap:10px;")
 
 
_CITIES = [
    ("Anaheim",        "Anaheim"),       ("Bakersfield",    "Bakersfield"),
    ("Fontana",        "Fontana"),       ("Fresno",         "Fresno"),
    ("Irvine",         "Irvine"),        ("Long Beach",     "Long Beach"),
    ("Los Angeles",    "Los Angeles"),   ("Modesto",        "Modesto"),
    ("Moreno Valley",  "Moreno Valley"), ("Oakland",        "Oakland"),
    ("Oxnard",         "Oxnard"),        ("Riverside",      "Riverside"),
    ("Sacramento",     "Sacramento"),    ("San Bernardino", "San Bernardino"),
    ("San Diego",      "San Diego"),     ("San Francisco",  "San Francisco"),
    ("San Jose",       "San Jose"),      ("Santa Ana",      "Santa Ana"),
    ("Santa Rosa",     "Santa Rosa"),    ("Stockton",       "Stockton"),
]
 
_NEIGHBOURHOODS = [
    ("quiet",    "🌳  Quiet street / cute-sac"),
    ("suburban", "🏘️  Typical suburb"),
    ("busy",     "🚦  Busy urban block"),
    ("dense",    "🏙️  Dense city centre"),
]
 
_BEDROOMS = [
    ("0", "Studio"),   ("1", "1 bedroom"), ("2", "2 bedrooms"),
    ("3", "3 bedrooms"), ("4", "4 bedrooms"), ("5", "5 bedrooms"),
    ("6", "6 bedrooms"), ("7", "7 bedrooms"), ("8", "8 bedrooms"),
]
 
_PEOPLE = [(str(i), f"{i} {'person' if i == 1 else 'people'}") for i in range(1, 13)]
 
 
def submission_form() -> str:
    row1 = _pair(
        _labelled("📍  City", _sel("city", _CITIES, "Pick a city…")),
        _labelled("🏙️  Neighbourhood",
                  _sel("neighbourhood", _NEIGHBOURHOODS, "Pick one…")),
    )
    row2 = _pair(
        _labelled("💰  Your annual income",
                  _dollar_input("annual_income_usd", "e.g. 65000", "5000", "500000"),
                  "Household income before tax"),
        _labelled("🏠  Home value",
                  _dollar_input("home_value_usd", "e.g. 450000", "15000", "1500000"),
                  "What the home is worth today"),
    )
    row3 = _pair(
        _labelled("🏗️  Year built",
                  f'<input class="input" type="number" name="year_built" '
                  f'placeholder="e.g. 1985" min="1940" max="2024" step="1" required />',
                  "When was the home built?"),
        _labelled("🛏️  Bedrooms", _sel("bedrooms", _BEDROOMS, "How many?")),
    )
    row4 = _labelled(
        "👥  People living in the home",
        _sel("people_in_home", _PEOPLE, "How many people?"),
    )
 
    buttons = div(
        '<button type="submit" class="btn btn--primary" id="submit-btn" style="flex:1;">'
        'Add My Data Point</button>'
        '<button type="button" class="btn btn--ghost" onclick="fillSample()">Try a sample</button>',
        style="display:flex;gap:8px;padding-top:6px;",
    )
 
    form = (
        '<form id="data-form" onsubmit="submitData(event)"'
        ' style="display:flex;flex-direction:column;gap:12px;">'
        + row1 + row2 + row3 + row4 + buttons
        + "</form>"
    )
 
    return card(
        section_label("Add Data Point")
        + h(2, "Tell us about a home",
            style="color:#e8f0f8;font-weight:700;font-size:1rem;"
                  "margin-top:4px;margin-bottom:18px;")
        + form,
        glow=True,
        style="padding:22px;",
    )
 
 
 
def stats_panel() -> str:
    placeholder = p("Load data to see statistics…", style="color:#4a6080;font-size:.8rem;")
    return card(
        section_label("Feature Statistics")
        + div(placeholder, id="stats-panel", style="margin-top:12px;display:flex;flex-direction:column;gap:8px;"),
        style="padding:20px;",
    )
 
 
def user_table() -> str:
    thead = (
        "<thead><tr>"
        "<th>#</th><th>City</th><th>Income</th><th>Price</th><th>Added</th>"
        "</tr></thead>"
    )
    placeholder = (
        '<tr><td colspan="5" style="text-align:center;color:#4a6080;padding:16px;">'
        "No submissions yet</td></tr>"
    )
    tbody = f'<tbody id="user-tbody">{placeholder}</tbody>'
    table = f'<table class="dtable">{thead}{tbody}</table>'
    scrollable = div(table, style="max-height:220px;overflow-y:auto;")
 
    reset_btn = (
        '<button class="btn btn--danger" onclick="resetData()" '
        'style="font-size:.75rem;padding:6px 12px;">Reset All</button>'
    )
    header_row = div(
        section_label("Your Submissions") + reset_btn,
        style="display:flex;align-items:center;justify-content:space-between;margin-bottom:12px;",
    )
 
    return card(header_row + scrollable, style="padding:20px;")
 
 
def toast() -> str:
    return '<div id="toast"></div>'