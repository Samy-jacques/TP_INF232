from __future__ import annotations


FONT_LINK: str = (
    '<link rel="preconnect" href="https://fonts.googleapis.com" />'
    '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />'
    '<link href="https://fonts.googleapis.com/css2?'
    'family=DM+Mono:ital,wght@0,300;0,400;0,500;1,400'
    '&family=Syne:wght@400;600;700;800&display=swap" rel="stylesheet" />'
)


TAILWIND_CDN: str = '<script src="https://cdn.tailwindcss.com"></script>'

TAILWIND_CONFIG: str = """
<script>
tailwind.config = {
  theme: {
    extend: {
      fontFamily: {
        sans: ['Syne', 'sans-serif'],
        mono: ['DM Mono', 'monospace'],
      },
      colors: {
        night:  { DEFAULT: '#080c14', 50: '#0d1525', 100: '#111d30' },
        ink:    { DEFAULT: '#141b2d', light: '#1a2340' },
        steel:  { DEFAULT: '#1f2d47', light: '#253354' },
        wire:   { DEFAULT: '#2a3a58' },
        muted:  { DEFAULT: '#4a6080' },
        slate:  { DEFAULT: '#7a90b0' },
        silver: { DEFAULT: '#b8cce0' },
        snow:   { DEFAULT: '#e8f0f8' },
        cyan:   { DEFAULT: '#00d4ff', dim: '#0096bb', glow: 'rgba(0,212,255,0.15)' },
        lime:   { DEFAULT: '#7fff6e', dim: '#4db843' },
        amber:  { DEFAULT: '#ffc947', dim: '#c49600' },
        rose:   { DEFAULT: '#ff5572', dim: '#c02040' },
      },
    }
  }
}
</script>
"""


