import marimo

__generated_with = "0.23.9"
app = marimo.App(width="full")


@app.cell
def _():
    import marimo as mo
    import json
    import re
    import statistics
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    from pathlib import Path
    from scipy import stats
    from sklearn.preprocessing import StandardScaler
    from sklearn.cluster import KMeans
    from sklearn.decomposition import PCA

    BRAND = "#2563eb"
    # Nature-figure palette (nature-skill) for all charts
    CAT_COLORS = {"rising_star": "#E2A52C", "direction_fit": "#8BCF8B",
                  "interesting": "#3775BA", "famous_but_fits": "#767676"}

    # ---- Nature-style mandatory rules: editable SVG text + Arial ----
    plt.rcParams["font.family"] = "sans-serif"
    plt.rcParams["font.sans-serif"] = ["Arial", "Helvetica", "DejaVu Sans"]
    plt.rcParams["svg.fonttype"] = "none"
    plt.rcParams.update({
        "figure.facecolor": "white", "savefig.dpi": 130,
        "axes.facecolor": "#ffffff", "axes.edgecolor": "#9aa6b2", "axes.linewidth": 0.9,
        "axes.grid": True, "grid.color": "#eef2f7", "grid.linewidth": 0.7,
        "axes.titlesize": 11, "axes.titleweight": "bold", "axes.titlecolor": "#0f172a",
        "axes.labelsize": 9, "axes.labelcolor": "#334155",
        "xtick.labelsize": 8, "ytick.labelsize": 8, "xtick.color": "#475569", "ytick.color": "#475569",
        "xtick.major.width": 0.9, "ytick.major.width": 0.9,
        "legend.fontsize": 8, "legend.frameon": False,
        "axes.spines.top": False, "axes.spines.right": False, "font.size": 9,
    })

    def badge(text, color, soft=True):
        if soft:
            return f'<span class="bdg" style="background:{color}1f;color:{color}">{text}</span>'
        return f'<span class="bdg" style="background:{color};color:#fff">{text}</span>'

    def fit_color(v):
        v = float(v) if v is not None else 0
        return "#059669" if v >= 9 else "#10b981" if v >= 8 else "#f59e0b" if v >= 7 else "#ef4444"

    def kpi(icon, num, label, accent):
        return (f'<div class="kpi"><div class="kpi-ico" style="background:{accent}1a;color:{accent}">{icon}</div>'
                f'<div class="kpi-meta"><div class="kpi-num">{num}</div><div class="kpi-lab">{label}</div></div></div>')

    def section(eyebrow, title, sub, anchor=""):
        a = f' id="{anchor}"' if anchor else ""
        return (f'<div class="sec"{a}><div class="eyebrow">{eyebrow}</div>'
                f'<div class="sec-title">{title}</div><div class="sec-sub">{sub}</div></div>')
    return (BRAND, CAT_COLORS, KMeans, PCA, Path, StandardScaler, badge, fit_color, json, kpi, mo, np, pd, plt, re, section, statistics, stats)


@app.cell
def _(mo):
    CSS = """
    <style>
    /*dash-brand-css — polished per ui-ux-pro-max: Data-Dense Dashboard + Bento Grid + Swiss Minimalism*/
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    :root{
      --brand:#2563eb; --brand-d:#1e3a8a; --brand-2:#3b82f6; --accent:#10b981; --amber:#d97706;
      --danger:#dc2626; --ok:#059669;
      --bg:#f6f8fc; --surface:#ffffff; --ink:#0f172a; --muted:#5b6472; --line:#e7ecf3; --ring:#93c5fd;
      --radius-sm:10px; --radius:16px; --radius-lg:22px;
      --shadow-xs:0 1px 3px rgba(15,23,42,.05);
      --shadow-sm:0 2px 10px rgba(15,23,42,.05);
      --shadow:0 6px 24px rgba(15,23,42,.07);
      --shadow-lg:0 18px 50px rgba(30,58,138,.22);
      --sp-1:4px; --sp-2:8px; --sp-3:12px; --sp-4:16px; --sp-5:24px; --sp-6:32px;
      --ease:cubic-bezier(.2,.7,.3,1);
      --font:"Inter",-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,
             "PingFang SC","Microsoft YaHei",sans-serif;
      --font-num:"Inter","SF Mono","Fira Code",ui-monospace,Menlo,Consolas,monospace;
    }
    html,body{background:var(--bg);}
    .dash, .hero, .nav, .kpi, .sec, .card, .pick, .bdg, .panel, .foot, .callout2 {
      font-family:var(--font); box-sizing:border-box; -webkit-font-smoothing:antialiased;
    }
    ::selection{background:#bfdbfe;color:var(--brand-d);}
    ::-webkit-scrollbar{width:10px;height:10px;}
    ::-webkit-scrollbar-track{background:transparent;}
    ::-webkit-scrollbar-thumb{background:#cbd5e1;border-radius:99px;}
    ::-webkit-scrollbar-thumb:hover{background:#94a3b8;}
    a:focus-visible, button:focus-visible, [tabindex]:focus-visible{
      outline:2.5px solid var(--ring); outline-offset:2px; border-radius:6px;
    }
    @media (prefers-reduced-motion: reduce){
      *{animation-duration:.001ms !important; transition-duration:.001ms !important;}
    }
    .kpi-num, .pick-stats b, .hero .pill b{font-family:var(--font-num); font-variant-numeric:tabular-nums; font-feature-settings:"tnum" 1;}

    .hero{
      position:relative; overflow:hidden; border-radius:var(--radius-lg); padding:40px 44px; color:#fff;
      background:radial-gradient(1200px 400px at 90% -20%,rgba(16,185,129,.5),transparent 60%),
                 linear-gradient(135deg,#1e3a8a 0%,#2563eb 52%,#0ea5e9 100%);
      box-shadow:var(--shadow-lg);
    }
    .hero:after{content:"";position:absolute;inset:0;background-image:
      radial-gradient(circle at 1px 1px,rgba(255,255,255,.16) 1px,transparent 0);background-size:22px 22px;opacity:.5;pointer-events:none;}
    .hero h1{font-size:32px;font-weight:800;letter-spacing:-.5px;margin:0;line-height:1.15;position:relative;}
    .hero p{font-size:15px;opacity:.94;margin:var(--sp-2) 0 0;position:relative;line-height:1.6;}
    .hero .pills{display:flex;flex-wrap:wrap;gap:var(--sp-2);margin-top:var(--sp-5);position:relative;}
    .hero .pill{background:rgba(255,255,255,.14);backdrop-filter:blur(8px);border:1px solid rgba(255,255,255,.24);
      border-radius:999px;padding:8px 16px;font-size:13px;font-weight:600;transition:background .18s var(--ease);}
    .hero .pill:hover{background:rgba(255,255,255,.22);}
    .hero .pill b{font-size:17px;}

    .nav{position:sticky;top:0;z-index:50;display:flex;flex-wrap:wrap;gap:6px;align-items:center;margin:var(--sp-4) 0 2px;
      background:rgba(255,255,255,.86);backdrop-filter:blur(12px);border:1px solid var(--line);border-radius:var(--radius-sm);
      padding:8px 12px;box-shadow:var(--shadow-sm);}
    .nav b{color:var(--brand-d);font-weight:800;margin-right:8px;font-size:13px;}
    .nav a{color:var(--muted);text-decoration:none;font-size:13px;font-weight:600;padding:6px 12px;border-radius:9px;
      transition:background .15s var(--ease),color .15s var(--ease);}
    .nav a:hover{background:var(--brand);color:#fff;}

    .kpi-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(168px,1fr));gap:var(--sp-3);margin:var(--sp-4) 0 6px;}
    .kpi{display:flex;gap:13px;align-items:center;background:var(--surface);border:1px solid var(--line);
      border-radius:var(--radius);padding:16px 18px;box-shadow:var(--shadow-xs);transition:transform .18s var(--ease),box-shadow .18s var(--ease);}
    .kpi:hover{transform:translateY(-2px);box-shadow:var(--shadow-sm);}
    .kpi-ico{width:44px;height:44px;border-radius:12px;display:flex;align-items:center;justify-content:center;font-size:20px;flex:none;}
    .kpi-num{font-size:24px;font-weight:800;color:var(--ink);line-height:1;}
    .kpi-lab{font-size:12px;color:var(--muted);margin-top:4px;font-weight:600;}

    .sec{margin:36px 0 6px;}
    .eyebrow{display:inline-block;text-transform:uppercase;letter-spacing:1.4px;font-size:11px;font-weight:800;
      color:var(--brand);background:#2563eb14;padding:4px 10px;border-radius:8px;}
    .sec-title{font-size:23px;font-weight:800;color:var(--ink);margin-top:10px;letter-spacing:-.3px;}
    .sec-sub{font-size:13.5px;color:var(--muted);margin-top:5px;max-width:920px;line-height:1.6;}

    .bdg{padding:3px 10px;border-radius:999px;font-size:12px;font-weight:700;white-space:nowrap;display:inline-block;margin:1px 4px 1px 0;}

    .card{border:1px solid var(--line);border-radius:var(--radius);padding:22px 26px;background:var(--surface);box-shadow:var(--shadow-sm);}
    .card h3{margin:0;font-size:20px;font-weight:800;color:var(--ink);}
    .card .sub{font-size:13.5px;color:var(--muted);margin:4px 0 10px;}
    .ktab{border-collapse:collapse;font-size:13px;line-height:1.6;width:100%;}
    .ktab td{padding:6px 14px 6px 0;vertical-align:top;}
    .ktab td.k{color:var(--muted);font-weight:700;white-space:nowrap;}

    .pick-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(258px,1fr));gap:var(--sp-4);margin-top:var(--sp-2);}
    .pick{position:relative;border:1px solid var(--line);border-radius:var(--radius);padding:18px 20px;background:var(--surface);
      box-shadow:var(--shadow-xs);transition:transform .18s var(--ease),box-shadow .18s var(--ease);overflow:hidden;}
    .pick:before{content:"";position:absolute;left:0;top:0;bottom:0;width:4px;background:linear-gradient(180deg,var(--brand),var(--accent));}
    .pick:hover{transform:translateY(-3px);box-shadow:var(--shadow-sm);}
    .pick-top{display:flex;gap:6px;margin-bottom:8px;}
    .pick-school{font-size:17px;font-weight:800;color:var(--ink);line-height:1.25;}
    .pick-prog{font-size:12px;color:var(--muted);margin:3px 0 12px;min-height:30px;}
    .pick-stats{display:flex;gap:14px;padding:11px 0;border-top:1px solid var(--line);border-bottom:1px solid var(--line);}
    .pick-stats div{text-align:left;} .pick-stats b{font-size:16px;color:var(--ink);display:block;}
    .pick-stats span{font-size:10.5px;color:var(--muted);font-weight:600;}
    .pick-pi{font-size:12px;color:#334155;margin:10px 0 6px;}
    .pick-why{font-size:11.5px;color:var(--muted);line-height:1.55;height:51px;overflow:hidden;}
    .pick-foot{font-size:11px;color:#94a3b8;margin-top:8px;border-top:1px dashed var(--line);padding-top:8px;}

    .panel{background:var(--surface);border:1px solid var(--line);border-radius:var(--radius);padding:8px 6px;box-shadow:var(--shadow-xs);margin-top:8px;}
    .callout2{display:flex;gap:12px;background:#eff6ff;border:1px solid #dbeafe;border-left:4px solid var(--brand);
      border-radius:var(--radius-sm);padding:13px 16px;font-size:13px;color:#1e3a8a;line-height:1.55;margin-top:12px;}

    .foot{margin:40px 0 10px;padding:22px 26px;border-radius:var(--radius);background:linear-gradient(135deg,#0f172a,#1e293b);
      color:#cbd5e1;font-size:12.5px;line-height:1.75;}
    .foot b{color:#fff;}

    /* ── browse rows: aligned table-like list with per-row delete ── */
    .brow{display:grid;align-items:center;gap:10px;padding:8px 14px;font-size:12.5px;line-height:1.3;
      border-top:1px solid var(--line);border-radius:8px;transition:background .12s var(--ease);min-width:0;width:100%;}
    .brow:hover{background:#f2f7ff;}
    .brow-prog{grid-template-columns:38px minmax(210px,2.5fr) 46px 86px minmax(88px,1fr) 74px;}
    .brow-pi{grid-template-columns:minmax(200px,2.4fr) 96px 46px minmax(110px,1.25fr);}
    .brow .rg{font-size:9.5px;font-weight:800;letter-spacing:.2px;padding:3px 0;border-radius:6px;text-align:center;color:#fff;}
    .brow .sc{min-width:0;overflow:hidden;}
    .brow .sc b{color:var(--ink);font-weight:700;}
    .brow .sub2{color:var(--muted);font-size:11px;}
    .brow .oneline{white-space:nowrap;overflow:hidden;text-overflow:ellipsis;}
    .brow .ft{font-weight:800;text-align:center;border-radius:6px;padding:3px 0;color:#fff;
      font-family:var(--font-num);font-variant-numeric:tabular-nums;font-size:11.5px;}
    .brow .st{font-family:var(--font-num);font-variant-numeric:tabular-nums;text-align:right;color:var(--ink);font-weight:600;}
    .brow .ci{color:var(--muted);}
    .brow .ap{color:#9aa6b5;font-size:10.5px;text-align:right;}
    .brow .cat{font-size:10px;font-weight:700;padding:3px 8px;border-radius:999px;text-align:center;}
    .brow .hh{font-family:var(--font-num);font-variant-numeric:tabular-nums;text-align:center;font-weight:700;color:var(--brand-d);}
    .brow .nt{color:var(--amber);font-size:11px;}
    .browhint{font-size:12px;color:var(--muted);margin:2px 0 6px;font-weight:600;}
    .browhint b{color:var(--ink);}
    @media (max-width: 720px){
      .hero{padding:28px 24px;} .hero h1{font-size:26px;}
      .kpi-grid, .pick-grid{grid-template-columns:1fr;}
      .brow-prog{grid-template-columns:34px 1fr 44px 72px;} .brow-prog .ci,.brow-prog .ap{display:none;}
      .brow-pi{grid-template-columns:1fr 80px 40px;} .brow-pi .sc{display:none;}
    }
    </style>
    """
    mo.Html(CSS)
    return


