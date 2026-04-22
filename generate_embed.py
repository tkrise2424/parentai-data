#!/usr/bin/env python3
"""
generate_embed.py
Reads trending.json and writes a fresh embed.html for Squarespace.
Run this script as part of the weekly ParentAI report workflow.
"""
import json, sys
from datetime import datetime
from pathlib import Path

def generate_embed_html(data):
    rankings = data.get("rankings", [])
    all_time = data.get("all_time", {})
    word_cloud = data.get("word_cloud", [])
    total_convos = all_time.get("total_conversations", 0)
    generated_at = data.get("generated_at", "")
    try:
        dt = datetime.fromisoformat(generated_at)
        updated_label = dt.strftime("%B %-d, %Y")
    except Exception:
        updated_label = generated_at

    ACCENT_COLORS = ["#da3c77", "#1b5f7a", "#10c2a9"]

    # Word cloud
    word_cloud_items = ""
    for i, w in enumerate(word_cloud):
        size = max(14, min(52, 14 + int(w["weight"] * 4.2)))
        color = w.get("color", ACCENT_COLORS[i % 3])
        opacity = round(max(0.7, 1.0 - (i * 0.03)), 2)
        weight = "800" if size > 30 else "700"
        word_cloud_items += (
            f'<span class="pai-ww" style="font-size:{size}px;font-weight:{weight};'
            f'color:{color};opacity:{opacity};display:inline-block;margin:6px 10px;line-height:1.2;'
            f'cursor:default;transition:transform 0.15s;" '
            f'onmouseover="this.style.transform=\'scale(1.12)\'" '
            f'onmouseout="this.style.transform=\'scale(1)\'">{w["word"]}</span>\n'
        )

    # Rank cards
    rank_cards = ""
    for r in rankings:
        rank = r.get("rank", 0)
        accent = r.get("accent", "#1b5f7a")
        tags_html = "".join(
            f'<span style="display:inline-block;font-size:10px;font-weight:600;padding:3px 10px;'
            f'border-radius:20px;background:{accent};color:#fff;opacity:0.85;margin:2px 3px 2px 0;">{t}</span>'
            for t in r.get("tags", [])
        )
        medal = "#f4c542" if rank == 1 else "#a8a8a8" if rank == 2 else "#cd7f32" if rank == 3 else "#ccc"
        rank_cards += f"""
        <div style="display:flex;align-items:flex-start;gap:12px;background:#fff;border-radius:14px;
                    padding:16px 18px;box-shadow:0 2px 10px rgba(0,0,0,0.06);
                    border-left:4px solid {accent};margin-bottom:0;">
          <div style="font-size:18px;font-weight:900;color:{medal};min-width:26px;text-align:center;padding-top:2px;">#{rank}</div>
          <div style="font-size:24px;min-width:32px;text-align:center;">{r.get("emoji","")}</div>
          <div style="flex:1;">
            <div style="font-size:14px;font-weight:700;color:#1a1a2e;margin-bottom:3px;">{r.get("title","")}</div>
            <div style="font-size:11px;color:#888;margin-bottom:6px;line-height:1.4;">{r.get("description","")}</div>
            <div>{tags_html}</div>
          </div>
          <div style="text-align:right;min-width:58px;">
            <div style="font-size:20px;font-weight:800;color:#1a1a2e;">{r.get("pct",0)}%</div>
            <div style="font-size:11px;color:#aaa;">{r.get("count",0)} conv.</div>
          </div>
        </div>"""

    return f'''<!-- ParentAI Trending Topics Widget - Generated {updated_label} -->
<!-- Paste into Squarespace Code Block -->
<style>
#pai-wrap{{font-family:'Helvetica Neue',Helvetica,Arial,sans-serif;max-width:1100px;margin:0 auto;padding:40px 20px;box-sizing:border-box;}}
#pai-wrap *{{box-sizing:border-box;}}
.pai-grid{{display:grid;grid-template-columns:1fr 1fr;gap:12px;}}
@media(max-width:680px){{
  .pai-grid{{grid-template-columns:1fr!important;}}
  #pai-wrap h2{{font-size:28px!important;}}
  .pai-ww{{font-size:16px!important;margin:4px 5px!important;}}
  #pai-wrap div[style*="padding:36px"]{{padding:20px 12px!important;}}
}}
</style>
<div id="pai-wrap">
  <div style="text-align:center;margin-bottom:44px;">
    <div style="display:inline-block;background:linear-gradient(135deg,#da3c77,#1b5f7a,#10c2a9);border-radius:50px;padding:8px 26px;margin-bottom:18px;">
      <span style="color:#fff;font-size:13px;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;">Live Insights</span>
    </div>
    <h2 style="font-size:42px;font-weight:800;color:#1b5f7a;margin:0 0 12px;line-height:1.15;">What Parents Are Asking</h2>
    <p style="font-size:18px;color:#888;margin:0;">Trending topics from real ParentAI conversations &middot; Updated weekly</p>
  </div>
  <div style="background:linear-gradient(135deg,#fdf4f8,#f0faf9);border-radius:20px;padding:36px 28px;margin-bottom:40px;text-align:center;border:1px solid #f0e0e8;">
    <div style="font-size:13px;font-weight:700;color:#da3c77;letter-spacing:1.5px;text-transform:uppercase;margin-bottom:16px;">&#128269; Conversation Word Cloud</div>
    <div style="line-height:2;overflow-wrap:break-word;word-break:break-word;">
{word_cloud_items}    </div>
  </div>
  <div style="display:flex;gap:16px;margin-bottom:40px;flex-wrap:wrap;">
    <div style="flex:1;min-width:140px;background:#fff;border-radius:14px;padding:20px;box-shadow:0 2px 10px rgba(0,0,0,0.06);text-align:center;">
      <div style="font-size:36px;font-weight:900;color:#1b5f7a;">{total_convos}</div>
      <div style="font-size:11px;color:#aaa;font-weight:600;text-transform:uppercase;letter-spacing:0.8px;margin-top:4px;">Total Conversations</div>
    </div>
    <div style="flex:1;min-width:140px;background:#fff;border-radius:14px;padding:20px;box-shadow:0 2px 10px rgba(0,0,0,0.06);text-align:center;">
      <div style="font-size:36px;font-weight:900;color:#da3c77;">{len(rankings)}</div>
      <div style="font-size:11px;color:#aaa;font-weight:600;text-transform:uppercase;letter-spacing:0.8px;margin-top:4px;">Topic Categories</div>
    </div>
  </div>
  <div style="font-size:13px;font-weight:700;color:#888;letter-spacing:1.2px;text-transform:uppercase;margin-bottom:16px;">&#127942; Top Topics — All Time</div>
  <div class="pai-grid">
{rank_cards}
  </div>
  <div style="text-align:center;font-size:11px;color:#ccc;padding-top:24px;">Updated {updated_label} &middot; ParentAI</div>
</div>'''

if __name__ == "__main__":
    src = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("trending.json")
    out = Path(sys.argv[2]) if len(sys.argv) > 2 else Path("embed.html")
    data = json.loads(src.read_text())
    out.write_text(generate_embed_html(data))
    print(f"embed.html written from {src}")