MAIN_CSS: str = """
<style>
/* ── CSS variables / design tokens ───────────────────────────────────── */
:root {
  --clr-bg:        #080c14;
  --clr-surface:   #141b2d;
  --clr-border:    #1f2d47;
  --clr-border-hi: #2a3a58;
  --clr-muted:     #4a6080;
  --clr-slate:     #7a90b0;
  --clr-silver:    #b8cce0;
  --clr-snow:      #e8f0f8;
  --clr-cyan:      #00d4ff;
  --clr-lime:      #7fff6e;
  --clr-amber:     #ffc947;
  --clr-rose:      #ff5572;
  --glow-cyan:     0 0 30px rgba(0,212,255,0.25);
  --glow-lime:     0 0 20px rgba(127,255,110,0.20);
  --radius-sm:     6px;
  --radius-md:     10px;
  --radius-lg:     14px;
  --font-sans:     'Syne', sans-serif;
  --font-mono:     'DM Mono', monospace;
}

/* ── Reset / base ─────────────────────────────────────────────────────── */
*, *::before, *::after { box-sizing: border-box; }

body {
  margin: 0;
  background: var(--clr-bg);
  font-family: var(--font-sans);
  color: var(--clr-silver);
  min-height: 100vh;
  background-image:
    linear-gradient(rgba(0,212,255,.03) 1px, transparent 1px),
    linear-gradient(90deg, rgba(0,212,255,.03) 1px, transparent 1px);
  background-size: 40px 40px;
}

/* ── Grain overlay ────────────────────────────────────────────────────── */
body::before {
  content: '';
  position: fixed;
  inset: 0;
  pointer-events: none;
  z-index: 100;
  opacity: .025;
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E");
}

/* ── Scrollbar ────────────────────────────────────────────────────────── */
::-webkit-scrollbar            { width:6px; height:6px; }
::-webkit-scrollbar-track      { background:#111d30; }
::-webkit-scrollbar-thumb      { background:#2a3a58; border-radius:3px; }

/* ── Cards ────────────────────────────────────────────────────────────── */
.card {
  background: var(--clr-surface);
  border: 1px solid var(--clr-border);
  border-radius: var(--radius-lg);
  transition: border-color .2s;
}
.card:hover          { border-color: var(--clr-border-hi); }
.card--glow          { box-shadow: var(--glow-cyan); }

/* ── Section labels ───────────────────────────────────────────────────── */
.label {
  font-size: .65rem;
  letter-spacing: .14em;
  text-transform: uppercase;
  color: var(--clr-muted);
  font-weight: 600;
}

/* ── Metric values ────────────────────────────────────────────────────── */
.metric {
  font-family: var(--font-mono);
  font-size: 1.6rem;
  font-weight: 500;
  color: var(--clr-cyan);
  line-height: 1;
}

/* ── Dataset mode tabs ────────────────────────────────────────────────── */
.tab-group { display:flex; gap:2px; background:#141b2d; padding:3px; border-radius:var(--radius-sm); border:1px solid var(--clr-border-hi); }
.tab {
  padding:5px 14px;
  border-radius:var(--radius-sm);
  font-size:.78rem;
  font-weight:600;
  letter-spacing:.05em;
  cursor:pointer;
  border:none;
  color:var(--clr-slate);
  background:transparent;
  transition:all .15s;
  font-family: var(--font-sans);
}
.tab:hover           { color:var(--clr-silver); }
.tab.active          { background:var(--clr-cyan); color:#080c14; }

/* ── Form inputs ──────────────────────────────────────────────────────── */
.input {
  background: #111d30;
  border: 1px solid var(--clr-border);
  border-radius: var(--radius-sm);
  color: var(--clr-silver);
  font-family: var(--font-mono);
  font-size: .83rem;
  padding: 8px 12px;
  width: 100%;
  transition: border-color .15s, box-shadow .15s;
  outline: none;
}
.input:focus {
  border-color: var(--clr-cyan);
  box-shadow: 0 0 0 2px rgba(0,212,255,.15);
}
.input::placeholder { color: var(--clr-muted); }
select.input        { cursor:pointer; appearance:none;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' fill='%234a6080' viewBox='0 0 16 16'%3E%3Cpath d='M7.247 11.14 2.451 5.658C1.885 5.013 2.345 4 3.204 4h9.592a1 1 0 0 1 .753 1.659l-4.796 5.48a1 1 0 0 1-1.506 0z'/%3E%3C/svg%3E");
  background-repeat:no-repeat; background-position:right 10px center;
  padding-right:28px; }
select.input option { background: var(--clr-surface); }

/* ── Buttons ──────────────────────────────────────────────────────────── */
.btn {
  border:none; border-radius:var(--radius-sm); cursor:pointer;
  font-family:var(--font-sans); font-weight:600;
  letter-spacing:.04em; transition:all .15s;
  display:inline-flex; align-items:center; gap:6px;
}
.btn--primary {
  background:var(--clr-cyan); color:#080c14;
  padding:10px 20px; font-size:.85rem;
}
.btn--primary:hover  { background:#22e0ff; box-shadow:var(--glow-cyan); transform:translateY(-1px); }
.btn--primary:active { transform:translateY(0); }
.btn--primary:disabled { opacity:.4; cursor:not-allowed; transform:none; }

.btn--danger {
  background:transparent; color:var(--clr-rose);
  border:1px solid #c02040; padding:7px 14px; font-size:.78rem;
}
.btn--danger:hover   { background:rgba(255,85,114,.1); border-color:var(--clr-rose); }

.btn--ghost {
  background:transparent; color:var(--clr-slate);
  border:1px solid var(--clr-border-hi); padding:7px 14px; font-size:.78rem;
}
.btn--ghost:hover    { color:var(--clr-silver); border-color:var(--clr-muted); }

/* ── Chart containers ─────────────────────────────────────────────────── */
.chart-wrap { position:relative; min-height:260px; }
.chart-wrap--sm { min-height:210px; }

/* ── Regression equation bar ──────────────────────────────────────────── */
.eq-bar {
  display:flex; align-items:center; gap:8px; flex-wrap:wrap;
  background:#0a1220; border:1px solid var(--clr-border);
  border-radius:var(--radius-sm); padding:10px 16px;
  font-family:var(--font-mono); font-size:.78rem;
}
.eq-bar .sep { color:var(--clr-border-hi); margin:0 4px; }

/* ── Data table ───────────────────────────────────────────────────────── */
.dtable { width:100%; border-collapse:collapse; font-family:var(--font-mono); font-size:.74rem; }
.dtable th {
  color:var(--clr-muted); font-weight:500;
  padding:7px 10px; border-bottom:1px solid var(--clr-border); text-align:left;
}
.dtable td { padding:6px 10px; border-bottom:1px solid #0d1525; color:var(--clr-slate); }
.dtable tr:hover td { background:#0d1525; color:var(--clr-silver); }

/* ── Stats mini-card ──────────────────────────────────────────────────── */
.stat-mini {
  background:#0d1525; border:1px solid #1a2340;
  border-radius:var(--radius-sm); padding:10px 12px;
}
.stat-mini .stat-grid {
  display:grid; grid-template-columns:repeat(4,1fr);
  gap:4px; text-align:center; font-family:var(--font-mono); font-size:.72rem;
}
.stat-mini .stat-lbl { color:var(--clr-border-hi); }
.stat-mini .stat-val { color:var(--clr-silver); }

/* ── Toast ────────────────────────────────────────────────────────────── */
#toast {
  position:fixed; bottom:24px; right:24px; z-index:999;
  padding:12px 20px; border-radius:var(--radius-md);
  font-size:.84rem; font-weight:600;
  transform:translateY(80px); opacity:0;
  transition:all .3s cubic-bezier(.34,1.56,.64,1);
  pointer-events:none; font-family:var(--font-sans);
}
#toast.show              { transform:translateY(0); opacity:1; }
#toast.t-success         { background:#0a2a1a; border:1px solid var(--clr-lime);  color:var(--clr-lime); }
#toast.t-error           { background:#2a0a10; border:1px solid var(--clr-rose);  color:var(--clr-rose); }
#toast.t-info            { background:#001a2a; border:1px solid var(--clr-cyan);  color:var(--clr-cyan); }

/* ── Spinner ──────────────────────────────────────────────────────────── */
.spinner {
  width:18px; height:18px;
  border:2px solid rgba(0,212,255,.2);
  border-top-color:var(--clr-cyan);
  border-radius:50%;
  display:inline-block;
  animation:spin .7s linear infinite;
}
@keyframes spin { to { transform:rotate(360deg); } }

/* ── Animations ───────────────────────────────────────────────────────── */
@keyframes fadeUp {
  from { opacity:0; transform:translateY(10px); }
  to   { opacity:1; transform:translateY(0); }
}
.fade-up { animation:fadeUp .4s ease forwards; }

@keyframes pulseGlow {
  0%,100% { box-shadow:0 0 6px  rgba(127,255,110,.3); }
  50%     { box-shadow:0 0 18px rgba(127,255,110,.6); }
}

/* ── Legend dots / lines ──────────────────────────────────────────────── */
.legend { display:flex; gap:16px; flex-wrap:wrap; font-size:.74rem; color:var(--clr-muted); margin-top:10px; }
.legend-dot { width:10px;height:10px;border-radius:50%;display:inline-block;margin-right:5px; }
.legend-line { width:18px;height:2px;display:inline-block;margin-right:5px;vertical-align:middle; }

/* ── Animated gradient text (header accent) ───────────────────────────── */
.header-gradient {
  background: linear-gradient(90deg, #00d4ff 0%, #7fff6e 50%, #ffc947 100%);
  background-size: 200% auto;
  animation: gradientShift 4s linear infinite;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}
@keyframes gradientShift {
  0%   { background-position: 0%   center; }
  100% { background-position: 200% center; }
}

/* ── Pulsing glow badge for user-data count ───────────────────────────── */
.user-badge { animation: pulseGlow 2.5s ease-in-out infinite; }

/* ── Subtle scanline overlay ──────────────────────────────────────────── */
.scanlines::after {
  content: '';
  position: absolute;
  inset: 0;
  pointer-events: none;
  background: repeating-linear-gradient(
    0deg, transparent, transparent 2px,
    rgba(0,0,0,.03) 2px, rgba(0,0,0,.03) 4px
  );
}

/* ── Number counter animation ─────────────────────────────────────────── */
.count-up { animation: countUp .6s ease-out forwards; }
@keyframes countUp {
  from { opacity:0; transform:translateY(10px); }
  to   { opacity:1; transform:translateY(0); }
}
</style>
"""


def head_styles() -> str:
    return "\n".join([FONT_LINK, TAILWIND_CDN, TAILWIND_CONFIG, MAIN_CSS])