@app.cell
def _(Path, json):
    # Resolve the data directory: prefer CWD, else the dir this notebook lives in.
    _here = Path(__file__).parent if "__file__" in dir() else Path.cwd()
    _cands = [Path.cwd(), _here]
    BASE = next((p for p in _cands if (p / "_research_data.json").exists()), Path.cwd())
    research = json.loads((BASE / "_research_data.json").read_text())
    rows = json.loads((BASE / "_rows.json").read_text())
    try:
        cfg = json.loads((BASE / "_config.json").read_text())
    except Exception:
        cfg = {}
    return BASE, cfg, research, rows


@app.cell
def _(BASE, json):
    # ---- Persistent per-PI notes (survive restarts) ----
    NOTES_PATH = BASE / "_pi_notes.json"

    def load_notes():
        try:
            return json.loads(NOTES_PATH.read_text())
        except Exception:
            return {}

    def write_notes(_d):
        NOTES_PATH.write_text(json.dumps(_d, ensure_ascii=False, indent=1))

    # ---- Persistent "not interested / hidden" lists (PIs + programs) ----
    HIDDEN_PATH = BASE / "_pi_hidden.json"

    def load_hidden():
        try:
            _d = json.loads(HIDDEN_PATH.read_text())
            return {"pis": list(_d.get("pis", [])), "programs": list(_d.get("programs", []))}
        except Exception:
            return {"pis": [], "programs": []}

    def write_hidden(_d):
        HIDDEN_PATH.write_text(json.dumps(_d, ensure_ascii=False, indent=1))
    return load_hidden, load_notes, write_hidden, write_notes


@app.cell
def _(load_hidden, mo, write_hidden):
    # 反应式隐藏状态：点击 ✕ / ↩︎ 即时生效并写盘
    get_hidden, set_hidden = mo.state(load_hidden())

    def _apply(_kind, _name, _add):
        _h = get_hidden()
        _pis = set(_h.get("pis", []))
        _progs = set(_h.get("programs", []))
        _tgt = _pis if _kind == "pis" else _progs
        (_tgt.add if _add else _tgt.discard)(_name)
        _new = {"pis": sorted(_pis), "programs": sorted(_progs)}
        write_hidden(_new)
        set_hidden(_new)

    def hide_pi(_n):
        _apply("pis", _n, True)

    def show_pi(_n):
        _apply("pis", _n, False)

    def hide_prog(_n):
        _apply("programs", _n, True)

    def show_prog(_n):
        _apply("programs", _n, False)
    return get_hidden, hide_pi, hide_prog, show_pi, show_prog


