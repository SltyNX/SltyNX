#!/usr/bin/env python3
"""
Generates Hero Banner, SltyNX Brand Logo, Telegram Contact Button, and Footer SVGs:
- assets/sltynx-logo.svg
- assets/hero.svg
- assets/telegram-button.svg
- assets/footer.svg
Also ensures assets/hero-fallback.png and assets/profile-avatar.png exist.
"""
from __future__ import annotations
from html import escape
import pathlib
import struct
import zlib

import config as C


def build_sltynx_logo() -> str:
    """
    Builds assets/sltynx-logo.svg:
    Clean, scalable monochrome white vector reproduction of Asset B on pure #000000.
    Also serves as the static fallback for the dot-matrix name simulator.
    """
    w, h = 560, 230
    emblem = C.render_brand_emblem_svg(cx=w / 2.0, top_y=28.0, scale=0.95)
    # Wordmark width at scale 0.82 is ~400px -> start_x = (560 - 400)/2 = 80
    wordmark = C.render_geometric_wordmark_svg(start_x=80.0, top_y=124.0, scale=0.82)

    return f'''<svg {C.SVG_NS} viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="SLYTNX monochrome emblem and wordmark">
  <title>SLYTNX Brand Logo</title>
  <rect x="0" y="0" width="{w}" height="{h}" fill="{C.BG_PRIMARY}"/>
  <rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="6" fill="none" stroke="{C.BORDER}" stroke-width="1"/>
  {emblem}
  {wordmark}
</svg>
'''


def _render_hero_dot_wordmark(start_x: float, start_y: float, dot_size: float = 4.2, pitch: float = 5.6) -> str:
    """
    Renders SLYTNX on the left side of the hero banner using discrete square dots
    (11 rows x 9 cols per letter) so each letter is genuinely formed from square pixels.
    """
    rects: list[str] = []
    word = "SLYTNX"
    letter_w = 9 * pitch
    letter_gap = 2.2 * pitch

    for li, ch in enumerate(word):
        grid = C.DOT_LETTERS[ch]
        lx = start_x + li * (letter_w + letter_gap)
        for r, row in enumerate(grid):
            for c, cell in enumerate(row):
                dx = lx + c * pitch
                dy = start_y + r * pitch
                if cell == "#":
                    delay = (li * 0.15 + r * 0.03) % 2.0
                    rects.append(
                        f'<rect x="{dx:.1f}" y="{dy:.1f}" width="{dot_size:.1f}" height="{dot_size:.1f}" '
                        f'fill="{C.TEXT_PRIMARY}" class="hdot" style="animation-delay:{delay:.2f}s"/>'
                    )
                else:
                    rects.append(
                        f'<rect x="{dx:.1f}" y="{dy:.1f}" width="{dot_size:.1f}" height="{dot_size:.1f}" '
                        f'fill="{C.BG_DOT_IDLE}"/>'
                    )
    return '<g class="hero-dot-wordmark">' + "".join(rects) + "</g>"


