# -*- coding: utf-8 -*-
r"""
update_llm_matrix.py -- LLM Matrix management tool for Life Admin

Single source of truth for model scores, pricing, and position recommendations.
Generates a 3-tab HTML dashboard and runs the LLM hiring algorithm.

Usage:
  python update_llm_matrix.py              # Regenerate llm-matrix.html
  python update_llm_matrix.py --stale      # List models not checked in 7+ days
  python update_llm_matrix.py --research   # Print research prompt for Claude Code
  python update_llm_matrix.py --skills     # Show skills gap report for all positions
  python update_llm_matrix.py --hire       # Run hiring algorithm, show recommendations
  python update_llm_matrix.py --open       # Regenerate and open in browser

Data file: D:\paperclip\scripts\llm-matrix-data.json
Output:    D:\paperclip\scripts\llm-matrix.html
"""

import json
import sys
import webbrowser
from datetime import datetime
from pathlib import Path

SCRIPTS_DIR = Path(__file__).parent
POSITIONS_DIR = SCRIPTS_DIR.parent / "positions"
DATA_FILE = SCRIPTS_DIR / "llm-matrix-data.json"
HTML_FILE = SCRIPTS_DIR / "llm-matrix.html"
POSITIONS_JSON = POSITIONS_DIR / "positions.json"

TASK_LABELS = {
    "coding":    "Coding",
    "reasoning": "Reasoning",
    "writing":   "Writing",
    "research":  "Research",
    "creative":  "Creative",
    "speed":     "Speed",
    "cost_eff":  "Cost Eff",
}

# Short display names for model chips in the position recommendations table
MODEL_SHORT_NAMES = {
    "claude-opus-4-6":     "Opus 4.6",
    "claude-sonnet-4-6":   "Sonnet 4.6",
    "claude-haiku-4-5":    "Haiku 4.5",
    "grok-3":              "Grok-3",
    "grok-4.1":            "Grok-4.1",
    "grok-code-fast-1":    "Grok Fast",
    "grok-3-mini":         "Grok Mini",
    "gemma4:26b":          "Gemma4:26b",
    "deepseek-chat":       "DS Chat",
    "deepseek-reasoner":   "DS R1",
    "mistral-large-latest":"Mistral L",
    "mistral-small-4":     "Mistral S",
    "kimi-k2.5":           "Kimi K2.5",
    "gemini-2.5-flash":    "Gem. Flash",
    "gpt-5.3-codex":       "Codex",
    "minimax-m2.7":        "MiniMax M2",
    "minimax-text-01":     "MiniMax T01",
    "qwen-plus":           "Qwen+",
    "codestral":           "Codestral",
}

# ─── Data helpers ─────────────────────────────────────────────────────────────

def load_data():
    with open(DATA_FILE, encoding="utf-8") as f:
        return json.load(f)