@app.cell
def _(cfg, pd, re, research, rows, statistics):
    _CY = cfg.get("current_year", 2026)
    # Interest-tag taxonomy — generated per research field during intake; falls back to a broad default.
    INTEREST_AREAS = cfg.get("interest_areas") or {
        "Immuno/T-cell": ["immun", "t cell", "t-cell", "lymphocyte", " tcr", "antigen", "cd8", "cd4", "thymus", "cytokine"],
        "StemCell/Dev": ["stem cell", "regenerat", "develop", "organoid", "ipsc", "pluripoten", "differentiat", "lineage", "morphogen", "hematopoiet"],
        "Neuro": ["neuro", "brain", "neuron", "synap", "cortex", "glia", "axon", "behavi"],
        "ML/DL": ["machine learning", "deep learning", "neural net", "foundation model", " ai ", "transformer", "predictive model", "deep-learning", "language model", "ai-"],
        "Cancer": ["cancer", "tumor", "tumour", "oncolog", "leukemia", "glioma", "carcinoma", "metasta", "melanoma"],
        "GeneReg/TF": ["transcription factor", "gene regulat", "regulatory", "chromatin", "enhancer", "epigen", "3d genome", "cis-regul", "gene-regulatory", "atac", "grn"],
        "SingleCell": ["single-cell", "single cell", "scrna", "scatac", "multiome", "spatial transcriptom", "perturb-seq"],
        "Aging": ["aging", "ageing", "senescen", "longevity"],
    }
    # Cost-of-living index by city (US-avg=100) — extend via config for other geographies.
    _COL = cfg.get("col_index") or {
        "new york": 187, "san francisco": 178, "berkeley": 178, "la jolla": 146, "san diego": 146,
        "boston": 162, "cambridge, ma": 162, "pasadena": 150, "los angeles": 150, "seattle": 155,
        "chicago": 119, "evanston": 119, "philadelphia": 108, "pittsburgh": 95, "houston": 96,
        "memphis": 86, "baltimore": 110, "new haven": 120, "princeton": 135, "durham": 102,
        "ithaca": 100, "cold spring harbor": 140, "bar harbor": 105, "farmington": 110}
    _URBAN3 = cfg.get("urban3") or ["new york", "san francisco", "berkeley", "boston", "cambridge, ma", "los angeles", "pasadena",
               "chicago", "seattle", "san diego", "la jolla", "houston", "washington", "philadelphia",
               "berlin", "london", "paris", "stockholm", "hong kong", "zurich", "basel", "singapore", "toronto", "tokyo"]
    _URBAN1 = cfg.get("urban1") or ["princeton", "ithaca", "cold spring harbor", "bar harbor", "farmington", "klosterneuburg", "hinxton"]

    def _col_idx(city):
        c = (city or "").lower()
        for k, v in _COL.items():
            if k in c:
                return v
        return None

    def _urban(city):
        c = (city or "").lower()
        if any(k in c for k in _URBAN1):
            return 1
        if any(k in c for k in _URBAN3):
            return 3
        return 2

    _rbp = {r["program"]: r for r in rows}
    _prog_rec, _pi_rec, _ia_rec = [], [], []
    for _school, _recs in research.items():
        for _rec in _recs:
            _prog = _rec["program"]; _f = _rec.get("facts", {}) or {}; _o = _rec.get("out", {}) or {}
            _pis = (_rec.get("pis", {}) or {}).get("pis", []) or []
            _rr = _rbp.get(_prog, {})
            _usd = _rr.get("usd") if _rr.get("usd") is not None else _f.get("stipendUSD")
            _usd = _usd if isinstance(_usd, (int, float)) else None
            _city = _rr.get("city") or _f.get("city") or ""
            _hs = [p.get("hIndex") for p in _pis if isinstance(p.get("hIndex"), (int, float)) and p.get("hIndex") >= 0]
            _n_ris = sum(1 for p in _pis if p.get("category") == "rising_star")
            _n_dir = sum(1 for p in _pis if p.get("category") == "direction_fit")
            _fitpis = [p for p in _pis if p.get("category") in ("rising_star", "direction_fit")]
            _best = max(_fitpis, key=lambda p: (p.get("hIndex") if isinstance(p.get("hIndex"), (int, float)) and p.get("hIndex") >= 0 else -1), default=None)
            _ia_counts = {}
            for _p in _pis:
                _txt = ((_p.get("research") or "") + " " + (_p.get("whyFit") or "") + " " + (_p.get("rank") or "")).lower()
                _hits = {a for a, kws in INTEREST_AREAS.items() if any(k in _txt for k in kws)}
                for a in _hits:
                    _ia_counts[a] = _ia_counts.get(a, 0) + 1
                _hi = _p.get("hIndex"); _ci = _p.get("citations")
                _m = re.search(r"(20[0-2]\d|19\d\d)", _p.get("startedApprox") or "")
                _pi_rec.append({
                    "region": _rr.get("region") or "", "school": _rr.get("school") or _school, "program": _prog,
                    "name": _p.get("name") or "", "category": _p.get("category") or "", "rank": _p.get("rank") or "",
                    "h_index": (_hi if isinstance(_hi, (int, float)) and _hi >= 0 else None),
                    "citations": (_ci if isinstance(_ci, (int, float)) and _ci >= 0 else None),
                    "scholar_url": _p.get("scholarUrl") or "", "started": _p.get("startedApprox") or "",
                    "years_active": (_CY - int(_m.group(1))) if _m else None, "lab_size": _p.get("labSize") or "",
                    "lab_focus": _p.get("labFocus") or "", "research": _p.get("research") or "", "why_fit": _p.get("whyFit") or "",
                    "recruiting": _p.get("recruiting") or "", "url": _p.get("url") or "", "is_new": bool(_p.get("_new")),
                    "interests": ", ".join(sorted(_hits)),
                })
            _ia_row = {"program": _prog, "school": _rr.get("school") or _school, "region": _rr.get("region") or "",
                       "fit": _rr.get("fit") if _rr.get("fit") is not None else _f.get("fitScore")}
            for a in INTEREST_AREAS:
                _ia_row[a] = _ia_counts.get(a, 0)
            _ia_rec.append(_ia_row)
            _col = _col_idx(_city)
            _prog_rec.append({
                "region": _rr.get("region") or "", "school": _rr.get("school") or _f.get("school") or _school,
                "program": _prog, "city": _city,
                "fit": _rr.get("fit") if _rr.get("fit") is not None else _f.get("fitScore"), "stipend_usd": _usd,
                "meets_floor": bool(_rr.get("floor") if _rr.get("floor") is not None else _f.get("meetsFloor")),
                "col_index": _col, "real_stipend": (round(_usd * 100.0 / _col) if (_usd and _col and _usd >= 0) else None),
                "urban": _urban(_city), "stipend_local": _f.get("stipendLocal") or "", "stipend_basis": _f.get("stipend_basis") or "",
                "stipend_conf": _f.get("stipend_confidence") or "", "stipend_found": _f.get("stipend_foundOfficial", _f.get("stipendFoundOfficial")),
                "stipend_notes": _f.get("stipendNotes") or "", "new_program": bool(_f.get("_newProgram")),
                "apply_rule": _rr.get("multi") or "", "pi_count": len(_pis), "n_rising": _n_ris, "n_dirfit": _n_dir, "n_pifit": _n_ris + _n_dir,
                "median_h": (int(statistics.median(_hs)) if _hs else None), "best_pi": (_best.get("name") if _best else ""),
                "best_pi_h": (_best.get("hIndex") if _best and isinstance(_best.get("hIndex"), (int, float)) and _best.get("hIndex") >= 0 else None),
                "cohort": _f.get("cohortSize") or "", "structure": _f.get("degreeStructure") or "", "route": _f.get("applicationRoute") or "",
                "deadline_tests": _f.get("deadlineAndTests") or "", "app_restrictions": _f.get("applicationRestrictions") or "",
                "focus": _f.get("researchFocus") or "", "systems_empirical": _f.get("systemsEmpiricalBalance") or "", "quant_qual": _f.get("quantQualApproach") or "",
                "fit_rationale": _f.get("fitRationale") or "", "sibling": _f.get("siblingPrograms") or "", "careers": _o.get("careerOutcomes") or "",
                "admit_bg": _o.get("admitBackgrounds") or "", "intl": _o.get("intlNotes") or "",
                "stipend_verified": _o.get("stipendVerified") or _f.get("stipend_whichIsRight") or "",
                "restrictions_verified": _o.get("restrictionsVerified") or "", "extra": _o.get("extraIntel") or "",
                "sources": " | ".join(_f.get("sources") or _f.get("stipend_sources") or []),
            })
    programs_df = pd.DataFrame(_prog_rec)
    pis_df = pd.DataFrame(_pi_rec)
    prog_ia = pd.DataFrame(_ia_rec)
    programs_df["fit"] = pd.to_numeric(programs_df["fit"], errors="coerce")
    programs_df["stipend_usd"] = pd.to_numeric(programs_df["stipend_usd"], errors="coerce")
    programs_df["region_ord"] = programs_df["region"].map(cfg.get("region_order") or {"US": 0, "Europe": 1, "HongKong": 2}).fillna(9)
    pis_df["h_index"] = pd.to_numeric(pis_df["h_index"], errors="coerce")
    pis_df["citations"] = pd.to_numeric(pis_df["citations"], errors="coerce")
    return INTEREST_AREAS, programs_df, pis_df, prog_ia


@app.cell
def _(cfg, programs_df):
    # Region palette / labels / order — works for ANY set of regions the user chose.
    _cfgreg = {r.get("key"): r for r in cfg.get("regions", [])}
    _pal = ["#0F4D92", "#42949E", "#B64342", "#8B5CF6", "#E2A52C", "#3775BA", "#059669", "#D97706"]
    _keys = sorted(set(programs_df.region.tolist()), key=lambda k: (_cfgreg.get(k, {}).get("order", 99), str(k)))
    REGION_COLORS, REGION_LABEL = {}, {}
    for _i, _k in enumerate(_keys):
        REGION_COLORS[_k] = _cfgreg.get(_k, {}).get("color") or _pal[_i % len(_pal)]
        REGION_LABEL[_k] = _cfgreg.get(_k, {}).get("short") or _cfgreg.get(_k, {}).get("label") or _k
    REGIONS_PRESENT = _keys
    FLOOR = int(cfg.get("stipend_floor", 35000))
    return FLOOR, REGION_COLORS, REGION_LABEL, REGIONS_PRESENT


@app.cell
def _(REGIONS_PRESENT, REGION_LABEL, cfg, mo, pis_df, programs_df):
    _n = len(programs_df)
    _title = cfg.get("title") or "PhD Application Planner — 项目 &amp; 导师决策仪表盘"
    _sub = cfg.get("subtitle") or "powered by marimo · 交互式 PhD 申请决策仪表盘 · 数据已逐项核验"
    _rp = " · ".join(f"<b>{int((programs_df.region == _k).sum())}</b> {REGION_LABEL.get(_k, _k)}" for _k in REGIONS_PRESENT)
    _hero = f"""
    <div class="hero">
      <h1>{_title}</h1>
      <p>{_sub}</p>
      <div class="pills">
        <div class="pill"><b>{_n}</b> 个项目</div>
        <div class="pill">{_rp}</div>
        <div class="pill"><b>{len(pis_df)}</b> 位目标 PI</div>
        <div class="pill"><b>{int(pis_df.h_index.notna().sum())}</b> 含 h-index</div>
        <div class="pill">stipend ✓ 已核验</div>
      </div>
    </div>
    <div class="nav"><b>PhD Application Planner</b>
      <a href="#picks">⭐ 精选</a><a href="#programs">🔎 项目</a><a href="#faculty">🔬 导师</a>
      <a href="#analysis">📊 分析</a><a href="#priority">🎯 优先级</a>
    </div>
    """
    mo.Html(_hero)
    return


@app.cell
def _(kpi, mo, pis_df, programs_df):
    _n = len(programs_df); _floor = int(programs_df.meets_floor.sum())
    _ris = int(programs_df.n_rising.sum()); _medh = int(pis_df.h_index.median()) if pis_df.h_index.notna().any() else 0
    _grid = '<div class="kpi-grid">' + "".join([
        kpi("🎓", _n, "PhD 项目", "#2563eb"),
        kpi("💵", f"{_floor}/{_n}", "过 $35k 线", "#10b981"),
        kpi("🔬", len(pis_df), "目标 PI", "#3b82f6"),
        kpi("⭐", _ris, "rising-star PI", "#f59e0b"),
        kpi("📈", _medh, "PI 中位 h-index", "#8b5cf6"),
    ]) + "</div>"
    mo.Html(_grid)
    return