def build_hero() -> str:
    """
    Builds assets/hero.svg (880x310):
    Left side:
      - Triangular SltyNX emblem + discrete dot-matrix SLYTNX wordmark
      - Subtitle: sleep > code > repeat
      - Secondary terminal details: Sleeping Core, status: sleeping..., clock [03:14 AM],
        blinking cursor, crescent moon & sleeping-cat doodle.
    Right side:
      - Continuous 16s seamless looping animation of the sleepy mascot walking toward the bed,
        climbing onto the mattress, lying down on the pillow, pulling the blanket up, closing
        its eyes, breathing subtly, and emitting floating pixel Z / Zz / Zzz effects,
        preserving the likeness and scene from Asset A (sleepy-mascot.jpg).
    """
    w, h = 880, 310
    sleepy_b64 = C.get_asset_base64("sleepy-mascot.jpg")
    bg_img_tag = ""
    if sleepy_b64:
        # Subtle dark-blended reference vignette inside the bed frame during the sleeping phase
        bg_img_tag = (
            f'<image href="data:image/jpeg;base64,{sleepy_b64}" '
            f'x="472" y="48" width="372" height="222" preserveAspectRatio="xMidYMid slice" '
            f'clip-path="url(#bedSceneClip)" opacity="0.24" class="ref-vignette"/>'
        )

    emblem_left = C.render_brand_emblem_svg(cx=64.0, top_y=64.0, scale=0.68)
    dot_wordmark = _render_hero_dot_wordmark(start_x=108.0, start_y=76.0, dot_size=3.6, pitch=4.8)

    return f'''<svg {C.SVG_NS} viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="SltyNX Hero Banner — sleep, code, repeat">
  <title>SltyNX — Sleeping Core (sleep &gt; code &gt; repeat)</title>
  <defs>
    <clipPath id="bedSceneClip">
      <rect x="472" y="48" width="372" height="222" rx="6"/>
    </clipPath>
  </defs>
  <style>
    .mono {{ font-family: {C.FONT_MONO}; }}
    .sans {{ font-family: {C.FONT_SANS}; }}
    .cur {{ animation: blink 1.1s steps(1) infinite; }}
    @keyframes blink {{ 0%, 49% {{ opacity: 1; }} 50%, 100% {{ opacity: 0; }} }}

    .hdot {{ animation: dotPulse 6s ease-in-out infinite; }}
    @keyframes dotPulse {{
      0%, 85%, 100% {{ fill: {C.TEXT_PRIMARY}; opacity: 1; }}
      92% {{ fill: #BDBDBD; opacity: 0.78; }}
    }}

    /* 16s seamless mascot bedtime loop:
       0% - 14%: Walk/shuffle toward bed
       14% - 25%: Climb onto mattress
       25% - 36%: Lie down on pillow and pull up blanket
       36% - 88%: Sleep with closed eyes, subtle breathing and floating Zzz
       88% - 100%: Rest and smooth fade transition
    */
    .phase-walk {{ animation: walkCycle 16s linear infinite; }}
    @keyframes walkCycle {{
      0% {{ opacity: 0; transform: translate(0px, 0px); }}
      3% {{ opacity: 1; transform: translate(6px, -2px); }}
      6% {{ opacity: 1; transform: translate(20px, 0px); }}
      9% {{ opacity: 1; transform: translate(35px, -2px); }}
      12% {{ opacity: 1; transform: translate(50px, 0px); }}
      14% {{ opacity: 1; transform: translate(58px, -1px); }}
      15%, 100% {{ opacity: 0; transform: translate(58px, -1px); }}
    }}

    .phase-climb {{ animation: climbCycle 16s linear infinite; }}
    @keyframes climbCycle {{
      0%, 13.9% {{ opacity: 0; transform: translate(0px, 0px); }}
      14% {{ opacity: 1; transform: translate(0px, 0px); }}
      18% {{ opacity: 1; transform: translate(22px, -18px); }}
      22% {{ opacity: 1; transform: translate(44px, -28px); }}
      25% {{ opacity: 1; transform: translate(54px, -24px); }}
      26%, 100% {{ opacity: 0; transform: translate(54px, -24px); }}
    }}

    .phase-settle {{ animation: settleCycle 16s linear infinite; }}
    @keyframes settleCycle {{
      0%, 24.9% {{ opacity: 0; }}
      25% {{ opacity: 1; }}
      35% {{ opacity: 1; }}
      36%, 100% {{ opacity: 0; }}
    }}

    .phase-sleep {{ animation: sleepCycle 16s linear infinite; }}
    @keyframes sleepCycle {{
      0%, 34.9% {{ opacity: 0; }}
      36%, 92% {{ opacity: 1; }}
      98%, 100% {{ opacity: 0; }}
    }}

    .breathe {{ animation: chestBreathe 3.2s ease-in-out infinite; }}
    @keyframes chestBreathe {{
      0%, 100% {{ transform: translateY(0px); }}
      50% {{ transform: translateY(-1.8px); }}
    }}

    .blanket-pull {{ animation: blanketUp 16s ease-in-out infinite; }}
    @keyframes blanketUp {{
      0%, 25% {{ transform: translate(16px, 14px); }}
      35%, 92% {{ transform: translate(0px, 0px); }}
      98%, 100% {{ transform: translate(16px, 14px); }}
    }}

    .z1 {{ animation: floatZ1 16s linear infinite; }}
    .z2 {{ animation: floatZ2 16s linear infinite; }}
    .z3 {{ animation: floatZ3 16s linear infinite; }}
    @keyframes floatZ1 {{
      0%, 38% {{ opacity: 0; transform: translate(0px, 0px); }}
      43% {{ opacity: 0.9; transform: translate(4px, -10px); }}
      55% {{ opacity: 0; transform: translate(10px, -28px); }}
      62% {{ opacity: 0; transform: translate(0px, 0px); }}
      67% {{ opacity: 0.9; transform: translate(4px, -10px); }}
      80% {{ opacity: 0; transform: translate(10px, -28px); }}
      100% {{ opacity: 0; }}
    }}
    @keyframes floatZ2 {{
      0%, 42% {{ opacity: 0; transform: translate(0px, 0px); }}
      48% {{ opacity: 0.85; transform: translate(6px, -12px); }}
      60% {{ opacity: 0; transform: translate(14px, -32px); }}
      66% {{ opacity: 0; transform: translate(0px, 0px); }}
      72% {{ opacity: 0.85; transform: translate(6px, -12px); }}
      85% {{ opacity: 0; transform: translate(14px, -32px); }}
      100% {{ opacity: 0; }}
    }}
    @keyframes floatZ3 {{
      0%, 46% {{ opacity: 0; transform: translate(0px, 0px); }}
      53% {{ opacity: 0.95; transform: translate(8px, -14px); }}
      66% {{ opacity: 0; transform: translate(18px, -38px); }}
      70% {{ opacity: 0; transform: translate(0px, 0px); }}
      77% {{ opacity: 0.95; transform: translate(8px, -14px); }}
      90% {{ opacity: 0; transform: translate(18px, -38px); }}
      100% {{ opacity: 0; }}
    }}

    .phone-glow {{ animation: phonePulse 4s ease-in-out infinite; }}
    @keyframes phonePulse {{
      0%, 100% {{ opacity: 0.65; }}
      50% {{ opacity: 0.95; }}
    }}

    @media (prefers-reduced-motion: reduce) {{
      .phase-walk, .phase-climb, .phase-settle {{ display: none !important; }}
      .phase-sleep {{ opacity: 1 !important; animation: none !important; }}
      .blanket-pull, .breathe, .hdot, .cur, .phone-glow {{ animation: none !important; }}
      .z1, .z2, .z3 {{ animation: none !important; opacity: 0.85 !important; }}
    }}
  </style>

  <!-- Outer Pure Black Canvas & Crisp 1px Terminal Border -->
  <rect x="0" y="0" width="{w}" height="{h}" rx="8" fill="{C.BG_PRIMARY}"/>
  <rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="7" fill="none" stroke="{C.BORDER}" stroke-width="1"/>

  <!-- Top Terminal Bar -->
  <rect x="1.5" y="1.5" width="{w - 3}" height="32" rx="6" fill="{C.BG_SECONDARY}"/>
  <line x1="1" y1="34" x2="{w - 1}" y2="34" stroke="{C.BORDER}" stroke-width="1"/>
  <circle cx="20" cy="17.5" r="4" fill="{C.TEXT_DIM}"/>
  <circle cx="34" cy="17.5" r="4" fill="{C.TEXT_DIM}"/>
  <circle cx="48" cy="17.5" r="4" fill="{C.TEXT_DIM}"/>
  <text x="68" y="22" class="mono" font-size="11.5" fill="{C.TEXT_SECONDARY}">sltynx@sleeping-core: ~/profile</text>

  <!-- Top-Right Clock & Moon Indicator -->
  <g transform="translate(738, 10)">
    <!-- Tiny Crescent Moon Doodle -->
    <path d="M 10 2 A 6.5 6.5 0 1 0 16 12.5 A 5.2 5.2 0 1 1 10 2 Z" fill="{C.TEXT_SECONDARY}"/>
    <rect x="22" y="4" width="1.5" height="1.5" fill="{C.TEXT_MUTED}"/>
    <rect x="26" y="9" width="1.5" height="1.5" fill="{C.TEXT_MUTED}"/>
    <text x="34" y="12" class="mono" font-size="11" fill="{C.TEXT_SECONDARY}">[{escape(C.HERO_CLOCK)}]</text>
  </g>

  <!-- ===================================================================== -->
  <!-- LEFT SIDE: Emblem, Dot-Matrix Wordmark, Tagline & Terminal Metadata   -->
  <!-- ===================================================================== -->
  {emblem_left}
  {dot_wordmark}

  <!-- Divider under wordmark -->
  <line x1="34" y1="154" x2="432" y2="154" stroke="{C.BORDER}" stroke-width="1"/>

  <!-- Tagline: sleep > code > repeat -->
  <text x="34" y="182" class="mono" font-size="16" font-weight="600" fill="{C.TEXT_PRIMARY}" letter-spacing="1.2">{escape(C.HERO_TAGLINE)}</text>

  <!-- Secondary Terminal Status Badges -->
  <rect x="34" y="202" width="136" height="26" rx="4" fill="{C.BG_SECONDARY}" stroke="{C.BORDER}" stroke-width="1"/>
  <circle cx="48" cy="215" r="3.5" fill="{C.TEXT_PRIMARY}"/>
  <text x="60" y="219" class="mono" font-size="12" fill="{C.TEXT_PRIMARY}">{escape(C.BIO)}</text>

  <rect x="180" y="202" width="184" height="26" rx="4" fill="{C.BG_SECONDARY}" stroke="{C.BORDER}" stroke-width="1"/>
  <text x="192" y="219" class="mono" font-size="12" fill="{C.TEXT_SECONDARY}">{escape(C.HERO_STATUS)}</text>
  <rect x="336" y="208" width="7" height="13" fill="{C.TEXT_PRIMARY}" class="cur"/>

  <!-- Bottom-Left Terminal Note & Tiny Sleeping Cat Doodle -->
  <text x="34" y="258" class="mono" font-size="11.5" fill="{C.TEXT_MUTED}">// low-energy mode enabled &#8226; learning step by step</text>
  <g transform="translate(34, 268)" stroke="{C.TEXT_MUTED}" stroke-width="1.2" fill="none">
    <!-- Tiny sleeping cat curled up on desk corner -->
    <path d="M 2 14 C 2 6, 22 6, 22 14 Z" fill="{C.BG_SECONDARY}"/>
    <path d="M 5 8 L 3 3 L 8 6 M 19 8 L 21 3 L 16 6"/>
    <path d="M 22 13 C 27 13, 28 9, 25 8"/>
    <text x="34" y="13" class="mono" font-size="10.5" fill="{C.TEXT_MUTED}" stroke="none">cat: also asleep</text>
  </g>

  <!-- Vertical Panel Separator -->
  <line x1="454" y1="34" x2="454" y2="309" stroke="{C.BORDER}" stroke-width="1"/>

  <!-- ===================================================================== -->
  <!-- RIGHT SIDE: Animated Sleepy Mascot Bedroom Scene (472..844, 48..270)  -->
  <!-- ===================================================================== -->
  <rect x="472" y="48" width="372" height="222" rx="6" fill="{C.BG_SECONDARY}" stroke="{C.BORDER}" stroke-width="1"/>
  {bg_img_tag}

  <g clip-path="url(#bedSceneClip)">
    <!-- Night Window & Moon in Bedroom Background -->
    <rect x="492" y="62" width="64" height="74" rx="2" fill="#050505" stroke="{C.BORDER}" stroke-width="1"/>
    <line x1="524" y1="62" x2="524" y2="136" stroke="{C.BORDER_SUBTLE}" stroke-width="1"/>
    <line x1="492" y1="99" x2="556" y2="99" stroke="{C.BORDER_SUBTLE}" stroke-width="1"/>
    <path d="M 536 74 A 7 7 0 1 0 543 84 A 5.5 5.5 0 1 1 536 74 Z" fill="{C.TEXT_SECONDARY}" opacity="0.7"/>
    <rect x="504" y="76" width="2" height="2" fill="{C.TEXT_MUTED}"/>
    <rect x="512" y="112" width="2" height="2" fill="{C.TEXT_MUTED}"/>

    <!-- Isometric/Angled Bed Frame & Bookshelf Headboard (matching Asset A) -->
    <!-- Headboard with stacked books -->
    <polygon points="590,115 745,68 745,108 590,155" fill="#0E0E0E" stroke="{C.BORDER}" stroke-width="1.2"/>
    <!-- Books on headboard shelf -->
    <rect x="612" y="102" width="22" height="14" transform="skewY(-16)" fill="#181818" stroke="{C.BORDER}" stroke-width="1"/>
    <rect x="615" y="96" width="20" height="7" transform="skewY(-16)" fill="#222222" stroke="{C.BORDER}" stroke-width="1"/>
    <line x1="685" y1="88" x2="685" y2="112" stroke="{C.BORDER}" stroke-width="2"/>
    <line x1="691" y1="86" x2="691" y2="110" stroke="{C.TEXT_MUTED}" stroke-width="2"/>
    <line x1="697" y1="84" x2="697" y2="108" stroke="{C.BORDER}" stroke-width="2"/>

    <!-- Mattress Surface -->
    <polygon points="580,152 745,102 836,196 664,258" fill="#0B0B0B" stroke="{C.BORDER}" stroke-width="1.4"/>
    <!-- Mattress Side Depth -->
    <polygon points="580,152 664,258 664,274 580,168" fill="#060606" stroke="{C.BORDER}" stroke-width="1.2"/>

    <!-- Soft Rectangular Pillow on Mattress -->
    <polygon points="642,140 722,114 748,144 668,172" rx="6" fill="#161616" stroke="{C.TEXT_MUTED}" stroke-width="1.2"/>

    <!-- Glowing Smartphone next to Pillow (Directly from Asset A!) -->
    <g class="phone-glow">
      <polygon points="614,174 632,166 644,182 626,190" fill="#1F1F1F" stroke="{C.TEXT_SECONDARY}" stroke-width="1"/>
      <polygon points="617,175 631,169 640,181 626,187" fill="#D8D8D8"/>
      <circle cx="632" cy="182" r="1.3" fill="{C.BG_PRIMARY}"/>
    </g>

    <!-- =============================================================== -->
    <!-- PHASE 1 (0% - 14%): Mascot Walking / Shuffling Toward the Bed   -->
    <!-- =============================================================== -->
    <g class="phase-walk">
      <!-- Shadow -->
      <ellipse cx="500" cy="236" rx="16" ry="5" fill="#050505"/>
      <!-- Legs shuffling -->
      <rect x="492" y="216" width="6" height="16" rx="2" fill="#1C1C1C" stroke="{C.TEXT_MUTED}" stroke-width="1"/>
      <rect x="502" y="214" width="6" height="16" rx="2" fill="#1C1C1C" stroke="{C.TEXT_MUTED}" stroke-width="1"/>
      <!-- Pajama Torso -->
      <rect x="488" y="190" width="24" height="28" rx="5" fill="#242424" stroke="{C.TEXT_SECONDARY}" stroke-width="1.2"/>
      <!-- Droopy Arms -->
      <rect x="483" y="194" width="6" height="18" rx="3" fill="#242424" stroke="{C.TEXT_SECONDARY}" stroke-width="1"/>
      <rect x="511" y="194" width="6" height="18" rx="3" fill="#242424" stroke="{C.TEXT_SECONDARY}" stroke-width="1"/>
      <!-- Chibi Head & Dark Hair -->
      <circle cx="500" cy="172" r="18" fill="#E5E5E5" stroke="{C.BORDER}" stroke-width="1.2"/>
      <path d="M 481 172 C 481 150, 519 150, 519 172 C 515 162, 505 165, 498 168 L 494 162 L 488 170 Z" fill="#1A1A1A" stroke="{C.TEXT_MUTED}" stroke-width="1"/>
      <!-- Half-closed sleepy eye -->
      <line x1="504" y1="175" x2="512" y2="175" stroke="{C.BG_PRIMARY}" stroke-width="2" stroke-linecap="round"/>
    </g>

    <!-- =============================================================== -->
    <!-- PHASE 2 (14% - 25%): Mascot Climbing Onto the Bed               -->
    <!-- =============================================================== -->
    <g class="phase-climb">
      <g transform="translate(558, 198) rotate(14)">
        <rect x="-10" y="14" width="7" height="14" rx="2" fill="#1C1C1C" stroke="{C.TEXT_MUTED}" stroke-width="1"/>
        <rect x="2" y="10" width="7" height="14" rx="2" fill="#1C1C1C" stroke="{C.TEXT_MUTED}" stroke-width="1"/>
        <rect x="-12" y="-10" width="24" height="26" rx="5" fill="#242424" stroke="{C.TEXT_SECONDARY}" stroke-width="1.2"/>
        <circle cx="0" cy="-26" r="17" fill="#E5E5E5" stroke="{C.BORDER}" stroke-width="1.2"/>
        <path d="M -17 -26 C -17 -46, 17 -46, 17 -26 C 12 -34, 2 -32, -4 -28 Z" fill="#1A1A1A" stroke="{C.TEXT_MUTED}" stroke-width="1"/>
        <line x1="3" y1="-23" x2="10" y2="-23" stroke="{C.BG_PRIMARY}" stroke-width="2" stroke-linecap="round"/>
      </g>
    </g>

    <!-- =============================================================== -->
    <!-- PHASE 3 (25% - 36%): Mascot Settling onto Pillow                -->
    <!-- =============================================================== -->
    <g class="phase-settle">
      <g transform="translate(698, 154)">
        <!-- Pajama Pants -->
        <path d="M 10 22 L 24 44 L 32 40 L 24 18 L 38 32 L 46 26 L 26 8 Z" fill="#171717" stroke="{C.TEXT_MUTED}" stroke-width="1.2"/>
        <!-- Pajama Top -->
        <polygon points="-14,6 16,-6 32,18 2,30" rx="5" fill="#262626" stroke="{C.TEXT_SECONDARY}" stroke-width="1.2"/>
        <!-- Arms reaching for blanket -->
        <rect x="-24" y="10" width="14" height="7" rx="3" fill="#262626" stroke="{C.TEXT_SECONDARY}" stroke-width="1"/>
        <rect x="14" y="-12" width="14" height="7" rx="3" fill="#262626" stroke="{C.TEXT_SECONDARY}" stroke-width="1"/>
        <!-- Head on Pillow -->
        <circle cx="-12" cy="-10" r="22" fill="#E5E5E5" stroke="{C.BORDER}" stroke-width="1.2"/>
        <path d="M -34 -12 C -34 -38, 10 -38, 10 -10 C 6 -2, 0 -6, -4 -10 L -10 -2 L -16 -12 L -24 -4 Z" fill="#1A1A1A" stroke="{C.TEXT_MUTED}" stroke-width="1.1"/>
        <line x1="-18" y1="-3" x2="-9" y2="-4" stroke="{C.BG_PRIMARY}" stroke-width="2.2" stroke-linecap="round"/>
      </g>
    </g>

    <!-- =============================================================== -->
    <!-- PHASE 4 (36% - 92%): Sleeping on Pillow + Breathing + Zzz       -->
    <!-- Matches the exact pose of 121597258683948101.jpg!               -->
    <!-- =============================================================== -->
    <g class="phase-sleep">
      <g transform="translate(698, 154)">
        <!-- Sprawled Legs & Socks (matching Asset A pose) -->
        <path d="M 10 22 L 24 46 L 33 41 L 24 20 L 42 32 L 49 25 L 26 8 Z" fill="#171717" stroke="{C.TEXT_MUTED}" stroke-width="1.2"/>
        <circle cx="28" cy="45" r="3.5" fill="#D8D8D8"/>
        <circle cx="47" cy="29" r="3.5" fill="#D8D8D8"/>

        <!-- Breathing Torso & Outstretched Arms -->
        <g class="breathe">
          <!-- Left arm resting near pillow -->
          <rect x="-26" y="8" width="16" height="8" rx="3" transform="rotate(-12 -18 12)" fill="#262626" stroke="{C.TEXT_SECONDARY}" stroke-width="1.1"/>
          <circle cx="-27" cy="13" r="3.5" fill="#E5E5E5"/>
          <!-- Right arm outstretched -->
          <rect x="14" y="-12" width="16" height="8" rx="3" transform="rotate(-22 22 -8)" fill="#262626" stroke="{C.TEXT_SECONDARY}" stroke-width="1.1"/>
          <circle cx="30" cy="-11" r="3.5" fill="#E5E5E5"/>
          <!-- Pajama Shirt -->
          <polygon points="-14,6 16,-6 32,18 2,30" fill="#262626" stroke="{C.TEXT_SECONDARY}" stroke-width="1.2"/>
        </g>

        <!-- Chibi Head Resting on Pillow (Dark hair & peaceful closed eye line) -->
        <circle cx="-12" cy="-10" r="22" fill="#E5E5E5" stroke="{C.BORDER}" stroke-width="1.2"/>
        <!-- Layered bangs from Asset A -->
        <path d="M -34 -10 C -34 -38, 10 -38, 10 -10 C 8 0, 2 -4, -2 -8 L -8 0 L -14 -10 L -22 -2 C -28 -4, -32 -6, -34 -10 Z" fill="#1A1A1A" stroke="{C.TEXT_MUTED}" stroke-width="1.1"/>
        <!-- Peaceful closed eye line -->
        <line x1="-19" y1="-2" x2="-9" y2="-4" stroke="{C.BG_PRIMARY}" stroke-width="2.4" stroke-linecap="round"/>
      </g>

      <!-- Floating Pixel-Style Z / Zz / Zzz Animation -->
      <g class="mono" font-weight="700" fill="{C.TEXT_PRIMARY}">
        <text x="676" y="118" font-size="12" class="z1">Z</text>
        <text x="692" y="102" font-size="15" class="z2">Zz</text>
        <text x="712" y="84" font-size="18" class="z3">Zzz</text>
      </g>
    </g>

    <!-- Blanket at Foot of Bed (Pulls up gently when mascot settles) -->
    <g class="blanket-pull">
      <path d="M 654 256 C 685 215, 765 182, 834 196 L 836 268 L 664 268 Z" fill="#141414" stroke="{C.TEXT_MUTED}" stroke-width="1.3"/>
      <path d="M 684 242 C 715 218, 762 204, 808 212" fill="none" stroke="{C.BORDER}" stroke-width="1.2"/>
    </g>

    <!-- Small Scene HUD Overlay inside Bedroom Bottom-Left -->
    <rect x="482" y="238" width="154" height="22" rx="3" fill="#000000" fill-opacity="0.82" stroke="{C.BORDER}" stroke-width="1"/>
    <text x="490" y="253" class="mono" font-size="10.5" fill="{C.TEXT_SECONDARY}">scene: bedtime_loop.sh</text>
  </g>
</svg>
'''


