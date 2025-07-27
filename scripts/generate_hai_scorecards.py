import math, os, hashlib, pathlib

RADIUS = 72
RING_WIDTH = 42
PLATE_RADIUS = 96
CENTER_RADIUS = 46

HUMAN = "#FFC300"
AI = "#0B2545"
TEXT_OXFORD = "#0B2545"
TEXT_WHITE = "#FFFFFF"

FRACTIONS = {0:1.00, 1:0.95, 2:0.80, 3:0.70, 4:0.60, 5:0.50, 6:0.30, 7:0.20, 8:0.10, 9:0.00}

SETS = [
    # name, plate_fill, plate_opacity, text_color, with_filters
    ("dark-translucent",  "#0F172A", 0.10, TEXT_OXFORD, True),
    ("light-translucent", "#FFFFFF", 0.14, TEXT_OXFORD, True),
    ("print-solid-light", "#E5E7EB", 1.00, TEXT_OXFORD, False),
    ("print-solid-dark",  "#1F2937", 1.00, TEXT_WHITE,  False),
]

def filters(uid, plate_alpha=0.26, donut_alpha=0.25):
    return f"""
  <filter id="f-plate-{uid}" filterUnits="userSpaceOnUse" x="-20" y="-20" width="240" height="240">
    <feOffset in="SourceAlpha" dx="0" dy="2" result="off"/>
    <feGaussianBlur in="off" stdDeviation="2" result="blur"/>
    <feColorMatrix in="blur" type="matrix"
      values="0 0 0 0 0   0 0 0 0 0   0 0 0 0 0   0 0 0 {plate_alpha} 0" result="shadow"/>
    <feMerge><feMergeNode in="shadow"/><feMergeNode in="SourceGraphic"/></feMerge>
  </filter>
  <filter id="f-donut-{uid}" filterUnits="userSpaceOnUse" x="-20" y="-20" width="240" height="240">
    <feOffset in="SourceAlpha" dx="0" dy="2" result="off"/>
    <feGaussianBlur in="off" stdDeviation="2" result="blur"/>
    <feColorMatrix in="blur" type="matrix"
      values="0 0 0 0 0   0 0 0 0 0   0 0 0 0 0   0 0 0 {donut_alpha} 0" result="shadow"/>
    <feMerge><feMergeNode in="shadow"/><feMergeNode in="SourceGraphic"/></feMerge>
  </filter>
"""

def svg_for(score, p, plate_fill, plate_opacity, text_color, with_filters):
    C = 2 * math.pi * RADIUS
    H = p * C
    A = (1 - p) * C
    # Round to two decimals for SVG
    Hs, As = f"{H:.2f}", f"{A:.2f}"

    uid = f"{score}-{int(p*1000)}"
    defs = filters(uid) if with_filters else ""
    plate_filter_attr = f'filter="url(#f-plate-{uid})"' if with_filters else ""
    donut_filter_attr = f'filter="url(#f-donut-{uid})"' if with_filters else ""

    svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="200" height="200" viewBox="0 0 200 200" aria-label="HAI/{score}">
  <defs>{defs}</defs>

  <circle cx="100" cy="100" r="{PLATE_RADIUS}" fill="{plate_fill}" opacity="{plate_opacity}" {plate_filter_attr}/>

  <g {donut_filter_attr}>
    <g transform="rotate(-90 100 100)">
      <circle cx="100" cy="100" r="{RADIUS}" fill="none"
              stroke="{AI}" stroke-width="{RING_WIDTH}" stroke-linecap="butt"
              stroke-dasharray="{As} {Hs}"/>
      <circle cx="100" cy="100" r="{RADIUS}" fill="none"
              stroke="{HUMAN}" stroke-width="{RING_WIDTH}" stroke-linecap="butt"
              stroke-dasharray="{Hs} {As}" stroke-dashoffset="-{As}"/>
    </g>
  </g>

  <circle cx="100" cy="100" r="{CENTER_RADIUS}" fill="{plate_fill}" opacity="{plate_opacity}"/>

  <text x="100" y="82" text-anchor="middle" font-family="Inter, system-ui, -apple-system, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif"
        font-size="18" font-weight="700" letter-spacing="0.5" fill="{text_color}">HAI/</text>
  <text x="100" y="115" text-anchor="middle" font-family="Inter, system-ui, -apple-system, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif"
        font-size="37" font-weight="700" fill="{text_color}">{score}</text>
</svg>'''
    return svg

def main():
    base = pathlib.Path("assets/scorecards")
    (base / "dark-translucent").mkdir(parents=True, exist_ok=True)
    (base / "light-translucent").mkdir(parents=True, exist_ok=True)
    (base / "print-solid-light").mkdir(parents=True, exist_ok=True)
    (base / "print-solid-dark").mkdir(parents=True, exist_ok=True)

    for set_name, plate_fill, plate_opacity, text_color, with_filters in SETS:
        outdir = base / set_name
        for score, p in FRACTIONS.items():
            svg = svg_for(score, p, plate_fill, plate_opacity, text_color, with_filters)
            filename = f"HAI_sticker_{set_name.replace('-', '')}_S{score}.svg"
            # Keep legacy-friendly names too
            if set_name == "dark-translucent":
                filename = f"HAI_sticker_darkPlate10_S{score}.svg"
            elif set_name == "light-translucent":
                filename = f"HAI_sticker_lightPlate14_S{score}.svg"
            elif set_name == "print-solid-light":
                filename = f"HAI_sticker_print_lightSolid_S{score}.svg"
            elif set_name == "print-solid-dark":
                filename = f"HAI_sticker_print_darkSolid_S{score}.svg"

            (outdir / filename).write_text(svg, encoding="utf-8")

if __name__ == "__main__":
    main()