@app.cell
def _(REGION_COLORS, badge, fit_color, mo, pd, programs_df):
    _top = programs_df.sort_values(["fit", "stipend_usd"], ascending=[False, False]).head(6)
    _rc = REGION_COLORS

    def _pick(r):
        _st = f"${int(r.stipend_usd):,}" if pd.notna(r.stipend_usd) and r.stipend_usd >= 0 else "—"
        _bh = f" · h{int(r.best_pi_h)}" if pd.notna(r.best_pi_h) else ""
        return f"""<div class="pick">
          <div class="pick-top">{badge(r.region, _rc.get(r.region,'#777'), False)}{badge(f'Fit {r.fit}', fit_color(r.fit), False)}</div>
          <div class="pick-school">{r.school}</div>
          <div class="pick-prog">{r.program[:58]}</div>
          <div class="pick-stats">
            <div><b>{_st}</b><span>stipend / yr</span></div>
            <div><b>{int(r.pi_count)}</b><span>target PIs</span></div>
            <div><b>{int(r.n_rising)}</b><span>⭐ rising</span></div>
          </div>
          <div class="pick-pi">🎯 最佳契合：<b>{r.best_pi or '—'}</b>{_bh}</div>
          <div class="pick-why">{(r.fit_rationale or '')[:130]}…</div>
          <div class="pick-foot">📍 {r.city} · {r.apply_rule or ''}</div>
        </div>"""
    _html = ('<div class="sec" id="picks"><div class="eyebrow">Top Picks</div>'
             '<div class="sec-title">⭐ 为你精选 · 契合度最高的 6 个</div>'
             '<div class="sec-sub">按 fit 分（同分看 stipend）。卡片含最佳契合 PI 及其 h-index、stipend、rising-star 数、城市与申请限制。</div></div>'
             '<div class="pick-grid">' + "".join(_pick(r) for r in _top.itertuples()) + "</div>")
    mo.Html(_html)
    return


@app.cell
def _(mo, section):
    mo.Html(section("Explore", "🔎 项目浏览", "按地区 / fit / stipend / 申请灵活度筛选。「COL调整后」= 按所在都市生活成本折算的真实购买力（仅美国）。", "programs"))
    return


@app.cell
def _(mo, programs_df):
    _regs = sorted(programs_df.region.unique().tolist())
    region_filter = mo.ui.multiselect(options=_regs, value=_regs, label="地区")
    fit_slider = mo.ui.slider(0, 10, value=0, step=0.5, label="最低 Fit", show_value=True)
    stipend_slider = mo.ui.slider(0, 80000, value=0, step=1000, label="最低 Stipend (USD/yr)", show_value=True)
    floor_cb = mo.ui.checkbox(value=False, label="只看过 $35k 线")
    multi_cb = mo.ui.checkbox(value=False, label="只看可多投")
    mo.vstack([mo.hstack([region_filter, fit_slider, stipend_slider], justify="start", gap=2),
               mo.hstack([floor_cb, multi_cb], justify="start", gap=2)])
    return fit_slider, floor_cb, multi_cb, region_filter, stipend_slider


@app.cell
def _(fit_slider, floor_cb, get_hidden, multi_cb, programs_df, region_filter, stipend_slider):
    _df = programs_df[programs_df.region.isin(region_filter.value)].copy()
    _df = _df[_df.fit.fillna(0) >= fit_slider.value]
    _df = _df[_df.stipend_usd.fillna(0) >= stipend_slider.value]
    if floor_cb.value:
        _df = _df[_df.meets_floor]
    if multi_cb.value:
        _df = _df[_df.apply_rule.str.contains("multi", case=False, na=False)]
    _df = _df[~_df.program.isin(set(get_hidden().get("programs", [])))]  # 排除已隐藏
    prog_filtered = _df.sort_values(["region_ord", "fit"], ascending=[True, False])
    return (prog_filtered,)


@app.cell
def _(REGION_COLORS, REGION_LABEL, fit_color, hide_prog, mo, prog_filtered):
    # 逐行 ✕ 直删：对齐的表格式行，点那一行的 ✕ 立即隐藏
    _RC = REGION_COLORS
    _RL = REGION_LABEL

    def _esc(_s):
        return (str(_s) if _s is not None else "").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

    _rows = []
    for _r in prog_filtered.itertuples():
        _btn = mo.ui.button(label="✕", on_click=lambda _v, _p=_r.program: hide_prog(_p))
        _su = f"${int(_r.stipend_usd):,}" if isinstance(_r.stipend_usd, (int, float)) and _r.stipend_usd == _r.stipend_usd and _r.stipend_usd > 0 else "$—"
        _fc = fit_color(_r.fit)
        _rgc = _RC.get(_r.region, "#767676")
        _html = (
            f'<div class="brow brow-prog">'
            f'<span class="rg" style="background:{_rgc}">{_esc(_RL.get(_r.region, _r.region))}</span>'
            f'<span class="sc oneline"><b>{_esc(_r.school)}</b> <span class="sub2">— {_esc(_r.program)}</span></span>'
            f'<span class="ft" style="background:{_fc}">{_r.fit}</span>'
            f'<span class="st">{_su}</span>'
            f'<span class="ci oneline">{_esc(_r.city)}</span>'
            f'<span class="ap oneline">{_esc(_r.apply_rule or "")}</span>'
            f'</div>'
        )
        _rows.append(mo.hstack([_btn, mo.Html(_html)], justify="start", gap=0.5, align="center", widths=[0.04, 1]))
    _hdr = mo.Html(f'<div class="browhint">共 <b>{len(prog_filtered)}</b> 个项目 · 点每行最左的 <b>✕</b> 直接隐藏（可在下方恢复）</div>')
    mo.vstack([_hdr] + _rows, gap=0.15)
    return


@app.cell
def _(get_hidden, mo, show_prog):
    # 已隐藏的项目 —— 点 ↩︎ 一键恢复
    _hid = sorted(get_hidden().get("programs", []))
    if not _hid:
        _panel = mo.md("✅ 还没有隐藏任何项目。在上面的列表里点某行的 **✕** 即可隐藏（持久保存，关掉再开还在）。")
    else:
        _rows = []
        for _p in _hid:
            _b = mo.ui.button(label="↩︎ 恢复", on_click=lambda _v, _x=_p: show_prog(_x))
            _rows.append(mo.hstack([_b, mo.md(_p)], justify="start", gap=0.75, align="center"))
        _panel = mo.vstack([mo.md(f"### 🚫 已隐藏的项目（{len(_hid)}）— 点 ↩︎ 恢复")] + _rows, gap=0.2)
    mo.callout(_panel, kind="info")
    return


@app.cell
def _(mo, programs_df):
    _pf = programs_df.sort_values(["region_ord", "fit"], ascending=[True, False])
    _opts = {f"[{r.region}] {r.school} — {r.program[:48]}  (fit {r.fit})": r.program for r in _pf.itertuples()}
    program_picker = mo.ui.dropdown(options=_opts, value=list(_opts.keys())[0], label="选项目看详情卡")
    mo.vstack([mo.md("### 🏫 项目详情卡"), program_picker])
    return (program_picker,)


@app.cell
def _(REGION_COLORS, badge, fit_color, mo, pd, pis_df, programs_df, program_picker):
    _r = programs_df[programs_df.program == program_picker.value].iloc[0]
    _usd = int(_r.stipend_usd) if pd.notna(_r.stipend_usd) and _r.stipend_usd >= 0 else None
    _rc = REGION_COLORS.get(_r.region, "#777")
    _b = (badge(f"Fit {_r.fit}/10", fit_color(_r.fit), False)
          + badge(f"${_usd:,}/yr" if _usd else "stipend 未核实", "#10b981" if _r.meets_floor else "#ef4444", False)
          + (badge(f"COL调整 ${int(_r.real_stipend):,}", "#8b5cf6") if pd.notna(_r.real_stipend) else "")
          + badge(_r.region, _rc) + badge(_r.apply_rule or "—", "#64748b")
          + badge(f"{int(_r.pi_count)} PIs · ⭐{int(_r.n_rising)}", "#3b82f6"))
    _found = {True: "官方✓", False: "⚠️非官方", None: "—"}.get(_r.stipend_found, "—")

    def _rw(lbl, val):
        return f'<tr><td class="k">{lbl}</td><td>{val}</td></tr>' if str(val).strip() else ""
    _card = f"""<div class="card">
      <h3>{_r.school}</h3><div class="sub">{_r.program} · {_r.city}</div>
      <div style="margin:4px 0 14px">{_b}</div>
      <table class="ktab">
        {_rw("Stipend", _r.stipend_local)}
        {_rw("Stipend 核实", f"来源 {_found} · 置信度 {_r.stipend_conf or '—'} · {_r.stipend_basis or ''}")}
        {_rw("申请路径", _r.route)}{_rw("Cohort/录取", _r.cohort)}
        {_rw("⚠️ 申请限制", _r.app_restrictions)}{_rw("截止/考试", _r.deadline_tests)}
        {_rw("研究方向", _r.focus)}{_rw("系统/实证", _r.systems_empirical)}{_rw("量化 vs 质化", _r.quant_qual)}
        {_rw("同校其他可投", _r.sibling)}{_rw("Fit 理由", _r.fit_rationale)}
        {_rw("出路", _r.careers)}{_rw("录取背景", _r.admit_bg)}{_rw("国际生", _r.intl)}{_rw("其他情报", _r.extra)}
      </table></div>"""
    _pdf = pis_df[pis_df.program == program_picker.value].copy().sort_values("h_index", ascending=False, na_position="last")
    _pidisp = _pdf[["name", "category", "h_index", "citations", "interests", "rank", "lab_size", "lab_focus", "why_fit", "url"]]
    mo.vstack([mo.Html(_card), mo.md("##### 🎯 目标 PI（按 h-index 降序）"), mo.ui.table(_pidisp, page_size=12, selection=None)])
    return


@app.cell
def _(mo, section):
    mo.Html(section("Faculty", "🔬 PI 浏览器", "全部目标 PI，可按类型 / 系统-实证 / 地区 / 最低 h-index / 关键词检索；含自动兴趣标签、建组年数、Scholar 链接。", "faculty"))
    return