def build_telegram_button() -> str:
    """
    Builds assets/telegram-button.svg (380x64):
    Prominent, professionally styled Telegram action button on #000000 with thin grey border,
    recognizable Telegram paper-plane icon, 'Message me on Telegram', and '@SltyNX_X'.
    """
    w, h = 380, 64
    return f'''<svg {C.SVG_NS} viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="Message me on Telegram @SltyNX_X">
  <title>{escape(C.TELEGRAM_CTA)} ({escape(C.TELEGRAM_USERNAME)})</title>
  <style>
    .mono {{ font-family: {C.FONT_MONO}; }}
    .sans {{ font-family: {C.FONT_SANS}; }}
    .border-pulse {{ animation: bPulse 4s ease-in-out infinite; }}
    @keyframes bPulse {{
      0%, 100% {{ stroke: {C.BORDER}; }}
      50% {{ stroke: {C.TEXT_SECONDARY}; }}
    }}
    @media (prefers-reduced-motion: reduce) {{
      .border-pulse {{ animation: none !important; }}
    }}
  </style>
  <rect x="0" y="0" width="{w}" height="{h}" rx="6" fill="{C.BG_PRIMARY}"/>
  <rect x="1.5" y="1.5" width="{w - 3}" height="{h - 3}" rx="5" fill="{C.BG_SECONDARY}" stroke="{C.BORDER}" stroke-width="1.2" class="border-pulse"/>

  <!-- Icon Box -->
  <rect x="14" y="12" width="40" height="40" rx="5" fill="{C.BG_ELEVATED}" stroke="{C.BORDER}" stroke-width="1"/>
  <!-- Recognizable Telegram Paper Plane Icon -->
  <g transform="translate(34, 32)">
    <path d="M -11 -1 L 10 -9 L 6 10 L 0 5.5 L -4 9 L -4 3.5 L 5 -4.5 L -6 2 Z" fill="{C.TEXT_PRIMARY}"/>
  </g>

  <!-- Primary & Secondary Text -->
  <text x="68" y="29" class="sans" font-size="14.5" font-weight="600" fill="{C.TEXT_PRIMARY}">{escape(C.TELEGRAM_CTA)}</text>
  <text x="68" y="47" class="mono" font-size="12" fill="{C.TEXT_SECONDARY}">{escape(C.TELEGRAM_USERNAME)}</text>

  <!-- Right Arrow Indicator Pill -->
  <rect x="304" y="19" width="60" height="26" rx="4" fill="{C.BG_PRIMARY}" stroke="{C.BORDER}" stroke-width="1"/>
  <text x="334" y="36" text-anchor="middle" class="mono" font-size="11.5" fill="{C.TEXT_PRIMARY}">open &#8594;</text>
</svg>
'''


