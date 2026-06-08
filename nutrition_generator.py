import os
import io
import urllib.request
import requests
from PIL import Image
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.colors import Color, HexColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import arabic_reshaper
from bidi.algorithm import get_display

W, H = A4

# ═══════════════════════════════════════════════
# FONT SYSTEM - Works on Windows + Linux + Cloud
# ═══════════════════════════════════════════════

FONT_MAP = {
    'P-Reg':   'Helvetica',
    'P-Bold':  'Helvetica-Bold',
    'P-Light': 'Helvetica',
    'P-Med':   'Helvetica',
    'AR-Reg':  'Helvetica',
    'AR-Bold': 'Helvetica-Bold',
}

# Amiri Arabic font - auto-download if missing
AMIRI_URLS = {
    'AR-Reg':  'https://github.com/google/fonts/raw/main/ofl/amiri/Amiri-Regular.ttf',
    'AR-Bold': 'https://github.com/google/fonts/raw/main/ofl/amiri/Amiri-Bold.ttf',
}

# Latin font search paths (Windows → Linux)
LATIN_PATHS = [
    ('C:/Windows/Fonts/arial.ttf',                                       'C:/Windows/Fonts/arialbd.ttf'),
    ('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',                  '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'),
    ('/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf',  '/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf'),
]

# Arabic font search paths (Local → Windows → Linux)
ARABIC_PATHS = [
    ('fonts/Amiri-Regular.ttf',                                   'fonts/Amiri-Bold.ttf'),
    ('C:/Windows/Fonts/arial.ttf',                                'C:/Windows/Fonts/arialbd.ttf'),
    ('/usr/share/fonts/truetype/amiri/amiri.ttf',                 '/usr/share/fonts/truetype/amiri/amiri-bold.ttf'),
    ('/usr/share/fonts/truetype/noto/NotoSansArabic-Regular.ttf', '/usr/share/fonts/truetype/noto/NotoSansArabic-Bold.ttf'),
]

def _register(alias, path, fallback):
    """Register a TTFont. Returns True on success."""
    if path and os.path.exists(path):
        try:
            pdfmetrics.registerFont(TTFont(alias, path))
            FONT_MAP[alias] = alias
            return True
        except:
            pass
    FONT_MAP[alias] = fallback
    return False

def _download_amiri():
    """Download Amiri Arabic fonts if not present locally."""
    os.makedirs('fonts', exist_ok=True)
    paths = {}
    for alias, url in AMIRI_URLS.items():
        dest = f'fonts/Amiri-{"Regular" if "Reg" in alias else "Bold"}.ttf'
        if not os.path.exists(dest):
            try:
                urllib.request.urlretrieve(url, dest)
            except:
                dest = None
        paths[alias] = dest
    return paths

def setup_fonts():
    """Initialize all fonts with automatic fallbacks."""
    # 1. Latin fonts
    for reg_path, bold_path in LATIN_PATHS:
        if os.path.exists(reg_path):
            try:
                pdfmetrics.registerFont(TTFont('P-Reg', reg_path))
                pdfmetrics.registerFont(TTFont('P-Light', reg_path))
                pdfmetrics.registerFont(TTFont('P-Med', reg_path))
                FONT_MAP['P-Reg'] = FONT_MAP['P-Light'] = FONT_MAP['P-Med'] = 'P-Reg'

                if os.path.exists(bold_path):
                    pdfmetrics.registerFont(TTFont('P-Bold', bold_path))
                    FONT_MAP['P-Bold'] = 'P-Bold'
                else:
                    pdfmetrics.registerFont(TTFont('P-Bold', reg_path))
                    FONT_MAP['P-Bold'] = 'P-Reg'
                break
            except:
                pass

    # Fallback if no Latin font registered
    if FONT_MAP.get('P-Reg') == 'Helvetica' or 'P-Reg' not in pdfmetrics._fonts:
        FONT_MAP['P-Reg']   = 'Helvetica'
        FONT_MAP['P-Bold']  = 'Helvetica-Bold'
        FONT_MAP['P-Light'] = 'Helvetica'
        FONT_MAP['P-Med']   = 'Helvetica'

    # 2. Arabic fonts
    arabic_ok = False
    for reg_path, bold_path in ARABIC_PATHS:
        if _register('AR-Reg', reg_path, 'Helvetica'):
            _register('AR-Bold', bold_path, FONT_MAP.get('AR-Reg', 'Helvetica'))
            arabic_ok = True
            break

    # 3. Auto-download Amiri if no Arabic font found
    if not arabic_ok:
        downloaded = _download_amiri()
        _register('AR-Reg', downloaded.get('AR-Reg'), 'Helvetica')
        _register('AR-Bold', downloaded.get('AR-Bold'), FONT_MAP.get('AR-Reg', 'Helvetica'))