@app.cell
def _(mo, pis_df):
    _cats = sorted(pis_df.category.unique().tolist())
    _focuses = sorted(pis_df.lab_focus.unique().tolist())
    _regs = sorted(pis_df.region.unique().tolist())
    _hmax = int(pis_df.h_index.max()) if pis_df.h_index.notna().any() else 100
    pi_cat = mo.ui.multiselect(options=_cats, value=_cats, label="类型")
    pi_wd = mo.ui.multiselect(options=_focuses, value=_focuses, label="系统/实证")
    pi_reg = mo.ui.multiselect(options=_regs, value=_regs, label="地区")
    pi_minh = mo.ui.slider(0, _hmax, value=0, step=5, label="最低 h-index", show_value=True)
    pi_search = mo.ui.text(placeholder="'trust calibration' / 'teleoperation' / 'shared autonomy' …", label="搜索", full_width=True)
    mo.vstack([mo.hstack([pi_cat, pi_wd, pi_reg, pi_minh], justify="start", gap=2),
               mo.hstack([pi_search], justify="start", gap=2)])
    return pi_cat, pi_minh, pi_reg, pi_search, pi_wd


@app.cell
def _(get_hidden, pi_cat, pi_minh, pi_reg, pi_search, pi_wd, pis_df):
    _df = pis_df[pis_df.category.isin(pi_cat.value)].copy()
    _df = _df[_df.lab_focus.isin(pi_wd.value)]
    _df = _df[_df.region.isin(pi_reg.value)]
    if pi_minh.value > 0:
        _df = _df[_df.h_index.fillna(-1) >= pi_minh.value]
    _q = (pi_search.value or "").strip().lower()
    if _q:
        _df = _df[_df.name.str.lower().str.contains(_q, na=False) | _df.why_fit.str.lower().str.contains(_q, na=False)
                  | _df.research.str.lower().str.contains(_q, na=False) | _df.interests.str.lower().str.contains(_q, na=False)]
    _df = _df[~_df.name.isin(set(get_hidden().get("pis", [])))]  # 排除已隐藏
    pi_filtered = _df.sort_values("h_index", ascending=False, na_position="last")
    return (pi_filtered,)


@app.cell
def _(hide_pi, load_notes, mo, note_save, pi_filtered):
    # 逐行 ✕ 直删：对齐的表格式行，点那一行的 ✕ 立即隐藏
    _CAP = 50
    note_save  # 备注变化后刷新行内 📝
    _CATC = {"rising_star": "#E2A52C", "direction_fit": "#8BCF8B",
             "interesting": "#3775BA", "famous_but_fits": "#767676"}
    _CATL = {"rising_star": "新星", "direction_fit": "方向契合",
             "interesting": "新方法", "famous_but_fits": "名家"}

    def _esc(_s):
        return (str(_s) if _s is not None else "").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

    _notes = load_notes()
    _rows = []
    for _r in pi_filtered.head(_CAP).itertuples():
        _btn = mo.ui.button(label="✕", on_click=lambda _v, _n=_r.name: hide_pi(_n))
        _hh = _r.h_index
        _ht = f"{int(_hh)}" if isinstance(_hh, (int, float)) and _hh == _hh and _hh >= 0 else "—"
        _sl = f' <a href="{_r.scholar_url}" target="_blank" style="text-decoration:none">📖</a>' if isinstance(_r.scholar_url, str) and _r.scholar_url else ""
        _nt = f' <span class="nt">📝 {_esc(_notes[_r.name][:30])}</span>' if _notes.get(_r.name) else ""
        _cbg = _CATC.get(_r.category, "#767676")
        _html = (
            f'<div class="brow brow-pi">'
            f'<span class="sc oneline"><b>{_esc(_r.name)}</b>{_sl} <span class="sub2">{_esc((_r.interests or "")[:52])}</span>{_nt}</span>'
            f'<span class="cat" style="background:{_cbg}1f;color:{_cbg}">{_esc(_CATL.get(_r.category, _r.category))}</span>'
            f'<span class="hh">{_ht}</span>'
            f'<span class="sc oneline"><span class="sub2">{_esc(_r.school)}</span></span>'
            f'</div>'
        )
        _rows.append(mo.hstack([_btn, mo.Html(_html)], justify="start", gap=0.5, align="center", widths=[0.04, 1]))
    _more = "" if len(pi_filtered) <= _CAP else f" · 显示前 {_CAP}（用上方筛选/搜索缩小）"
    _hdr = mo.Html(f'<div class="browhint">共 <b>{len(pi_filtered)}</b> 位 PI · 点每行最左的 <b>✕</b> 直接隐藏{_more}</div>')
    mo.vstack([_hdr] + _rows, gap=0.15)
    return


@app.cell
def _(mo, pis_df):
    # 选哪位老师写备注 + 保存按钮
    _names = sorted(pis_df.name.dropna().astype(str).unique().tolist())
    note_pi = mo.ui.dropdown(options=_names, value=(_names[0] if _names else None),
                             label="选老师", searchable=True, full_width=True)
    note_save = mo.ui.run_button(label="💾 保存备注", kind="success")
    return note_pi, note_save


@app.cell
def _(load_notes, mo, note_pi):
    # 文本框预填该老师已存的备注；切换老师时自动重载
    _existing = load_notes().get(note_pi.value, "") if note_pi.value else ""
    note_editor = mo.ui.text_area(
        value=_existing, label="", full_width=True, rows=7,
        placeholder="meet 完随手记：研究方向印象 / 是否在招 / 聊了什么 / 好感度 / 下一步…",
    )
    return (note_editor,)


@app.cell
def _(load_notes, mo, note_editor, note_pi, note_save):
    _all = load_notes()
    _done = "、".join(sorted(_all.keys())) if _all else "（还没有备注）"
    note_save  # 保存后刷新“已记录”清单
    mo.callout(
        mo.vstack([
            mo.md("### ✍️ 我的导师备注 — meet 完随手记（自动存到本地，关掉再打开还在）"),
            mo.md("**用法**：选老师 → 写/改备注 → 点 **保存**。切换老师会载入该老师已存的备注；改完务必点保存再切。"),
            note_pi,
            note_editor,
            note_save,
            mo.md(f"**已记录（{len(load_notes())} 位）：** {_done}"),
        ], gap=0.5),
        kind="warn",
    )
    return


@app.cell
def _(load_notes, mo, note_editor, note_pi, note_save, write_notes):
    # 仅在点击“保存”时写盘
    mo.stop(not note_save.value)
    _d = load_notes()
    _name = note_pi.value
    _txt = (note_editor.value or "").strip()
    if _name:
        if _txt:
            _d[_name] = _txt
        else:
            _d.pop(_name, None)
        write_notes(_d)
    mo.callout(mo.md(f"✅ 已保存 **{_name}** 的备注（共 {len(_d)} 位老师有备注）"), kind="success")
    return


@app.cell
def _(get_hidden, mo, show_pi):
    # 已隐藏的老师 —— 点 ↩︎ 一键恢复
    _hid = sorted(get_hidden().get("pis", []))
    if not _hid:
        _panel = mo.md("✅ 还没有隐藏任何老师。在上面的列表里点某行的 **✕** 即可隐藏（持久保存，关掉再开还在）。")
    else:
        _rows = []
        for _n in _hid:
            _b = mo.ui.button(label="↩︎ 恢复", on_click=lambda _v, _x=_n: show_pi(_x))
            _rows.append(mo.hstack([_b, mo.md(_n)], justify="start", gap=0.75, align="center"))
        _panel = mo.vstack([mo.md(f"### 🚫 已隐藏的老师（{len(_hid)}）— 点 ↩︎ 恢复")] + _rows, gap=0.2)
    mo.callout(_panel, kind="info")
    return


@app.cell
def _(mo, section):
    mo.Html(section("Deep Analysis", "📊 深度分析", "申请优先级排序器 · 真实购买力 · PI 影响力地形 · 兴趣覆盖热图 · 概览。", "analysis"))
    return


@app.cell
def _(mo, section):
    mo.Html(section("Strategy", "🎯 交互式申请优先级排序器", "拖动 5 个权重 + 勾选你最看重的兴趣方向 → 排名实时更新。优先级 = 加权(契合度·stipend·城市·rising/契合 PI 密度·兴趣覆盖)，0–100。", "priority"))
    return


@app.cell
def _(INTEREST_AREAS, mo):
    w_fit = mo.ui.slider(0, 100, value=40, step=5, label="① 契合度", show_value=True)
    w_stip = mo.ui.slider(0, 100, value=20, step=5, label="② Stipend", show_value=True)
    w_city = mo.ui.slider(0, 100, value=15, step=5, label="③ 城市", show_value=True)
    w_pi = mo.ui.slider(0, 100, value=15, step=5, label="④ rising/契合 PI 密度", show_value=True)
    w_int = mo.ui.slider(0, 100, value=10, step=5, label="⑤ 兴趣覆盖", show_value=True)
    pri_interests = mo.ui.multiselect(options=list(INTEREST_AREAS.keys()),
                                      value=["Immuno/T-cell", "StemCell/Dev", "GeneReg/TF", "ML/DL", "Neuro"], label="你看重的兴趣方向")
    pri_floor = mo.ui.checkbox(value=True, label="排除低于 $35k 的项目")
    mo.vstack([mo.hstack([w_fit, w_stip, w_city], justify="start", gap=2),
               mo.hstack([w_pi, w_int, pri_floor], justify="start", gap=2), pri_interests])
    return pri_floor, pri_interests, w_city, w_fit, w_int, w_pi, w_stip