def build_footer() -> str:
    """
    Builds assets/footer.svg (880x155):
    Compact closing section featuring the original triangular SltyNX emblem,
    SLYTNX, sleep • code • create, Thanks for visiting!, Still loading...,
    and a small sleeping-cat & crescent moon doodle.
    """
    w, h = 880, 155
    emblem = C.render_brand_emblem_svg(cx=w / 2.0, top_y=18.0, scale=0.46)
    return f'''<svg {C.SVG_NS} viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="SLYTNX — sleep, code, create. Thanks for visiting! Still loading...">
  <title>SLYTNX Footer — {escape(C.FOOTER_TAGLINE)}</title>
  <style>
    .mono {{ font-family: {C.FONT_MONO}; }}
    .sans {{ font-family: {C.FONT_SANS}; }}
    .cur {{ animation: blink 1.2s steps(1) infinite; }}
    @keyframes blink {{ 0%, 49% {{ opacity: 1; }} 50%, 100% {{ opacity: 0; }} }}
    @media (prefers-reduced-motion: reduce) {{ .cur {{ animation: none !important; }} }}
  </style>
  <rect x="0" y="0" width="{w}" height="{h}" rx="6" fill="{C.BG_PRIMARY}"/>
  <line x1="24" y1="2" x2="{w - 24}" y2="2" stroke="{C.BORDER}" stroke-width="1"/>

  <!-- Left Crescent Moon Doodle -->
  <g transform="translate(44, 24)">
    <path d="M 12 2 A 8 8 0 1 0 20 15 A 6.5 6.5 0 1 1 12 2 Z" fill="none" stroke="{C.TEXT_MUTED}" stroke-width="1.2"/>
    <rect x="26" y="4" width="2" height="2" fill="{C.TEXT_DIM}"/>
    <rect x="32" y="12" width="1.5" height="1.5" fill="{C.TEXT_DIM}"/>
  </g>

  <!-- Centered Triangular SltyNX Emblem -->
  {emblem}

  <!-- Wordmark & Taglines -->
  <text x="{w / 2:.0f}" y="76" text-anchor="middle" class="mono" font-size="15" font-weight="700" fill="{C.TEXT_PRIMARY}" letter-spacing="4">{escape(C.FOOTER_WORDMARK)}</text>
  <text x="{w / 2:.0f}" y="96" text-anchor="middle" class="mono" font-size="12" fill="{C.TEXT_SECONDARY}" letter-spacing="1.5">{escape(C.FOOTER_TAGLINE)}</text>
  <text x="{w / 2:.0f}" y="118" text-anchor="middle" class="sans" font-size="12.5" fill="{C.TEXT_PRIMARY}">{escape(C.FOOTER_THANKS)}</text>

  <!-- Still loading... with blinking terminal cursor -->
  <text x="{w / 2 - 6:.0f}" y="138" text-anchor="middle" class="mono" font-size="11.5" fill="{C.TEXT_MUTED}">{escape(C.FOOTER_STATUS)}</text>
  <rect x="{w / 2 + 44:.0f}" y="128" width="6" height="11" fill="{C.TEXT_MUTED}" class="cur"/>

  <!-- Right Sleeping Cat Doodle -->
  <g transform="translate(806, 118)" stroke="{C.TEXT_MUTED}" stroke-width="1.2" fill="none">
    <path d="M 0 16 C 0 7, 22 7, 22 16 Z" fill="{C.BG_SECONDARY}"/>
    <path d="M 3 10 L 1 4 L 7 7 M 19 10 L 21 4 L 15 7"/>
    <text x="26" y="10" class="mono" font-size="9" fill="{C.TEXT_MUTED}" stroke="none">zZz</text>
  </g>
</svg>
'''