def load_positions_state():
    try:
        with open(POSITIONS_JSON, encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {"positions": {}}

def is_stale(last_checked, days=7):
    if not last_checked:
        return True
    try:
        checked = datetime.fromisoformat(last_checked)
        return (datetime.now() - checked).days > days
    except Exception:
        return True

def score_colour(score):
    if score >= 9:  return "#bbf7d0"
    elif score >= 7: return "#d9f99d"
    elif score >= 5: return "#fef9c3"
    elif score >= 3: return "#fed7aa"
    else:            return "#fecaca"

def score_text_colour(score):
    if score >= 7: return "#14532d"
    elif score >= 5: return "#78350f"
    else:            return "#7f1d1d"

def format_price(val):
    if val == 0:
        return "—"
    if val < 1:
        return f"${val:.2f}"
    return f"${val:.0f}"

# ─── Hiring algorithm ─────────────────────────────────────────────────────────

def compute_rankings(data):
    """For each position, rank all eligible models by weighted task score."""
    models = {m["id"]: m for m in data["models"] if m.get("status") != "deprecated"}
    rankings = {}

    for pos_key, profile in data["position_profiles"].items():
        constraints = profile.get("constraints", {})
        local_only = constraints.get("local_only", False)
        allow_claude = constraints.get("allow_claude", True)  # default True (no restriction)
        task_weights = profile.get("tasks", {})

        candidates = []
        for model_id, model in models.items():
            if local_only and not model.get("local_only", False):
                continue
            if model_id == "gemma4:26b" and not local_only:
                continue  # gemma4 reserved for Emergency only on non-local positions
            if not allow_claude and model.get("adapter") == "claude_local":
                continue  # Claude tokens reserved for designated positions only

            weighted = sum(
                model["scores"].get(task, 5) * weight
                for task, weight in task_weights.items()
            )
            candidates.append({
                "model_id": model_id,
                "name": model["name"],
                "provider": model["provider"],
                "score": round(weighted, 2),
                "adapter": model["adapter"],
                "cost_note": model["pricing_note"],
            })

        candidates.sort(key=lambda x: -x["score"])
        rankings[pos_key] = candidates

    return rankings

# ─── Skills gap report ────────────────────────────────────────────────────────

def load_skills_status():
    """Read all SKILLS.md files and return per-position skills info."""
    result = {}
    for pos_key in _all_position_keys():
        dept_path = _dept_path_for(pos_key)
        if not dept_path:
            continue
        skills_file = POSITIONS_DIR / dept_path / "SKILLS.md"
        pd_file = POSITIONS_DIR / dept_path / "PD.md"
        if not skills_file.exists():
            result[pos_key] = {"installed": [], "pending": [], "custom": [], "mcp": []}
            continue
        with open(skills_file, encoding="utf-8") as f:
            content = f.read()
        result[pos_key] = _parse_skills_md(content)
    return result

def _parse_skills_md(content):
    """Parse new-format SKILLS.md into installed/pending/custom/mcp sections."""
    sections = {"installed": [], "pending": [], "custom": [], "mcp": []}
    current_section = None
    for line in content.splitlines():
        l = line.strip()
        if "## System Skills" in l or "## Document Skills" in l or "(installed)" in l.lower():
            current_section = "installed"
        elif "pending" in l.lower() or "vet" in l.lower():
            current_section = "pending"
        elif "custom" in l.lower() or "build" in l.lower():
            current_section = "custom"
        elif "mcp" in l.lower():
            current_section = "mcp"
        elif l.startswith("- ") and current_section:
            item = l.lstrip("- ").strip().split("—")[0].strip()
            if item and not item.startswith("#"):
                sections[current_section].append(item)
    return sections

def _all_position_keys():
    try:
        with open(POSITIONS_JSON, encoding="utf-8") as f:
            data = json.load(f)
        return list(data["positions"].keys())
    except Exception:
        return []

def _dept_path_for(pos_key):
    """Map position key to dept_path by reading positions.json."""
    try:
        with open(POSITIONS_JSON, encoding="utf-8") as f:
            data = json.load(f)
        return data["positions"].get(pos_key, {}).get("dept_path", "")
    except Exception:
        return ""

# ─── CLI commands ─────────────────────────────────────────────────────────────

def cmd_stale():
    data = load_data()
    stale = [m for m in data["models"] if is_stale(m.get("last_checked"))]
    if not stale:
        print("All models checked within the last 7 days. Nothing stale.")
        return
    print(f"\nStale models ({len(stale)} need checking):")
    print("-" * 50)
    for m in stale:
        last = m.get("last_checked", "never")
        print(f"  {m['name']:<30} last checked: {last}")
    print()
    print("To update: edit llm-matrix-data.json with new scores/pricing,")
    print("           then run: python update_llm_matrix.py")

def cmd_research():
    data = load_data()
    stale = [m for m in data["models"] if is_stale(m.get("last_checked"))]
    print(f"\nLLM Matrix — Research Needed ({datetime.now().strftime('%Y-%m-%d')})")
    print("=" * 60)
    if stale:
        print(f"\nStale models ({len(stale)}):")
        for m in stale:
            print(f"  • {m['provider']}: {m['name']} — check pricing + capability updates")
    else:
        print("  All models are up to date (checked within 7 days).")
    print("""
Research checklist:
  1. Anthropic: claude.ai/news — new model releases, pricing changes
  2. xAI: x.ai/api — Grok pricing, new variants
  3. Google: ai.google.dev — Gemini pricing, Flash/Pro updates
  4. Mistral: mistral.ai/technology — new models, pricing
  5. Moonshot/Kimi: platform.moonshot.cn — Kimi pricing
  6. DeepSeek: api-docs.deepseek.com — pricing, new versions
  7. OpenAI: openai.com/codex — Codex task limits, new features
  8. MiniMax/Qwen: check provider dashboards

Update process:
  1. Edit D:\\paperclip\\scripts\\llm-matrix-data.json
     — update input_per_1m, output_per_1m, scores, last_checked
     — add new models if released
  2. Run: python update_llm_matrix.py
  3. Run: python update_llm_matrix.py --hire  (check if lineup changes needed)
  4. Run: python position_manager.py sync all  (push updated pricing to agents)
""")

def cmd_skills():
    skills_data = load_skills_status()
    state = load_positions_state()
    print(f"\nSkills Gap Report — {datetime.now().strftime('%Y-%m-%d')}")
    print("=" * 70)
    print(f"{'Position':<20} {'Installed':<10} {'Pending':<10} {'Custom':<10} {'MCP':<10}")
    print("-" * 70)
    for pos_key, skills in skills_data.items():
        inst = len(skills.get("installed", []))
        pend = len(skills.get("pending", []))
        cust = len(skills.get("custom", []))
        mcp = len(skills.get("mcp", []))
        total = inst + pend + cust
        pct = f"{(inst / total * 100):.0f}%" if total > 0 else "0%"
        gap_flag = "[!] " if pend + cust > 0 else "[+] "
        print(f"  {gap_flag}{pos_key:<18} {inst:<10} {pend:<10} {cust:<10} {mcp:<10} ({pct} installed)")
    print()

def cmd_hire():
    data = load_data()
    state = load_positions_state()
    rankings = compute_rankings(data)

    print(f"\nHIRING ROUND — {datetime.now().strftime('%Y-%m-%d')}")
    print("=" * 70)

    changes_recommended = []
    for pos_key, candidates in rankings.items():
        current_pos = state["positions"].get(pos_key, {})
        current_model = current_pos.get("active_model", "unknown")
        current_slot = current_pos.get("active_slot", "Primary")
        profile = data["position_profiles"].get(pos_key, {})
        display_name = profile.get("display_name", pos_key)

        top3 = candidates[:3]
        primary_name = top3[0]["name"] if top3 else "N/A"
        is_current_best = any(c["name"].lower() in current_model.lower() or
                              current_model.lower() in c["name"].lower()
                              for c in top3[:1])

        print(f"\n{display_name}")
        for i, c in enumerate(top3):
            slot_label = ["Primary", "Fallback 1", "Fallback 2"][i]
            print(f"  {slot_label:<12} {c['name']:<28} score: {c['score']:.2f}  ({c['cost_note']})")

        if not is_current_best and current_slot == "Primary":
            changes_recommended.append({
                "position": pos_key,
                "display": display_name,
                "current": current_model,
                "recommended": primary_name,
                "score": top3[0]["score"] if top3 else 0,
            })
            print(f"  [!] CURRENT: {current_model} -- recommended change to {primary_name}")

    print("\n" + "=" * 70)
    if changes_recommended:
        print(f"\n{len(changes_recommended)} position(s) with recommended changes:")
        for c in changes_recommended:
            print(f"  • {c['display']}: {c['current']} → {c['recommended']} (score {c['score']:.2f})")
        print("\nTo apply: review above, then use position_manager.py sub/sync as needed.")
    else:
        print("\n✅  All positions are on their best-fit model. No changes recommended.")
    print()

# ─── HTML generation ──────────────────────────────────────────────────────────

def generate_html():
    data = load_data()
    state = load_positions_state()
    rankings = compute_rankings(data)
    skills_data = load_skills_status()

    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    last_updated = data.get("last_updated", "unknown")

    all_providers = sorted(set(m["provider"] for m in data["models"]))
    task_cols = list(TASK_LABELS.keys())

    # ── Models tab ─────────────────────────────────────────────────────────────
    model_rows = ""
    for m in data["models"]:
        stale_badge = ' <span class="badge warn">⚠️ Check</span>' if is_stale(m.get("last_checked")) else ""
        deprecated = m.get("status") == "deprecated"
        row_class = 'class="deprecated"' if deprecated else ""
        score_cells = ""
        for task in task_cols:
            s = m["scores"].get(task, 0)
            bg = score_colour(s)
            tc = score_text_colour(s)
            score_cells += f'<td style="background:{bg};color:{tc};font-weight:600;text-align:center">{s}</td>'

        model_rows += f"""
        <tr {row_class} data-provider="{m['provider']}">
          <td><strong>{m['name']}</strong>{stale_badge}</td>
          <td>{m['provider']}</td>
          <td><code>{m['adapter']}</code></td>
          <td style="text-align:right">{format_price(m['input_per_1m'])}</td>
          <td style="text-align:right">{format_price(m['output_per_1m'])}</td>
          {score_cells}
          <td style="color:#64748b;font-size:0.8em">{m.get('notes','')}</td>
        </tr>"""

    # ── Position recommendations (part of Models tab) ─────────────────────────
    pos_rec_rows = ""
    for pos_key, candidates in rankings.items():
        profile = data["position_profiles"].get(pos_key, {})
        display_name = profile.get("display_name", pos_key)
        current_pos = state["positions"].get(pos_key, {})
        current_model = current_pos.get("active_model", "—")
        local_only = profile.get("constraints", {}).get("local_only", False)
        local_badge = ' <span class="badge local">LOCAL ONLY</span>' if local_only else ""

        top = candidates[:1]
        best_name = top[0]["name"] if top else "N/A"
        best_score = top[0]["score"] if top else 0
        is_current_best = any(c["name"].lower() in current_model.lower() or
                              current_model.lower() in c["name"].lower()
                              for c in top)
        status_cell = '<span class="badge ok">✅ Best fit</span>' if is_current_best else f'<span class="badge warn">⚠️ {best_name} better fit</span>'

        top5_chips = ""
        for rank_i, c in enumerate(candidates[:5]):
            cid = c["model_id"]
            cname = c["name"]
            cscore = c["score"]
            cshort = MODEL_SHORT_NAMES.get(cid, cname)
            bg = score_colour(cscore)
            tc = score_text_colour(cscore)
            rank_label = f"#{rank_i+1} " if rank_i == 0 else ""
            top5_chips += (
                f'<span class="slot-chip" title="{cname} - score {cscore:.2f}" '
                f'style="background:{bg};color:{tc};font-weight:{"700" if rank_i==0 else "500"}">'
                f'{rank_label}{cshort}</span>'
            )

        pos_rec_rows += f"""
        <tr>
          <td><strong>{display_name}</strong>{local_badge}</td>
          <td><code style="font-size:0.8em">{current_model}</code></td>
          <td>{top5_chips}</td>
          <td>{status_cell}</td>
        </tr>"""

    # ── Skills tab ─────────────────────────────────────────────────────────────
    skills_rows = ""
    for pos_key, skills in skills_data.items():
        profile = data["position_profiles"].get(pos_key, {})
        display_name = profile.get("display_name", pos_key)
        local_only = profile.get("constraints", {}).get("local_only", False)
        local_badge = ' <span class="badge local">🔒</span>' if local_only else ""

        inst = skills.get("installed", [])
        pend = skills.get("pending", [])
        cust = skills.get("custom", [])
        mcp_list = skills.get("mcp", [])
        total = len(inst) + len(pend) + len(cust)
        gap_pct = int(len(inst) / total * 100) if total > 0 else 0
        gap_colour = "#bbf7d0" if gap_pct >= 80 else "#fef9c3" if gap_pct >= 50 else "#fecaca"

        inst_chips = "".join(f'<span class="skill-chip installed">{s}</span>' for s in inst[:6])
        pend_chips = "".join(f'<span class="skill-chip pending">{s}</span>' for s in (pend + cust)[:4])
        mcp_chips = "".join(f'<span class="skill-chip mcp">{s}</span>' for s in mcp_list[:3])

        skills_rows += f"""
        <tr>
          <td><strong>{display_name}</strong>{local_badge}</td>
          <td style="font-size:0.8em">{inst_chips or '<span style="color:#94a3b8">none</span>'}</td>
          <td style="font-size:0.8em">{pend_chips or '<span style="color:#94a3b8">none</span>'}</td>
          <td style="font-size:0.8em">{mcp_chips or '<span style="color:#94a3b8">none</span>'}</td>
          <td><div style="background:{gap_colour};padding:2px 8px;border-radius:10px;text-align:center;font-size:0.8em;font-weight:600">{gap_pct}%</div></td>
        </tr>"""

    # ── Hiring tab ─────────────────────────────────────────────────────────────
    hiring_rows = ""
    for pos_key, candidates in rankings.items():
        profile = data["position_profiles"].get(pos_key, {})
        display_name = profile.get("display_name", pos_key)
        current_pos = state["positions"].get(pos_key, {})
        current_model = current_pos.get("active_model", "—")
        local_only = profile.get("constraints", {}).get("local_only", False)

        top3 = candidates[:3]
        primary = top3[0] if top3 else None
        f1 = top3[1] if len(top3) > 1 else None
        f2 = top3[2] if len(top3) > 2 else None

        is_best = any(c["name"].lower() in current_model.lower() or
                      current_model.lower() in c["name"].lower()
                      for c in candidates[:1])
        status = '<span class="badge ok">✅ Best fit</span>' if is_best else '<span class="badge warn">⚠️ Change available</span>'

        def model_cell(c):
            if not c: return "<td>—</td>"
            return f'<td><strong>{c["name"]}</strong><br><span style="font-size:0.75em;color:#64748b">{c["score"]:.2f} · {c["cost_note"]}</span></td>'

        hiring_rows += f"""
        <tr>
          <td><strong>{display_name}</strong></td>
          <td><code style="font-size:0.8em">{current_model}</code></td>
          {model_cell(primary)}
          {model_cell(f1)}
          {model_cell(f2)}
          <td>{'<span class="badge local">local</span>' if local_only else ''}</td>
          <td>{status}</td>
        </tr>"""

    # ── Research notes ─────────────────────────────────────────────────────────
    notes_html = ""
    for note in reversed(data.get("research_notes", [])):
        notes_html += f'<div class="note-entry"><strong>{note["date"]}</strong> — {note["note"]}</div>'

    # ── Provider filter buttons ────────────────────────────────────────────────
    provider_btns = '<button class="filter-btn active" onclick="filterProvider(\'all\')">All</button>\n'
    for p in all_providers:
        safe = p.replace(" ", "_").replace("/", "_")
        provider_btns += f'<button class="filter-btn" onclick="filterProvider(\'{p}\')">{p}</button>\n'

    # ── Score header cells ─────────────────────────────────────────────────────
    score_headers = "".join(f"<th>{TASK_LABELS[t]}</th>" for t in task_cols)

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>LLM Matrix — Life Admin</title>
  <style>
    * {{ box-sizing: border-box; }}
    body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; background: #f1f5f9; color: #1e293b; margin: 0; padding: 24px; }}
    h1 {{ font-size: 1.4em; color: #0f172a; margin-bottom: 2px; }}
    .sub {{ color: #64748b; font-size: 0.85em; margin-bottom: 20px; }}

    /* Tabs */
    .tabs {{ display: flex; gap: 4px; margin-bottom: 20px; border-bottom: 2px solid #e2e8f0; }}
    .tab {{ padding: 8px 20px; cursor: pointer; border-radius: 6px 6px 0 0; font-weight: 600; font-size: 0.9em; color: #64748b; border: 1px solid transparent; border-bottom: none; transition: all 0.15s; }}
    .tab.active {{ background: white; color: #0f172a; border-color: #e2e8f0; margin-bottom: -2px; }}
    .tab:hover:not(.active) {{ background: #e2e8f0; color: #334155; }}
    .tab-panel {{ display: none; }}
    .tab-panel.active {{ display: block; }}

    /* Cards / sections */
    .card {{ background: white; border: 1px solid #e2e8f0; border-radius: 10px; padding: 18px; margin-bottom: 20px; overflow-x: auto; }}
    .section-title {{ font-size: 0.72em; text-transform: uppercase; letter-spacing: 0.1em; color: #94a3b8; font-weight: 600; margin-bottom: 12px; }}

    /* Tables */
    table {{ border-collapse: collapse; width: 100%; font-size: 0.85em; }}
    th {{ background: #f8fafc; color: #475569; font-weight: 600; padding: 8px 10px; text-align: left; border-bottom: 2px solid #e2e8f0; white-space: nowrap; font-size: 0.8em; }}
    td {{ padding: 7px 10px; border-bottom: 1px solid #f1f5f9; vertical-align: middle; }}
    tr:hover td {{ background: #f8fafc; }}
    tr.deprecated td {{ opacity: 0.45; }}
    code {{ background: #f1f5f9; padding: 1px 5px; border-radius: 4px; font-size: 0.85em; }}

    /* Badges */
    .badge {{ display: inline-block; padding: 2px 8px; border-radius: 8px; font-size: 0.72em; font-weight: 600; white-space: nowrap; }}
    .badge.ok {{ background: #dcfce7; color: #15803d; }}
    .badge.warn {{ background: #fef9c3; color: #854d0e; }}
    .badge.local {{ background: #dbeafe; color: #1d4ed8; }}

    /* Skill chips */
    .skill-chip {{ display: inline-block; padding: 1px 7px; border-radius: 8px; font-size: 0.75em; margin: 1px; font-weight: 500; }}
    .skill-chip.installed {{ background: #dcfce7; color: #15803d; }}
    .skill-chip.pending {{ background: #fef9c3; color: #854d0e; }}
    .skill-chip.mcp {{ background: #ede9fe; color: #6d28d9; }}

    /* Slot chips (hiring) */
    .slot-chip {{ display: inline-block; background: #e2e8f0; color: #334155; padding: 2px 8px; border-radius: 6px; font-size: 0.75em; margin: 1px; }}

    /* Filter buttons */
    .filters {{ display: flex; gap: 6px; flex-wrap: wrap; margin-bottom: 14px; }}
    .filter-btn {{ padding: 4px 12px; border: 1px solid #e2e8f0; border-radius: 20px; background: white; cursor: pointer; font-size: 0.8em; color: #475569; transition: all 0.15s; }}
    .filter-btn:hover, .filter-btn.active {{ background: #1d4ed8; color: white; border-color: #1d4ed8; }}

    /* Research notes */
    .note-entry {{ padding: 8px 12px; border-left: 3px solid #e2e8f0; margin-bottom: 8px; font-size: 0.85em; color: #475569; }}
    details summary {{ cursor: pointer; font-size: 0.85em; font-weight: 600; color: #475569; padding: 6px 0; }}

    /* Hiring last-run bar */
    .hire-bar {{ background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 10px 16px; margin-bottom: 16px; display: flex; align-items: center; gap: 12px; font-size: 0.85em; color: #475569; }}
    .hire-bar strong {{ color: #0f172a; }}
  </style>
</head>
<body>
  <h1>🧠 LLM Matrix — Life Admin</h1>
  <p class="sub">
    Last data update: <strong>{last_updated}</strong> &bull;
    Dashboard generated: {now} &bull;
    <a href="lineup_dashboard.html">Agent Matrix</a> &bull;
    <a href="ops-hub.html">Ops Hub</a>
  </p>

  <div class="tabs">
    <div class="tab active" onclick="switchTab('models')">📊 Models</div>
    <div class="tab" onclick="switchTab('skills')">🛠 Skills</div>
    <div class="tab" onclick="switchTab('hiring')">👔 Hiring</div>
  </div>

  <!-- ═══ MODELS TAB ═══ -->
  <div id="tab-models" class="tab-panel active">

    <div class="card">
      <div class="section-title">Model Comparison — Task Scores &amp; Pricing</div>
      <div class="filters" id="provider-filters">
        {provider_btns}
      </div>
      <table id="models-table">
        <thead>
          <tr>
            <th>Model</th><th>Provider</th><th>Adapter</th>
            <th>$/1M in</th><th>$/1M out</th>
            {score_headers}
            <th>Notes</th>
          </tr>
        </thead>
        <tbody id="models-body">
          {model_rows}
        </tbody>
      </table>
      <p style="font-size:0.75em;color:#94a3b8;margin-top:10px">
        Score legend: <span style="background:#bbf7d0;padding:1px 6px;border-radius:4px">9–10 excellent</span>
        <span style="background:#d9f99d;padding:1px 6px;border-radius:4px">7–8 good</span>
        <span style="background:#fef9c3;padding:1px 6px;border-radius:4px">5–6 adequate</span>
        <span style="background:#fed7aa;padding:1px 6px;border-radius:4px">3–4 limited</span>
        <span style="background:#fecaca;padding:1px 6px;border-radius:4px">1–2 poor</span>
      </p>
    </div>

    <div class="card">
      <div class="section-title">Position Recommendations — Best-fit Model per Role</div>
      <table>
        <thead>
          <tr><th>Position</th><th>Current Model</th><th>Top 5 Candidates (score-coloured — green=excellent, yellow=good, orange=adequate)</th><th>Status</th></tr>
        </thead>
        <tbody>
          {pos_rec_rows}
        </tbody>
      </table>
    </div>

    <details style="background:white;border:1px solid #e2e8f0;border-radius:8px;padding:12px 18px;margin-bottom:20px">
      <summary>Research Notes</summary>
      <div style="margin-top:10px">{notes_html or '<p style="color:#94a3b8;font-size:0.85em">No research notes yet.</p>'}</div>
    </details>
  </div>

  <!-- ═══ SKILLS TAB ═══ -->
  <div id="tab-skills" class="tab-panel">
    <div class="card">
      <div class="section-title">Skills Gap Analysis — All 21 Positions</div>
      <p style="font-size:0.82em;color:#64748b;margin-bottom:12px">
        <span class="skill-chip installed">●</span> Installed &nbsp;
        <span class="skill-chip pending">●</span> Pending vet/install &nbsp;
        <span class="skill-chip mcp">●</span> MCP tools &nbsp;
        Gap % = installed ÷ total required
      </p>
      <table>
        <thead>
          <tr><th>Position</th><th>Installed Skills</th><th>Pending / Custom Build</th><th>MCP Tools</th><th>Gap %</th></tr>
        </thead>
        <tbody>
          {skills_rows or '<tr><td colspan="5" style="color:#94a3b8;text-align:center;padding:20px">SKILLS.md files not yet in new format. Run WS4B to expand them.</td></tr>'}
        </tbody>
      </table>
    </div>

    <div class="card">
      <div class="section-title">Skill Sources</div>
      <table>
        <thead><tr><th>Source</th><th>URL</th><th>Best for</th></tr></thead>
        <tbody>
          <tr><td>Official Anthropic skills</td><td><code>github.com/anthropics/skills</code></td><td>pdf, xlsx, pptx, docx, webapp-testing — all agents</td></tr>
          <tr><td>C-Level Advisory (34 skills)</td><td><code>github.com/alirezarezvani/claude-skills</code></td><td>CEO, COO, CTO — executive frameworks</td></tr>
          <tr><td>Marketing (45 skills)</td><td><code>github.com/alirezarezvani/claude-skills</code></td><td>Content Lead — copy, SEO, campaigns</td></tr>
          <tr><td>Engineering (129 skills)</td><td><code>github.com/wshobson/agents</code></td><td>CTO, Senior Engineer, Engineer, QA Bot</td></tr>
          <tr><td>MCP servers</td><td><code>github.com/modelcontextprotocol/servers</code></td><td>GitHub, Google Workspace, Sequential Thinking</td></tr>
          <tr><td>Google Workspace MCP</td><td><code>workspacemcp.com</code></td><td>CEO, COO, Content Lead, TravelAgent — Gmail+Calendar</td></tr>
          <tr><td>agentskills.io specification</td><td><code>agentskills.io/specification</code></td><td>SKILL.md format reference</td></tr>
        </tbody>
      </table>
    </div>
  </div>

  <!-- ═══ HIRING TAB ═══ -->
  <div id="tab-hiring" class="tab-panel">
    <div class="hire-bar">
      <span>Last hiring round: <strong>run <code>python update_llm_matrix.py --hire</code> to see full report</strong></span>
      <span style="margin-left:auto;color:#94a3b8;font-size:0.8em">Emergency slot is always gemma4:26b (availability guarantee, not merit)</span>
    </div>

    <div class="card">
      <div class="section-title">Current Rankings — Primary, Fallback 1, Fallback 2 by Position</div>
      <table>
        <thead>
          <tr><th>Position</th><th>Current</th><th>Primary (best)</th><th>Fallback 1</th><th>Fallback 2</th><th>Flags</th><th>Status</th></tr>
        </thead>
        <tbody>
          {hiring_rows}
        </tbody>
      </table>
    </div>

    <div class="card">
      <div class="section-title">How the Hiring Algorithm Works</div>
      <p style="font-size:0.85em;color:#475569;line-height:1.6">
        Each position has a <strong>task weight profile</strong> in <code>llm-matrix-data.json</code> (e.g. CEO = 30% reasoning, 25% research, 20% writing...).
        The algorithm scores every model by computing <em>sum(task_score × weight)</em> across all task dimensions.
        The highest-scoring model becomes the recommended Primary; next two become Fallback 1 and Fallback 2.
        Emergency is always <strong>gemma4:26b</strong> — it is the always-available local fallback regardless of score.
        <br><br>
        Local-only positions (Doc, Freud, Council Local) only consider models where <code>local_only: true</code>.
        If a better model is released or pricing drops significantly, re-run <code>--hire</code> to see if lineup changes are warranted.
        <br><br>
        <strong>Greg approves all changes</strong> — the algorithm recommends, Greg decides, <code>position_manager.py sub</code> applies.
      </p>
    </div>
  </div>

  <p style="font-size:0.75em;color:#94a3b8;margin-top:24px">
    LLM Matrix &bull; Life Admin &bull; Generated {now}
  </p>

  <script>
    function switchTab(name) {{
      document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
      document.querySelectorAll('.tab-panel').forEach(p => p.classList.remove('active'));
      document.getElementById('tab-' + name).classList.add('active');
      event.target.classList.add('active');
    }}

    function filterProvider(provider) {{
      document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
      event.target.classList.add('active');
      document.querySelectorAll('#models-body tr').forEach(row => {{
        if (provider === 'all' || row.dataset.provider === provider) {{
          row.style.display = '';
        }} else {{
          row.style.display = 'none';
        }}
      }});
    }}
  </script>
</body>
</html>"""

    with open(HTML_FILE, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"Dashboard written to {HTML_FILE}")

# ─── Entry point ──────────────────────────────────────────────────────────────

def main():
    args = sys.argv[1:]

    if "--stale" in args:
        cmd_stale()
    elif "--research" in args:
        cmd_research()
    elif "--skills" in args:
        cmd_skills()
    elif "--hire" in args:
        cmd_hire()
    else:
        generate_html()
        print("Done.")
        if "--open" in args:
            webbrowser.open(str(HTML_FILE))

if __name__ == "__main__":
    main()