@app.cell
def _(FLOOR, REGION_COLORS, mo, plt, pri_floor, pri_interests, prog_ia, programs_df, w_city, w_fit, w_int, w_pi, w_stip):
    _d = programs_df.copy()
    if pri_floor.value:
        _d = _d[_d.meets_floor]
    _ia = prog_ia.set_index("program")
    _sel = list(pri_interests.value) or list(prog_ia.columns[4:])
    _d["intscore"] = _d.program.map(_ia[_sel].sum(axis=1)).fillna(0)
    _ws = max(1e-9, w_fit.value + w_stip.value + w_city.value + w_pi.value + w_int.value)
    _fitn = (_d.fit.fillna(0) / 10).clip(0, 1)
    _stipn = ((_d.stipend_usd.fillna(0) - FLOOR) / 25000).clip(0, 1).where(_d.meets_floor, 0)
    _cityn = (_d.urban / 3).clip(0, 1)
    _pin = (_d.n_pifit / 8).clip(0, 1)
    _intn = (_d.intscore / max(1, _d.intscore.max())).clip(0, 1)
    _d["priority"] = (100 * (w_fit.value * _fitn + w_stip.value * _stipn + w_city.value * _cityn + w_pi.value * _pin + w_int.value * _intn) / _ws).round(1)
    _d = _d.sort_values("priority", ascending=False)
    _top = _d.head(18)
    _fig, _ax = plt.subplots(figsize=(9.5, 7))
    _y = list(range(len(_top)))[::-1]
    _ax.barh(_y, _top.priority, color=[REGION_COLORS.get(r, "#888") for r in _top.region], height=0.72)
    for _i, (_, _row) in enumerate(_top.iterrows()):
        _ax.text(_row.priority + 0.7, len(_top) - 1 - _i, f"{_row.priority:.0f}", va="center", fontsize=7.5, color="#475569", fontweight="bold")
    _ax.set_yticks(_y); _ax.set_yticklabels([f"{s[:20]} — {p[:24]}" for s, p in zip(_top.school, _top.program)], fontsize=7)
    _ax.set_xlabel("Composite application-priority score (0–100, weighted by your sliders)")
    _ax.set_title("Top-18 programs by YOUR weighted priority — colour = region", fontsize=11); _ax.set_xlim(0, 102)
    _fig.tight_layout()
    _tbl = _d.head(20)[["region", "school", "program", "fit", "stipend_usd", "urban", "n_rising", "n_dirfit", "intscore", "best_pi", "best_pi_h", "apply_rule", "priority"]].rename(
        columns={"stipend_usd": "$USD", "urban": "城市(1-3)", "n_rising": "#⭐", "n_dirfit": "#🎯", "intscore": "兴趣PI", "best_pi": "最佳契合PI", "best_pi_h": "其h", "apply_rule": "可多投?", "priority": "优先级"})
    mo.vstack([_fig, mo.md("**优先级前 20（可点列头再排序）**"), mo.ui.table(_tbl, page_size=20, selection=None)])
    return


@app.cell
def _(mo, section):
    mo.Html(section("Real Pay", "💰 生活成本调整后的真实 Stipend", "名义高 ≠ 真实购买力高。深色条 = 按所在都市生活成本指数（均值=100）折算后的真实 stipend（仅对有 COL 数据的城市）。"))
    return


@app.cell
def _(FLOOR, REGION_COLORS, mo, plt, programs_df):
    _d = programs_df[programs_df.real_stipend.notna()].copy().sort_values("real_stipend")
    if len(_d) == 0:
        mo.md("（暂无城市生活成本（COL）数据，跳过真实购买力图；可在 `_config.json` 的 `col_index` 补充城市指数。）")
    else:
        _fig, _ax = plt.subplots(figsize=(9.5, max(3.5, 0.32 * len(_d))))
        _y = range(len(_d))
        _ax.barh(_y, _d.stipend_usd, color="#dbe6f5", label="Nominal stipend (USD/yr)")
        _ax.barh(_y, _d.real_stipend, color=[REGION_COLORS.get(_r, "#0F4D92") for _r in _d.region], height=0.55, label="Cost-of-living adjusted (COL avg=100)")
        _ax.set_yticks(list(_y)); _ax.set_yticklabels([f"{s[:18]} ({str(c).split(',')[0][:12]})" for s, c in zip(_d.school, _d.city)], fontsize=6.5)
        _ax.axvline(FLOOR, color="#ef4444", linestyle="--", linewidth=1)
        _ax.set_xlabel("Annual stipend (USD/yr) — light = nominal, dark = cost-of-living adjusted")
        _ax.set_title("Real vs nominal PhD stipend (programs with COL data)", fontsize=11)
        _ax.legend(loc="lower right"); _fig.tight_layout()
        _hi = _d.nlargest(3, "real_stipend"); _lo = _d.nsmallest(3, "real_stipend")
        mo.vstack([_fig, mo.Html('<div class="callout2"><div>💡</div><div><b>真实购买力最高：</b> '
            + " · ".join(f"{r.school} (${int(r.real_stipend):,})" for _, r in _hi.iterrows())
            + "　｜　<b>最低：</b> " + " · ".join(f"{r.school} (${int(r.real_stipend):,})" for _, r in _lo.iterrows())
            + "。名义 stipend 高 ≠ 真实购买力高：高消费都市会被 COL 拉低，低消费地区可能反超。</div></div>")])
    return


@app.cell
def _(mo, section):
    mo.Html(section("Talent", "🧪 PI 质量地形：建组年限 vs 影响力", "横轴=独立建组年数（越左越年轻），纵轴=h-index。左下=新晋 rising star，右上=资深。你偏好年轻/中小组 → 重点看左侧高亮带。"))
    return


@app.cell
def _(CAT_COLORS, mo, pis_df, plt):
    _d = pis_df.dropna(subset=["h_index", "years_active"])
    _d = _d[(_d.years_active >= 0) & (_d.years_active <= 40)]
    _fig, _ax = plt.subplots(figsize=(9.5, 6))
    _ax.axvspan(0, 7, color="#f59e0b", alpha=0.08)
    for _c, _g in _d.groupby("category"):
        _ax.scatter(_g.years_active, _g.h_index, s=36, alpha=0.74, color=CAT_COLORS.get(_c, "#888"), label=_c, edgecolor="white", linewidth=0.5)
    _ax.text(0.4, _d.h_index.max() * 0.96, "≤7 yrs · junior / rising-star zone", fontsize=8.5, color="#b45309", fontweight="bold")
    _ax.set_xlabel("Years since lab started (lower = more junior)")
    _ax.set_ylabel("Google Scholar h-index")
    _ax.set_title("PI landscape: lab age vs h-index, by fit category", fontsize=11)
    _ax.legend(title="Category", loc="upper right"); _fig.tight_layout()
    _jr = _d[(_d.years_active <= 7) & (_d.category.isin(["rising_star", "direction_fit"]))]
    mo.vstack([_fig, mo.md(f"**{len(_jr)} 位「年轻(≤7y)且契合」PI** —— 正是你偏好的画像。")])
    return


@app.cell
def _(mo, section):
    mo.Html(section("Coverage", "🧬 兴趣方向覆盖热图", "每格 = 该项目里命中某兴趣方向的 PI 数（按 PI 研究/契合描述自动打标签）。颜色越深 = 该方向越强。看你「topic flexible」下各方向最强的项目。"))
    return


@app.cell
def _(INTEREST_AREAS, mo, plt, prog_ia):
    _d = prog_ia.copy(); _d["fitn"] = _d.fit.fillna(0)
    _d = _d.sort_values(["region", "fitn"], ascending=[True, False])
    _areas = list(INTEREST_AREAS.keys()); _mat = _d[_areas].values
    _fig, _ax = plt.subplots(figsize=(9, 14))
    _im = _ax.imshow(_mat, aspect="auto", cmap="YlGnBu", vmin=0, vmax=max(3, _mat.max()))
    _ax.set_xticks(range(len(_areas))); _ax.set_xticklabels(_areas, rotation=40, ha="right", fontsize=8.5)
    _ax.set_yticks(range(len(_d))); _ax.set_yticklabels([f"[{r[:2]}] {s[:16]} — {p[:20]}" for r, s, p in zip(_d.region, _d.school, _d.program)], fontsize=5.5)
    for _i in range(_mat.shape[0]):
        for _j in range(_mat.shape[1]):
            if _mat[_i, _j]:
                _ax.text(_j, _i, int(_mat[_i, _j]), ha="center", va="center", fontsize=5.5, color="white" if _mat[_i, _j] > _mat.max() * 0.55 else "#1e293b")
    _cb = _fig.colorbar(_im, ax=_ax, fraction=0.024, pad=0.02); _cb.set_label("# target PIs matching the interest area", fontsize=8)
    _ax.set_title("Interest-area coverage by program (# matching PIs)", fontsize=11); _fig.tight_layout()
    _fig
    return


@app.cell
def _(mo, section):
    mo.Html(section("Overview", "📈 概览图", "fit × stipend 全景，以及按 h-index 排名的 Top-25 目标 PI。"))
    return


@app.cell
def _(FLOOR, REGION_COLORS, REGION_LABEL, mo, plt, programs_df):
    _d = programs_df.dropna(subset=["stipend_usd", "fit"]); _d = _d[_d.stipend_usd >= 0]
    _fig, _ax = plt.subplots(figsize=(9.5, 6))
    for _reg, _g in _d.groupby("region"):
        _ax.scatter(_g.stipend_usd, _g.fit, s=78, alpha=0.84, color=REGION_COLORS.get(_reg, "#888"), label=REGION_LABEL.get(_reg, _reg), edgecolor="white", linewidth=0.7)
    for _r in _d.itertuples():
        _ax.annotate(str(_r.school)[:13], (_r.stipend_usd, _r.fit), fontsize=5, alpha=0.7, xytext=(3, 2), textcoords="offset points")
    _ax.axvline(FLOOR, color="#ef4444", linestyle="--", linewidth=1.1); _ax.text(FLOOR * 1.01, _d.fit.min(), f"${FLOOR // 1000}k floor", color="#ef4444", fontsize=8)
    _ax.set_xlabel("Annual PhD stipend (USD/yr, re-verified)"); _ax.set_ylabel("Fit-for-candidate score (1–10)")
    _ax.set_title("Fit vs stipend — each point = one program", fontsize=11); _ax.legend(title="Region"); _fig.tight_layout()
    _fig
    return


@app.cell
def _(CAT_COLORS, mo, pis_df, plt):
    _d = pis_df.dropna(subset=["h_index"]).sort_values("h_index").tail(25)
    _fig, _ax = plt.subplots(figsize=(9.5, 8))
    _ax.barh(range(len(_d)), _d.h_index, color=[CAT_COLORS.get(c, "#888") for c in _d.category])
    _ax.set_yticks(range(len(_d))); _ax.set_yticklabels([f"{n[:22]} ({s[:11]})" for n, s in zip(_d.name, _d.school)], fontsize=6)
    _ax.set_xlabel("Google Scholar h-index"); _ax.set_ylabel("Principal investigator")
    _ax.set_title("Top-25 target PIs by h-index (colour = fit category)", fontsize=11); _fig.tight_layout()
    _fig
    return