def _write_minimal_png_if_missing(target: pathlib.Path, width: int, height: int) -> None:
    """
    Pure-Python standard library fallback PNG writer in case a PNG fallback file
    does not yet exist on a clean environment without Pillow.
    """
    if target.exists() and target.stat().st_size > 100:
        return

    # Create a valid dark #000000 PNG with a 1px #303030 border using pure stdlib zlib/struct
    raw_rows = bytearray()
    for y in range(height):
        raw_rows.append(0)  # filter type 0
        is_border_y = y in (0, height - 1)
        for x in range(width):
            if is_border_y or x in (0, width - 1):
                raw_rows.extend((48, 48, 48))
            else:
                raw_rows.extend((0, 0, 0))

    def chunk(ctype: bytes, data: bytes) -> bytes:
        crc = zlib.crc32(ctype + data) & 0xFFFFFFFF
        return struct.pack(">I", len(data)) + ctype + data + struct.pack(">I", crc)

    ihdr = struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0)
    idat = zlib.compress(bytes(raw_rows), 9)
    png_bytes = b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", ihdr) + chunk(b"IDAT", idat) + chunk(b"IEND", b"")
    target.write_bytes(png_bytes)


def generate_all() -> dict[str, pathlib.Path]:
    C.ASSETS_DIR.mkdir(parents=True, exist_ok=True)
    outputs = {
        "sltynx-logo.svg": build_sltynx_logo(),
        "hero.svg": build_hero(),
        "telegram-button.svg": build_telegram_button(),
        "footer.svg": build_footer(),
    }
    written: dict[str, pathlib.Path] = {}
    for name, content in outputs.items():
        out_path = C.ASSETS_DIR / name
        out_path.write_text(content, encoding="utf-8")
        written[name] = out_path

    # Ensure PNG fallbacks exist
    hero_png = C.ASSETS_DIR / "hero-fallback.png"
    avatar_png = C.ASSETS_DIR / "profile-avatar.png"
    _write_minimal_png_if_missing(hero_png, 880, 310)
    _write_minimal_png_if_missing(avatar_png, 180, 180)
    written["hero-fallback.png"] = hero_png
    written["profile-avatar.png"] = avatar_png
    return written


if __name__ == "__main__":
    for k, p in generate_all().items():
        print(f"wrote {k:24s} ({p.stat().st_size:,} bytes)")