setup_fonts()

# ═══════════════════════════════════════════════
# ARABIC TEXT PROCESSING
# ═══════════════════════════════════════════════

def ar(text):
    """Reshape + reorder Arabic text for proper PDF rendering."""
    try:
        s = str(text)
        if any('\u0600' <= ch <= '\u06ff' for ch in s):
            reshaped = arabic_reshaper.reshape(s)
            return get_display(reshaped)
        return s
    except:
        return str(text)

def is_arabic(text):
    """Check if text contains Arabic characters."""
    return any('\u0600' <= ch <= '\u06ff' for ch in str(text))

def _select_font(f, text):
    """Select Arabic font for Arabic text, Latin font for everything else."""
    if is_arabic(str(text)):
        return 'AR-Bold' if 'Bold' in f else 'AR-Reg'
    return f

# ═══════════════════════════════════════════════
# COLORS
# ═══════════════════════════════════════════════
BG_DARK     = HexColor('#0A1A0A')
BG_WHITE    = HexColor('#FFFFFF')
BG_CREAM    = HexColor('#F8FAF8')
GREEN       = HexColor('#2E7D32')
GREEN_MID   = HexColor('#4CAF50')
GREEN_LIGHT = HexColor('#81C784')
GREEN_DIM   = HexColor('#C8E6C9')
GOLD        = HexColor('#C8963E')
GOLD2       = HexColor('#D4AF37')
GRAY_DARK   = HexColor('#333333')
GRAY        = HexColor('#666666')
GRAY_LIGHT  = HexColor('#999999')
WHITE       = HexColor('#FFFFFF')
BLACK       = HexColor('#111111')

# ═══════════════════════════════════════════════
# LAYOUT CONSTANTS
# ═══════════════════════════════════════════════
M           = 24
HDR_H       = 44
FTR_H       = 34
STRIPE_W    = 4
TOTAL_PAGES = 6

# ═══════════════════════════════════════════════
# IMAGE LOADER
# ═══════════════════════════════════════════════
temp_images = []

def load_image_from_url(url, max_size=(200, 200)):
    """Download image from URL, return temp file path."""
    if not url or url == '#' or not url.startswith('http'):
        return None
    try:
        response = requests.get(url, timeout=10, headers={'User-Agent': 'Mozilla/5.0'})
        response.raise_for_status()
        img = Image.open(BytesIO(response.content))
        img = img.convert('RGB')
        img.thumbnail(max_size, Image.LANCZOS)
        temp_path = f'temp_img_{len(temp_images)}.jpg'
        img.save(temp_path, 'JPEG', quality=85)
        temp_images.append(temp_path)
        return temp_path
    except:
        return None

def cleanup_temp_images():
    """Remove temporary image files."""
    for path in temp_images:
        try:
            if os.path.exists(path):
                os.remove(path)
        except:
            pass

# ═══════════════════════════════════════════════
# PRIMITIVES
# ═══════════════════════════════════════════════

def fill_bg(c, col=None):
    c.setFillColor(col or BG_WHITE)
    c.rect(0, 0, W, H, stroke=0, fill=1)

def fill_rect(c, x, y, w, h, col):
    c.setFillColor(col)
    c.rect(x, y, w, h, stroke=0, fill=1)