@app.cell
def _(mo, section):
    mo.Html(section("Statistics", "📐 统计分析与建议", "用统计说话：相关性 · 分布检验（Kruskal–Wallis / Mann–Whitney）· Pareto 前沿 · K-means 聚类。图表为 Nature 出版风格（同款已导出到 figures/）。", "stats"))
    return


@app.cell
def _(KMeans, PCA, REGIONS_PRESENT, StandardScaler, np, pd, pis_df, programs_df, stats):
    _d = programs_df.dropna(subset=["fit", "stipend_usd"])
    rho_fs, p_fs = stats.spearmanr(_d.stipend_usd, _d.fit)
    rho_fp, p_fp = stats.spearmanr(programs_df.fit, programs_df.n_pifit, nan_policy="omit")
    _ord = REGIONS_PRESENT
    _g = [programs_df[programs_df.region == r].stipend_usd.dropna().values for r in _ord]
    kw_reg_p = stats.kruskal(*[x for x in _g if len(x)])[1]
    reg_med = {r: int(np.median(x)) for r, x in zip(_ord, _g) if len(x)}
    _co = ["rising_star", "direction_fit", "interesting", "famous_but_fits"]
    _h = [pis_df[pis_df.category == c].h_index.dropna().values for c in _co]
    kw_cat_p = stats.kruskal(*[x for x in _h if len(x)])[1]
    cat_med = {c: int(np.nanmedian(x)) for c, x in zip(_co, _h) if len(x)}
    _pf = programs_df.dropna(subset=["fit", "stipend_usd"]); _pf = _pf[_pf.meets_floor]
    _pts = _pf[["stipend_usd", "fit"]].values
    _par = [i for i, (s, f) in enumerate(_pts) if not any((_pts[:, 0] >= s) & (_pts[:, 1] >= f) & ((_pts[:, 0] > s) | (_pts[:, 1] > f)))]
    pareto_df = _pf.iloc[_par].sort_values(["fit", "stipend_usd"], ascending=False)
    _cf = ["fit", "stipend_usd", "urban", "n_pifit", "median_h"]
    _X = programs_df[_cf].apply(pd.to_numeric, errors="coerce"); _X = _X.fillna(_X.median())
    _nrow = len(_X)
    cl_df = programs_df.copy()
    if _nrow >= 2:
        _Xs = StandardScaler().fit_transform(_X)
        _k = min(4, _nrow)
        _km = KMeans(n_clusters=_k, random_state=0, n_init=10).fit(_Xs)
        _Z = PCA(n_components=2, random_state=0).fit_transform(_Xs) if _nrow >= 2 else np.zeros((_nrow, 2))
        cl_df["cluster"] = _km.labels_; cl_df["pc1"] = _Z[:, 0]; cl_df["pc2"] = _Z[:, 1]
    else:
        cl_df["cluster"] = 0; cl_df["pc1"] = 0.0; cl_df["pc2"] = 0.0
    cl_prof = cl_df.groupby("cluster")[_cf].mean().round(1)
    return cat_med, cl_df, cl_prof, kw_cat_p, kw_reg_p, p_fs, pareto_df, reg_med, rho_fp, rho_fs


@app.cell
def _(REGION_LABEL, cat_med, cl_df, cl_prof, kw_cat_p, kw_reg_p, mo, p_fs, pareto_df, programs_df, reg_med, rho_fp, rho_fs):
    _best = cl_prof.fit.idxmax(); _pir = cl_prof.n_pifit.idxmax()
    _bm = " · ".join(cl_df[cl_df.cluster == _best].sort_values("fit", ascending=False).school.head(8).tolist())
    _pm = " · ".join(cl_df[cl_df.cluster == _pir].sort_values("n_pifit", ascending=False).school.head(7).tolist())
    _par = "；".join(f"<b>{r.school}</b> (fit {r.fit}, ${int(r.stipend_usd):,})" for _, r in pareto_df.iterrows())

    def _rec(n, color, stat, adv):
        return (f'<div style="display:flex;gap:14px;padding:14px 16px;border:1px solid #e7ecf3;border-radius:14px;'
                f'background:#fff;box-shadow:0 2px 10px rgba(15,23,42,.05);margin-bottom:11px">'
                f'<div style="flex:none;width:34px;height:34px;border-radius:10px;background:{color}1f;color:{color};'
                f'font-weight:800;display:flex;align-items:center;justify-content:center;font-size:14px">{n}</div>'
                f'<div><div style="font-weight:700;color:#0f172a;font-size:13.5px;margin-bottom:3px">{stat}</div>'
                f'<div style="color:#475569;font-size:12.5px;line-height:1.58">{adv}</div></div></div>')
    _html = ('<div style="border:1px solid #dbeafe;background:linear-gradient(135deg,#f8fbff,#eef6ff);'
             'border-radius:18px;padding:20px 22px;box-shadow:0 6px 24px rgba(15,23,42,.06)">'
             '<div style="font-size:16px;font-weight:800;color:#1e3a8a;margin-bottom:14px">🧠 统计意义上的 6 条申请建议</div>'
             + _rec("01", "#0F4D92", f"契合度 × stipend：Spearman ρ = {rho_fs:.2f}（P = {p_fs:.0e}）",
                    ("契合度最高的项目往往 stipend 也更高 —— <b>不存在「钱 vs 契合」的取舍</b>，放心按契合度优化。" if rho_fs > 0.2 else "契合度与 stipend 关系不强 —— 两者可基本独立地各自优化。"))
             + _rec("02", "#E2A52C", f"项目 fit 与「rising/契合 PI 数」相关性：ρ = {rho_fp:.2f}",
                    "<b>别只看项目 fit 分</b> —— 它未必预测你能找到多少契合 PI。用下方热图 / PI 浏览器按 <b>PI 优先</b>找，fit 中等的项目也可能 PI 极契合。")
             + _rec("03", "#3775BA", f"四类 PI 的 h-index 差异：Kruskal–Wallis P = {kw_cat_p:.0e}",
                    f"中位 rising <b>{cat_med.get('rising_star','—')}</b> · dir-fit <b>{cat_med.get('direction_fit','—')}</b> · interesting <b>{cat_med.get('interesting','—')}</b> · famous <b>{cat_med.get('famous_but_fits','—')}</b>。要<b>年轻高潜力</b>导师锁定 h 较低的 rising_star；要稳资源找 famous。")
             + _rec("04", "#42949E", f"stipend 地区差异：Kruskal–Wallis P = {kw_reg_p:.3f}",
                    "中位 stipend：" + " ＞ ".join(f"<b>{REGION_LABEL.get(_k,_k)} ${_v:,}</b>" for _k, _v in sorted(reg_med.items(), key=lambda kv: -kv[1])) + "。据此权衡地区与经费；低 stipend 地区多需 fellowship 才过线。")
             + _rec("05", "#B64342", f"Pareto 最优（fit 与 stipend 都无法被同时超越）：{len(pareto_df)} 个",
                    f"{_par}。其余项目在这两维都被它们「支配」——可作上限参照；但 fit 粒度较粗，别只用 Pareto 选校。")
             + _rec("06", "#9A4D8E", f"K-means 把 {len(programs_df)} 个项目分 4 组，甜区 = C{_best+1}",
                    f"C{_best+1}（均 fit {cl_prof.loc[_best,'fit']}，${int(cl_prof.loc[_best,'stipend_usd']):,}，中位 h {cl_prof.loc[_best,'median_h']}）：{_bm}…。另有「PI 最密」的 C{_pir+1}（n_pifit≈{cl_prof.loc[_pir,'n_pifit']}、更年轻）：{_pm} —— PI-first 视角下同样值得冲。")
             + '</div>')
    mo.Html(_html)
    return


@app.cell
def _(REGION_COLORS, REGION_LABEL, mo, np, plt, programs_df, stats):
    _d = programs_df.dropna(subset=["fit", "stipend_usd"])
    _x = _d.stipend_usd.values / 1000.0; _y = _d.fit.values
    _n = len(_x)
    _fig, _ax = plt.subplots(figsize=(8.6, 5.4))
    for _r, _gg in _d.groupby("region"):
        _ax.scatter(_gg.stipend_usd / 1000, _gg.fit, s=42, color=REGION_COLORS.get(_r, "#888"), alpha=.85, edgecolor="white", linewidth=.5, label=REGION_LABEL.get(_r, _r))
    if _n >= 3 and np.ptp(_x) > 0:
        _rho, _p = stats.spearmanr(_x, _y); _sl, _ic, _, _, _ = stats.linregress(_x, _y)
        _xs = np.linspace(_x.min(), _x.max(), 100); _yh = _ic + _sl * _xs
        _se = np.sqrt(np.sum((_y - (_ic + _sl * _x)) ** 2) / (_n - 2))
        _ci = 1.96 * _se * np.sqrt(1.0 / _n + (_xs - _x.mean()) ** 2 / np.sum((_x - _x.mean()) ** 2))
        _ax.plot(_xs, _yh, color="#4D4D4D", lw=1.6); _ax.fill_between(_xs, _yh - _ci, _yh + _ci, color="#767676", alpha=.15)
        _ax.text(.03, .95, f"Spearman ρ = {_rho:.2f}\nP = {_p:.1e}", transform=_ax.transAxes, va="top", fontsize=10,
                 bbox=dict(boxstyle="round,pad=0.35", fc="white", ec="#cfcece", lw=.7))
    else:
        _ax.text(.03, .95, f"n={_n} — 样本过少，跳过回归", transform=_ax.transAxes, va="top", fontsize=10, color="#767676")
    _ax.set_xlabel("Annual stipend (USD ×10³ / yr)"); _ax.set_ylabel("Fit-for-candidate score (1–10)")
    _ax.set_title("Fit vs stipend"); _ax.legend(title="Region")
    _fig.tight_layout()
    mo.vstack([mo.md("**① 契合度 × stipend** — 散点 + OLS 回归 + 95% CI + Spearman 检验"), _fig])
    return


@app.cell
def _(FLOOR, REGIONS_PRESENT, REGION_COLORS, REGION_LABEL, mo, np, plt, programs_df, stats):
    _ord = REGIONS_PRESENT
    _g = [programs_df[programs_df.region == r].stipend_usd.dropna().values for r in _ord]
    _n = len(_ord)
    _h, _p = stats.kruskal(*[x for x in _g if len(x)]) if sum(len(x) > 0 for x in _g) >= 2 else (float("nan"), float("nan"))
    _fig, _ax = plt.subplots(figsize=(max(4.5, 2.2 * _n), 5.0))
    _bp = _ax.boxplot(_g, positions=range(_n), widths=.55, patch_artist=True, showfliers=False,
                      medianprops=dict(color="#4D4D4D", lw=1.3), whiskerprops=dict(color="#767676", lw=.9), capprops=dict(color="#767676", lw=.9))
    for _pa, _r in zip(_bp["boxes"], _ord):
        _pa.set(facecolor=REGION_COLORS[_r], alpha=.28, edgecolor=REGION_COLORS[_r], linewidth=1.0)
    for _i, (_r, _v) in enumerate(zip(_ord, _g)):
        _ax.scatter(np.random.default_rng(_i).normal(_i, .07, len(_v)), _v, s=20, color=REGION_COLORS[_r], alpha=.8, edgecolor="white", linewidth=.4, zorder=3)
    _ax.axhline(FLOOR, color="#B64342", ls="--", lw=1.0); _ax.text(_n - 0.65, FLOOR * 1.03, f"${FLOOR // 1000}k floor", color="#B64342", fontsize=8)
    _ax.set_xticks(range(_n)); _ax.set_xticklabels([REGION_LABEL.get(_r, _r) for _r in _ord]); _ax.set_ylabel("Annual stipend (USD / yr)")
    _ax.set_title("Stipend by region"); _ax.text(.03, .96, f"Kruskal–Wallis\nH={_h:.1f}, P={_p:.2g}", transform=_ax.transAxes, va="top", fontsize=9,
             bbox=dict(boxstyle="round,pad=0.35", fc="white", ec="#cfcece", lw=.7))
    _fig.tight_layout()
    mo.vstack([mo.md("**② stipend 地区分布** — 箱线 + 散点 + Kruskal–Wallis（US 显著高于 EU/HK；EU≈HK）"), _fig])
    return


@app.cell
def _(CAT_COLORS, mo, np, pis_df, plt, stats):
    _co = ["rising_star", "direction_fit", "interesting", "famous_but_fits"]
    _h = [pis_df[pis_df.category == c].h_index.dropna().values for c in _co]
    _kh, _kp = stats.kruskal(*[x for x in _h if len(x)])
    _fig, _ax = plt.subplots(figsize=(7.6, 5.0))
    _bp = _ax.boxplot(_h, positions=range(4), widths=.55, patch_artist=True, showfliers=False,
                      medianprops=dict(color="#4D4D4D", lw=1.3), whiskerprops=dict(color="#767676", lw=.9), capprops=dict(color="#767676", lw=.9))
    for _pa, _c in zip(_bp["boxes"], _co):
        _pa.set(facecolor=CAT_COLORS[_c], alpha=.30, edgecolor=CAT_COLORS[_c], linewidth=1.0)
    for _i, (_c, _v) in enumerate(zip(_co, _h)):
        _ax.scatter(np.random.default_rng(_i + 9).normal(_i, .07, len(_v)), _v, s=10, color=CAT_COLORS[_c], alpha=.55, edgecolor="white", linewidth=.2, zorder=3)
    _ax.set_xticks(range(4)); _ax.set_xticklabels(["rising", "dir-fit", "interest", "famous"], rotation=10)
    _ax.set_ylabel("Google Scholar h-index"); _ax.set_title("PI h-index by fit category")
    _ax.text(.03, .96, f"Kruskal–Wallis\nH={_kh:.0f}, P={_kp:.1e}", transform=_ax.transAxes, va="top", fontsize=9,
             bbox=dict(boxstyle="round,pad=0.35", fc="white", ec="#cfcece", lw=.7))
    _fig.tight_layout()
    mo.vstack([mo.md("**③ PI h-index × 类型** — rising_star 显著低于 famous（标签自洽，可据此找年轻高潜力导师）"), _fig])
    return


@app.cell
def _(mo, np, pd, plt, programs_df, stats):
    _feat = ["fit", "stipend_usd", "urban", "n_rising", "n_dirfit", "median_h", "pi_count"]
    _lab = ["fit", "stipend", "city", "#rising", "#dir-fit", "med h", "#PI"]
    _M = programs_df[_feat].apply(pd.to_numeric, errors="coerce")
    _C = _M.corr(method="spearman").values
    _fig, _ax = plt.subplots(figsize=(6.6, 5.6))
    _im = _ax.imshow(_C, cmap="RdBu_r", vmin=-1, vmax=1, aspect="auto")
    _ax.set_xticks(range(len(_lab))); _ax.set_xticklabels(_lab, rotation=40, ha="right", fontsize=8)
    _ax.set_yticks(range(len(_lab))); _ax.set_yticklabels(_lab, fontsize=8)
    for _i in range(len(_feat)):
        for _j in range(len(_feat)):
            _ax.text(_j, _i, f"{_C[_i,_j]:.2f}", ha="center", va="center", fontsize=7, color="white" if abs(_C[_i, _j]) > .55 else "#1e293b")
    _cb = _fig.colorbar(_im, ax=_ax, fraction=.046, pad=.03); _cb.set_label("Spearman ρ", fontsize=8)
    _ax.set_title("Program-feature correlation (Spearman)"); _ax.grid(False)
    _fig.tight_layout()
    mo.vstack([mo.md("**④ 特征相关性矩阵** — 注意 fit 与 #rising/#dir-fit 近乎 0：项目 fit 不代表 PI 契合密度"), _fig])
    return


@app.cell
def _(mo, plt, programs_df):
    _d = programs_df.dropna(subset=["fit", "stipend_usd"]); _d = _d[_d.meets_floor].copy()
    _pts = _d[["stipend_usd", "fit"]].values
    _par = [i for i, (s, f) in enumerate(_pts) if not any((_pts[:, 0] >= s) & (_pts[:, 1] >= f) & ((_pts[:, 0] > s) | (_pts[:, 1] > f)))]
    _d["par"] = False; _d.iloc[_par, _d.columns.get_loc("par")] = True
    _fig, _ax = plt.subplots(figsize=(8.0, 5.4))
    _o = _d[~_d.par]; _pf = _d[_d.par].sort_values("stipend_usd")
    _ax.scatter(_o.stipend_usd / 1000, _o.fit, s=28, color="#CFCECE", edgecolor="white", linewidth=.4, label="dominated")
    _ax.plot(_pf.stipend_usd / 1000, _pf.fit, color="#B64342", lw=1.3, ls="--", zorder=1)
    _ax.scatter(_pf.stipend_usd / 1000, _pf.fit, s=64, color="#B64342", edgecolor="white", linewidth=.6, zorder=2, label="Pareto-optimal")
    for _, _r in _pf.iterrows():
        _ax.annotate(_r.school[:14], (_r.stipend_usd / 1000, _r.fit), fontsize=7, color="#4D4D4D", xytext=(4, 4), textcoords="offset points")
    _ax.set_xlabel("Annual stipend (USD ×10³ / yr)"); _ax.set_ylabel("Fit score (1–10)")
    _ax.set_title("Pareto frontier — maximise fit & stipend (floor-passing)"); _ax.legend(loc="lower right")
    _fig.tight_layout()
    mo.vstack([mo.md("**⑤ Pareto 前沿** — 红点 = 在 fit 与 stipend 上都无法被同时超越的非支配项目"), _fig])
    return


@app.cell
def _(cl_df, cl_prof, mo, plt):
    _cc = ["#0F4D92", "#8BCF8B", "#E2A52C", "#9A4D8E"]
    _fig, _ax = plt.subplots(figsize=(8.0, 5.6))
    for _k in sorted(cl_df.cluster.unique()):
        _m = cl_df.cluster == _k
        _lab = f"C{_k+1} (n={_m.sum()}, fit {cl_prof.loc[_k,'fit']}, ${int(cl_prof.loc[_k,'stipend_usd']/1000)}k)"
        _ax.scatter(cl_df[_m].pc1, cl_df[_m].pc2, s=30, color=_cc[_k % 4], alpha=.82, edgecolor="white", linewidth=.5, label=_lab)
    for _, _r in cl_df.sort_values("fit", ascending=False).head(8).iterrows():
        _ax.annotate(_r.school[:12], (_r.pc1, _r.pc2), fontsize=6, color="#4D4D4D", xytext=(3, 3), textcoords="offset points")
    _ax.set_xlabel("PC1"); _ax.set_ylabel("PC2"); _ax.set_title("Program clusters (K-means on 5 standardized features → PCA)")
    _ax.legend(fontsize=7, loc="best"); _fig.tight_layout()
    mo.vstack([mo.md("**⑥ 项目聚类** — 标准化[fit·stipend·城市·契合PI数·中位h] → K-means(4) → PCA 投影"), _fig])
    return


@app.cell
def _(mo):
    mo.Html("""<div class="foot"><b>PhD Application Planner</b> · powered by <b>marimo</b> · 交互式 PhD 申请决策仪表盘<br>
    数据来自 <code>_research_data.json</code> / <code>_rows.json</code>（并行 web 检索 + 逐项核验生成）；备注/隐藏存于 <code>_pi_notes.json</code> / <code>_pi_hidden.json</code>，跨会话保留。<br>
    stipend 为检索快照、请以各项目官方页面为准；h-index 为 Google Scholar 快照，落地前请按链接复核。</div>""")
    return


if __name__ == "__main__":
    app.run()