def rrect(c, x, y, w, h, r, fc, sc=None, sw=0.5):
    c.setFillColor(fc)
    if sc:
        c.setStrokeColor(sc)
        c.setLineWidth(sw)
    p = c.beginPath()
    p.moveTo(x+r, y); p.lineTo(x+w-r, y)
    p.arcTo(x+w-2*r, y, x+w, y+2*r, -90, 90)
    p.lineTo(x+w, y+h-r)
    p.arcTo(x+w-2*r, y+h-2*r, x+w, y+h, 0, 90)
    p.lineTo(x+r, y+h)
    p.arcTo(x, y+h-2*r, x+2*r, y+h, 90, 90)
    p.lineTo(x, y+r)
    p.arcTo(x, y, x+2*r, y+2*r, 180, 90)
    p.close()
    c.drawPath(p, fill=1, stroke=1 if sc else 0)

def tl(c, s, x, y, f='P-Reg', sz=10, col=BLACK):
    """Left-aligned text. Auto-switches to Arabic font if text is Arabic."""
    font = FONT_MAP.get(_select_font(f, s), f)
    c.setFillColor(col)
    c.setFont(font, sz)
    c.drawString(x, y, ar(s))

def tc(c, s, x, y, f='P-Reg', sz=10, col=BLACK):
    """Center-aligned text. Auto-switches to Arabic font if text is Arabic."""
    font = FONT_MAP.get(_select_font(f, s), f)
    c.setFillColor(col)
    c.setFont(font, sz)
    c.drawCentredString(x, y, ar(s))

def tr(c, s, x, y, f='P-Reg', sz=10, col=BLACK):
    """Right-aligned text. Auto-switches to Arabic font if text is Arabic."""
    font = FONT_MAP.get(_select_font(f, s), f)
    c.setFillColor(col)
    c.setFont(font, sz)
    c.drawRightString(x, y, ar(s))

def hline(c, x, y, w, col=GREEN, lw=1.0):
    c.setStrokeColor(col); c.setLineWidth(lw); c.line(x, y, x+w, y)

def circle(c, cx, cy, r, col):
    c.setFillColor(col); c.circle(cx, cy, r, fill=1, stroke=0)

def stripe(c):
    fill_rect(c, 0, 0, STRIPE_W, H, GREEN)

def content_area():
    x = STRIPE_W + M
    w = W - x - M
    return x, H - HDR_H - M, w

def wrap(c, text, x, y, maxw, f, sz, col, lh=None):
    """Word-wrap with auto font selection for Arabic/English."""
    lh = lh or sz * 1.55
    font = FONT_MAP.get(_select_font(f, text), f)
    c.setFillColor(col)
    c.setFont(font, sz)
    words = ar(text).split()
    line = []
    for word in words:
        if c.stringWidth(' '.join(line + [word]), font, sz) <= maxw:
            line.append(word)
        else:
            if line: c.drawString(x, y, ' '.join(line)); y -= lh
            line = [word]
    if line: c.drawString(x, y, ' '.join(line)); y -= lh
    return y

# ═══════════════════════════════════════════════
# CHROME (Header + Footer) — always English
# ═══════════════════════════════════════════════

def chrome(c, section, pgnum, data):
    stripe(c)
    fill_rect(c, 0, H-HDR_H, W, HDR_H, BG_CREAM)
    hline(c, 0, H-HDR_H, W, GREEN, 0.8)
    tl(c, 'AHMED', STRIPE_W+12, H-HDR_H+17, 'P-Bold', 13, GREEN)
    tl(c, 'TEKA', STRIPE_W+68, H-HDR_H+17, 'P-Bold', 13, GRAY_DARK)
    tc(c, section, W/2, H-HDR_H+17, 'P-Reg', 9, GRAY)
    fill_rect(c, 0, 0, W, FTR_H, BG_CREAM)
    hline(c, 0, FTR_H, W, GREEN, 0.6)
    tl(c, '@coach.teka1', STRIPE_W+12, FTR_H/2-4, 'P-Reg', 8, GREEN)
    c.linkURL('https://www.instagram.com/coach.teka1',
              (STRIPE_W+12, FTR_H/2-10, STRIPE_W+80, FTR_H/2+4), relative=0)
    tc(c, '01033047057', W/2, FTR_H/2-4, 'P-Reg', 8, GRAY)
    tr(c, f'{pgnum} / {TOTAL_PAGES}', W-12, FTR_H/2-4, 'P-Bold', 9, GREEN)

# ═══════════════════════════════════════════════
# PAGE 1 - COVER  (fully English)
# ═══════════════════════════════════════════════

def p1_cover(c, data):
    fill_bg(c, BG_DARK)

    cover_photo = 'images/AhmedTeka_image1.jpeg'
    try:
        if os.path.exists(cover_photo):
            c.drawImage(cover_photo, 0, 0, W, H, preserveAspectRatio=True)
    except:
        pass

    c.setFillColor(Color(0, 0, 0, alpha=0.55))
    c.rect(0, 0, W, H, stroke=0, fill=1)
    stripe(c)

    fill_rect(c, 0, H-52, W, 52, Color(0,0,0,0.85))
    hline(c, 0, H-52, W, GREEN_MID, 1.2)
    tl(c, 'AHMED', STRIPE_W+16, H-32, 'P-Bold', 18, GREEN_MID)
    tl(c, 'TEKA', STRIPE_W+84, H-32, 'P-Bold', 18, WHITE)
    hline(c, STRIPE_W+16, H-40, 100, GREEN_MID, 0.6)
    tr(c, 'NUTRITION COACH', W-16, H-32, 'P-Reg', 8.5, GRAY_LIGHT)

    ty = H - 130
    c.setStrokeColor(Color(1,1,1,0.4)); c.setLineWidth(1.2)
    c.line(STRIPE_W+20, ty+30, STRIPE_W+20+50, ty+30)
    c.line(W-20-50, ty+30, W-20, ty+30)

    tc(c, 'NUTRITION', W/2, ty+15, 'P-Bold', 56, WHITE)
    tc(c, 'PLAN', W/2, ty-30, 'P-Bold', 56, GREEN_MID)
    tc(c, 'Personalized Meal Plan', W/2, ty-55, 'P-Reg', 12, Color(1,1,1,0.6))

    by = 130
    rrect(c, STRIPE_W+16, by, W-STRIPE_W-32, 54, 6, Color(0,0,0,0.78), GREEN_MID, 1.2)
    fill_rect(c, STRIPE_W+16, by, 4, 54, GREEN_MID)
    tl(c, 'CLIENT', STRIPE_W+28, by+40, 'P-Light', 7, GREEN_LIGHT)
    tr(c, data.get('client_name', 'CLIENT'), W-24, by+16, 'P-Bold', 32, WHITE)

    pw = (W - STRIPE_W - 36) / 3 - 5
    pills = [
        ('DURATION', data.get('duration', '12 WEEKS')),
        ('MEALS',    data.get('meals_count', '4 MEALS')),
        ('START',    data.get('start_date', 'JUNE 2026')),
    ]
    for i, (lbl, val) in enumerate(pills):
        px = STRIPE_W + 16 + i * (pw + 7.5)
        rrect(c, px, by-58, pw, 50, 4, Color(0,0,0,0.70), GOLD2, 0.6)
        tl(c, lbl, px+10, by-24, 'P-Light', 7, GRAY_LIGHT)
        tl(c, str(val), px+10, by-44, 'P-Bold', 12, GREEN_MID)

    fill_rect(c, 0, 0, W, 40, Color(0,0,0,0.88))
    hline(c, 0, 40, W, GREEN_MID, 0.8)
    tl(c, '@coach.teka1', STRIPE_W+16, 15, 'P-Reg', 8, GREEN_MID)
    c.linkURL('https://www.instagram.com/coach.teka1',
              (STRIPE_W+16, 8, STRIPE_W+85, 24), relative=0)
    tc(c, '01033047057', W/2, 15, 'P-Reg', 8, GRAY_LIGHT)
    tr(c, f'Coach {data.get("coach_name", "AHMED TEKA")}', W-14, 15, 'P-Bold', 9, GREEN_MID)

    c.showPage()

# ═══════════════════════════════════════════════
# PAGE 2 - PROFILE  (fully English)
# ═══════════════════════════════════════════════

def p2_profile(c, data):
    fill_bg(c, BG_CREAM)
    chrome(c, 'CLIENT PROFILE', 2, data)
    x, y, cw = content_area()

    tc(c, 'CLIENT PROFILE', x + cw/2, y - 10, 'P-Bold', 30, GREEN)
    hline(c, x, y - 20, cw, GREEN, 1)

    py = y - 40
    info_items = [
        ('FULL NAME', data.get('full_name', 'N/A')),
        ('AGE',       data.get('age', 'N/A')),
        ('WEIGHT',    data.get('weight', 'N/A')),
        ('HEIGHT',    data.get('height', 'N/A')),
        ('GOAL',      data.get('goal', 'N/A')),
    ]

    bw = (cw - 10) / 2
    for i, (lbl, val) in enumerate(info_items):
        col = i % 2
        row = i // 2
        ix = x + col * (bw + 10)
        iy = py - row * 52

        rrect(c, ix, iy-42, bw, 40, 5, WHITE, GREEN_DIM, 0.3)
        fill_rect(c, ix, iy-42, 3, 40, GREEN)
        # Label always English
        tl(c, lbl, ix+10, iy-14, 'P-Light', 10, GRAY)
        # Value: render with auto font (English values stay Latin, Arabic values switch)
        if is_arabic(str(val)):
            tr(c, val, ix+bw-10, iy-30, 'P-Bold', 16, BLACK)
        else:
            tl(c, val, ix+10, iy-30, 'P-Bold', 16, BLACK)

    ny = py - (((len(info_items) // 2) + 1) * 52) - 10
    if data.get('notes'):
        rrect(c, x, ny-42, cw, 40, 5, WHITE, GREEN_DIM, 0.4)
        tl(c, 'COACH NOTES:', x+10, ny-14, 'P-Bold', 10, GREEN)
        notes_text = data.get('notes', '')
        if is_arabic(str(notes_text)):
            tr(c, notes_text[:70], x+cw-10, ny-28, 'P-Reg', 10, GRAY)
        else:
            tl(c, notes_text[:70], x+10, ny-28, 'P-Reg', 10, GRAY)
        ny -= 52

    my = ny - 60
    tc(c, 'DAILY MACRONUTRIENTS', x + cw/2, my, 'P-Bold', 18, GREEN)
    hline(c, x, my-6, cw, GOLD, 0.6)

    macros = [
        ('MEALS',   data.get('main_meals', '4'), 'per day', GREEN),
        ('PROTEIN', data.get('protein_g', '0'),  'g/day',   GREEN_MID),
        ('CARBS',   data.get('carbs_g', '0'),    'g/day',   GOLD2),
        ('FAT',     data.get('fat_g', '0'),      'g/day',   GREEN_LIGHT),
    ]

    mw = (cw - 24) / 4
    for i, (lbl, val, unit, color) in enumerate(macros):
        mx = x + i * (mw + 8)
        rrect(c, mx, my-60, mw, 55, 7, WHITE, color, 0.8)
        circle(c, mx + mw/2, my-20, 18, color)
        tc(c, str(val), mx + mw/2, my-25, 'P-Bold', 15, WHITE)
        tc(c, lbl,      mx + mw/2, my-42, 'P-Light', 9,  GRAY)
        tc(c, unit,     mx + mw/2, my-52, 'P-Light', 8,  GRAY)

    c.showPage()

# ═══════════════════════════════════════════════
# PAGE 3 - MEALS
# Titles/labels: English
# Meal details (name, type, ingredients, alt): Arabic preserved
# ═══════════════════════════════════════════════

def p3_meals(c, data):
    bg_image = 'images/p3MEAlS.png'
    try:
        if os.path.exists(bg_image):
            c.drawImage(bg_image, 0, 0, W, H, preserveAspectRatio=True)
    except:
        fill_bg(c, BG_CREAM)

    c.setFillColor(Color(1, 1, 1, 0.75))
    c.rect(0, 0, W, H, stroke=0, fill=1)

    chrome(c, 'DAILY MEAL PLAN', 3, data)
    x, y, cw = content_area()

    tc(c, 'DAILY MEAL PLAN', x + cw/2, y - 10, 'P-Bold', 28, GREEN)
    hline(c, x, y - 18, cw, GREEN, 0.8)

    meals = data.get('meals', [])

    my = y - 35
    for i, meal in enumerate(meals[:6]):
        mh = 120

        rrect(c, x, my-mh, cw, mh-3, 7, WHITE, GREEN_DIM, 0.3)
        fill_rect(c, x, my-mh, 4, mh, GREEN)

        icon_url = meal.get('icon', '')
        icon_loaded = False
        if icon_url and icon_url.startswith('http'):
            icon_path = load_image_from_url(icon_url, (40, 40))
            if icon_path and os.path.exists(icon_path):
                c.drawImage(icon_path, x+10, my-38, 36, 36,
                            preserveAspectRatio=True, mask='auto')
                icon_loaded = True

        if not icon_loaded:
            circle(c, x+28, my-28, 18, GREEN_DIM)
            tc(c, '🍽', x+28, my-32, 'P-Reg', 14, BLACK)

        # Meal name & type — Arabic auto-detected
        tr(c, meal.get('name', ''), x+cw-12, my-16, 'P-Bold', 15, BLACK)
        tr(c, meal.get('type', ''), x+cw-12, my-34, 'P-Reg',  10, GRAY)

        # Calories & macros — always English format
        tl(c, f'{meal.get("calories", "0")} kcal', x+56, my-44, 'P-Bold', 22, GREEN)
        tl(c, f'P:{meal.get("protein","0")}g | C:{meal.get("carbs","0")}g | F:{meal.get("fat","0")}g',
           x+56, my-58, 'P-Reg', 11, GRAY)

        # Ingredients — Arabic auto-detected
        ingredients = meal.get('ingredients', [])
        ing_y = my - 52
        if isinstance(ingredients, list):
            for ing in ingredients[:4]:
                tr(c, f'• {ing}', x+cw-12, ing_y, 'P-Reg', 13, GRAY_DARK)
                ing_y -= 14
        else:
            tr(c, f'• {ingredients[:55]}', x+cw-12, ing_y, 'P-Reg', 13, GRAY_DARK)

        # Alternative — Arabic auto-detected
        alt = meal.get('alternative', '')
        if alt:
            tl(c, f'Alt: {alt[:60]}', x+12, my-mh+14, 'P-Reg', 9, GREEN)

        my -= mh + 3

    if my > FTR_H + 50:
        rrect(c, x, my-38, cw, 34, 7, GREEN_DIM, GREEN, 1)
        tc(c, f'Total: {data.get("total_calories", "0")} kcal/day',
           x + cw/2, my-16, 'P-Bold', 15, GREEN)

    c.showPage()

# ═══════════════════════════════════════════════
# PAGE 4 - GUIDELINES  (fully English)
# ═══════════════════════════════════════════════

def p4_guidelines(c, data):
    fill_bg(c, BG_CREAM)
    chrome(c, 'GUIDELINES', 4, data)
    x, y, cw = content_area()

    tc(c, 'DAILY GUIDELINES', x + cw/2, y - 10, 'P-Bold', 28, GREEN)
    hline(c, x, y - 18, cw, GREEN, 0.8)

    wy = y - 35
    rrect(c, x, wy-50, cw, 46, 7, WHITE, GREEN, 1.2)
    fill_rect(c, x, wy-50, 4, 46, GREEN)
    tc(c, 'DAILY HYDRATION', x + cw/2, wy-16, 'P-Bold', 12, GREEN)
    tc(c, f'{data.get("water", "4-6 L")} per day', x + cw/2, wy-36, 'P-Bold', 20, BLACK)

    gy = wy - 65
    gw = (cw - 12) / 2
    guidelines = [
        ('Meal Timing',  data.get('meal_timing', '')),
        ('Food Weighing', data.get('food_weighing', '')),
        ('Drinks',       data.get('drinks', '')),
        ('Restricted',   data.get('sweets', '')),
    ]

    for i, (title, body) in enumerate(guidelines):
        col = i % 2
        row = i // 2
        gx = x + col * (gw + 12)
        gyy = gy - row * 58

        rrect(c, gx, gyy-46, gw, 42, 5, WHITE, GREEN_DIM, 0.3)
        fill_rect(c, gx, gyy-46, 3, 42, GREEN)
        tl(c, title,       gx+8,    gyy-16, 'P-Bold', 11, GREEN)
        tr(c, str(body)[:40], gx+gw-8, gyy-16, 'P-Reg',  11, GRAY)

    oy = gy - 130
    rrect(c, x, oy-32, cw, 28, 5, WHITE, GREEN_DIM, 0.4)
    tl(c, f'Omega-3: {data.get("omega", "")}', x+10, oy-12, 'P-Bold', 11, GREEN)

    sy = oy - 48
    tc(c, 'SUPPLEMENTS', x + cw/2, sy, 'P-Bold', 15, GREEN)
    hline(c, x, sy-5, cw, GOLD, 0.4)

    supplements = data.get('supplements', [])
    for i, sup in enumerate(supplements[:4]):
        sr = sy - 20 - i * 35
        rrect(c, x, sr-26, cw, 24, 4, WHITE, GREEN_DIM, 0.2)
        circle(c, x+18, sr-14, 10, GREEN)
        tc(c, str(i+1), x+18, sr-17, 'P-Bold', 7, WHITE)
        tl(c, sup.get('name', ''),  x+34,    sr-6, 'P-Bold', 11, BLACK)
        tr(c, f'{sup.get("dose", "")} - {sup.get("benefit", "")}'[:45],
           x+cw-10, sr-6, 'P-Reg', 10, GRAY)

    py2 = sy - 20 - len(supplements) * 35 - 15
    if py2 > FTR_H + 60:
        tc(c, 'PRE-WORKOUT PROTOCOL', x + cw/2, py2, 'P-Bold', 13, GREEN)
        hline(c, x, py2-5, cw, GOLD, 0.4)

        preworkout = data.get('preworkout', [])
        for i, pw in enumerate(preworkout[:2]):
            pwy = py2 - 20 - i * 30
            rrect(c, x, pwy-22, cw, 20, 4, GREEN_DIM, GREEN, 0.2)
            tl(c, f'{pw.get("time", "")}: {pw.get("item", "")}'[:65],
               x+10, pwy-10, 'P-Reg', 10, BLACK)

    c.showPage()

# ═══════════════════════════════════════════════
# PAGE 5 - RECIPES  (fully English)
# ═══════════════════════════════════════════════

def p5_recipes(c, data):
    fill_bg(c, BG_CREAM)
    chrome(c, 'RECIPES', 5, data)
    x, y, cw = content_area()

    tc(c, 'RECIPE LIBRARY', x + cw/2, y - 10, 'P-Bold', 28, GREEN)
    hline(c, x, y - 18, cw, GREEN, 0.8)

    recipes = data.get('recipes', [])
    rw = (cw - 16) / 3

    ry = y - 35
    for i, recipe in enumerate(recipes[:6]):
        col = i % 3
        row = i // 3
        rx = x + col * (rw + 8)
        ryy = ry - row * 125

        rrect(c, rx, ryy-110, rw, 105, 7, WHITE, GREEN_DIM, 0.3)

        img_url = recipe.get('image', '')
        img_loaded = False
        if img_url and img_url.startswith('http'):
            img_path = load_image_from_url(img_url, (60, 60))
            if img_path and os.path.exists(img_path):
                c.saveState()
                clip_path = c.beginPath()
                clip_path.circle(rx + rw/2, ryy-40, 24)
                c.clipPath(clip_path, stroke=0, fill=0)
                c.drawImage(img_path, rx + rw/2 - 24, ryy-64, 48, 48,
                            preserveAspectRatio=True)
                c.restoreState()
                img_loaded = True

        if not img_loaded:
            circle(c, rx + rw/2, ryy-40, 24, GREEN_DIM)
            circle(c, rx + rw/2, ryy-40, 18, GREEN)
            tc(c, '🍽', rx + rw/2, ryy-44, 'P-Reg', 14, WHITE)
        else:
            c.setStrokeColor(GREEN)
            c.setLineWidth(2)
            c.circle(rx + rw/2, ryy-40, 24, fill=0, stroke=1)

        tc(c, recipe.get('name', '')[:16], rx + rw/2, ryy-68, 'P-Bold', 12, BLACK)
        tc(c, recipe.get('desc', '')[:22], rx + rw/2, ryy-82, 'P-Reg',  10, GRAY)

        rrect(c, rx+10, ryy-104, rw-20, 18, 4, GREEN)
        tc(c, 'Watch', rx + rw/2, ryy-94, 'P-Bold', 8, WHITE)

        link = recipe.get('link', '#')
        if link and link != '#':
            c.linkURL(link, (rx+10, ryy-104, rx+rw-10, ryy-86))

    qy = ry - 280
    if qy > FTR_H + 50:
        rrect(c, x, qy-44, cw, 40, 7, GREEN_DIM, GREEN, 0.8)
        tc(c, '"Stay consistent, stay disciplined."', x + cw/2, qy-16, 'P-Bold', 12, GREEN)
        tc(c, f'- {data.get("coach_name", "Ahmed Teka")}', x + cw/2, qy-32, 'P-Reg', 10, GRAY)

    c.showPage()

# ═══════════════════════════════════════════════
# PAGE 6 - COACH  (fully English)
# ═══════════════════════════════════════════════

def p6_coach(c, data):
    fill_bg(c, BG_DARK)

    coach_photo = 'images/AhmedTeka_image3.jpeg'
    try:
        if os.path.exists(coach_photo):
            c.drawImage(coach_photo, 0, 0, W, H, preserveAspectRatio=True)
    except:
        pass

    c.setFillColor(Color(0, 0, 0, alpha=0.55))
    c.rect(0, 0, W, H, stroke=0, fill=1)
    stripe(c)

    fill_rect(c, 0, H-60, W, 60, Color(0,0,0,0.8))
    hline(c, 0, H-60, W, GREEN_MID, 0.8)
    tc(c, data.get('coach_name', 'AHMED TEKA'), W/2, H-45, 'P-Bold', 48, GREEN_MID)

    cy = H * 0.55

    fill_rect(c, 0, 0, W, 75, Color(0,0,0,0.8))
    hline(c, 0, 75, W, GREEN_MID, 0.7)

    btn_w = 150; btn_h = 32
    total_w = 2*btn_w + 12
    bx_start = W/2 - total_w/2

    for i, (lbl, color) in enumerate([
        (data.get('instagram', '@coach.teka1'), GREEN_MID),
        (data.get('phone', '01033047057'),      GOLD2),
    ]):
        bx = bx_start + i*(btn_w+12)
        by = 22
        rrect(c, bx, by, btn_w, btn_h, 5, Color(0,0,0,0.4), color, 1)
        tc(c, lbl, bx+btn_w/2, by+btn_h/2-4, 'P-Bold', 10, WHITE)
        if i == 0:
            insta = data.get('instagram', 'coach.teka1').lstrip('@')
            c.linkURL(
                f'https://www.instagram.com/{insta}',
                (bx, by, bx+btn_w, by+btn_h),
                relative=0
            )

    tr(c, f'{TOTAL_PAGES} / {TOTAL_PAGES}', W-14, 85, 'P-Bold', 9, GREEN_MID)

    c.showPage()
# ═══════════════════════════════════════════════
# BUILD
# ═══════════════════════════════════════════════

def generate_nutrition_pdf(data):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    c.setTitle('AHMED TEKA - Diet Plan')
    c.setAuthor('AHMED TEKA')

    p1_cover(c, data)
    p2_profile(c, data)
    p3_meals(c, data)
    p4_guidelines(c, data)
    p5_recipes(c, data)
    p6_coach(c, data)

    c.save()
    pdf_bytes = buffer.getvalue()
    buffer.close()
    cleanup_temp_images()
    return pdf_bytes