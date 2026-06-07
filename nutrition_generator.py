import os
import io
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.colors import Color, HexColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import arabic_reshaper
from bidi.algorithm import get_display

W, H = A4

# ═══════════════════════════════════════════════
# FONTS
# ═══════════════════════════════════════════════
FONT_PATHS = [
    'C:/Windows/Fonts/arial.ttf',
    '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',
    '/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf',
]

for fp in FONT_PATHS:
    if os.path.exists(fp):
        try:
            pdfmetrics.registerFont(TTFont('P-Reg', fp))
            bold_path = fp.replace('.ttf','bd.ttf').replace('Sans','Sans-Bold').replace('Regular','Bold')
            if os.path.exists(bold_path):
                pdfmetrics.registerFont(TTFont('P-Bold', bold_path))
            else:
                pdfmetrics.registerFont(TTFont('P-Bold', fp))
            pdfmetrics.registerFont(TTFont('P-Light', fp))
            pdfmetrics.registerFont(TTFont('P-Med', fp))
            break
        except:
            pass

# ═══════════════════════════════════════════════
# ARABIC HELPER
# ═══════════════════════════════════════════════
def ar(text):
    try:
        s = str(text)
        if any('\u0600' <= c <= '\u06ff' for c in s):
            reshaped = arabic_reshaper.reshape(s)
            bidi = get_display(reshaped)
            return bidi
        return s
    except:
        return str(text)

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
# LAYOUT
# ═══════════════════════════════════════════════
M           = 24
HDR_H       = 44
FTR_H       = 34
STRIPE_W    = 4
TOTAL_PAGES = 6

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
    c.setFillColor(col); c.setFont(f, sz); c.drawString(x, y, ar(s))

def tc(c, s, x, y, f='P-Reg', sz=10, col=BLACK):
    c.setFillColor(col); c.setFont(f, sz); c.drawCentredString(x, y, ar(s))

def tr(c, s, x, y, f='P-Reg', sz=10, col=BLACK):
    c.setFillColor(col); c.setFont(f, sz); c.drawRightString(x, y, ar(s))

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
    lh = lh or sz * 1.55
    c.setFillColor(col); c.setFont(f, sz)
    words = ar(text).split()
    line = []
    for word in words:
        if c.stringWidth(' '.join(line + [word]), f, sz) <= maxw:
            line.append(word)
        else:
            if line: c.drawString(x, y, ' '.join(line)); y -= lh
            line = [word]
    if line: c.drawString(x, y, ' '.join(line)); y -= lh
    return y

# ═══════════════════════════════════════════════
# CHROME
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
    tc(c, '01033047057', W/2, FTR_H/2-4, 'P-Reg', 8, GRAY)
    tr(c, f'{pgnum} / {TOTAL_PAGES}', W-12, FTR_H/2-4, 'P-Bold', 9, GREEN)

# ═══════════════════════════════════════════════
# PAGE 1 - COVER
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
    
    fill_rect(c, 0, H-50, W, 50, Color(0,0,0,0.8))
    hline(c, 0, H-50, W, GREEN_MID, 1)
    tl(c, 'AHMED', STRIPE_W+16, H-32, 'P-Bold', 18, GREEN_MID)
    tl(c, 'TEKA', STRIPE_W+82, H-32, 'P-Bold', 18, WHITE)
    tr(c, 'NUTRITION COACH', W-16, H-32, 'P-Reg', 9, GRAY_LIGHT)
    
    ty = H - 135
    tc(c, 'NUTRITION', W/2, ty+15, 'P-Bold', 52, WHITE)
    tc(c, 'PLAN', W/2, ty-30, 'P-Bold', 52, GREEN_MID)
    tc(c, 'Personalized Meal Plan', W/2, ty-55, 'P-Reg', 11, Color(1,1,1,0.6))
    
    # Client card - Name only, no goal
    cy = ty - 100
    rrect(c, STRIPE_W+16, cy, W-STRIPE_W-32, 56, 6, Color(0,0,0,0.75), GREEN_MID, 1)
    fill_rect(c, STRIPE_W+16, cy, 4, 56, GREEN_MID)
    tl(c, 'CLIENT', STRIPE_W+28, cy+40, 'P-Light', 8, GREEN_LIGHT)
    tr(c, data.get('client_name', 'CLIENT'), W-24, cy+10, 'P-Bold', 28, WHITE)
    
    by = cy - 10
    pw = (W - STRIPE_W - 36) / 3 - 5
    pills = [
        ('DURATION', data.get('duration', '12 WEEKS')),
        ('MEALS', data.get('meals_count', '4 MEALS')),
        ('START', data.get('start_date', 'JUNE 2026')),
    ]
    for i, (lbl, val) in enumerate(pills):
        px = STRIPE_W + 16 + i * (pw + 7.5)
        rrect(c, px, by-55, pw, 46, 4, Color(0,0,0,0.65), GOLD2, 0.5)
        tl(c, lbl, px+10, by-22, 'P-Light', 8, GRAY_LIGHT)
        tl(c, val, px+10, by-42, 'P-Bold', 12, GREEN_MID)
    
    fill_rect(c, 0, 0, W, 38, Color(0,0,0,0.85))
    hline(c, 0, 38, W, GREEN_MID, 0.7)
    tl(c, '@coach.teka1', STRIPE_W+16, 13, 'P-Reg', 9, GREEN_MID)
    tc(c, '01033047057', W/2, 13, 'P-Reg', 9, GRAY_LIGHT)
    tr(c, 'Coach Ahmed Teka', W-14, 13, 'P-Bold', 10, GREEN_MID)
    
    c.showPage()

# ═══════════════════════════════════════════════
# PAGE 2 - PROFILE
# ═══════════════════════════════════════════════

def p2_profile(c, data):
    fill_bg(c, BG_CREAM)
    chrome(c, 'CLIENT PROFILE', 2, data)
    x, y, cw = content_area()
    
    tc(c, 'CLIENT PROFILE', x + cw/2, y - 10, 'P-Bold', 26, GREEN)
    hline(c, x, y - 20, cw, GREEN, 1)
    
    py = y - 40
    info_items = [
        ('FULL NAME', data.get('full_name', 'N/A')),
        ('AGE', data.get('age', 'N/A')),
        ('WEIGHT', data.get('weight', 'N/A')),
        ('HEIGHT', data.get('height', 'N/A')),
        ('GOAL', data.get('goal', 'N/A')),
    ]
    
    bw = (cw - 10) / 2
    for i, (lbl, val) in enumerate(info_items):
        col = i % 2
        row = i // 2
        ix = x + col * (bw + 10)
        iy = py - row * 52
        
        rrect(c, ix, iy-42, bw, 40, 5, WHITE, GREEN_DIM, 0.3)
        fill_rect(c, ix, iy-42, 3, 40, GREEN)
        tl(c, lbl, ix+10, iy-14, 'P-Light', 8, GRAY)
        tr(c, val, ix+bw-10, iy-14, 'P-Bold', 14, BLACK)
    
    ny = py - 120
    if data.get('notes'):
        rrect(c, x, ny-42, cw, 40, 5, WHITE, GREEN_DIM, 0.4)
        tl(c, 'COACH NOTES:', x+10, ny-14, 'P-Bold', 10, GREEN)
        tr(c, data.get('notes', '')[:70], x+cw-10, ny-14, 'P-Reg', 10, GRAY)
        ny -= 52
    
    my = ny - 60
    tc(c, 'DAILY MACRONUTRIENTS', x + cw/2, my, 'P-Bold', 16, GREEN)
    hline(c, x, my-6, cw, GOLD, 0.6)
    
    macros = [
        ('MEALS', data.get('main_meals', '4'), 'per day', GREEN),
        ('PROTEIN', data.get('protein_g', '0'), 'g/day', GREEN_MID),
        ('CARBS', data.get('carbs_g', '0'), 'g/day', GOLD2),
        ('FAT', data.get('fat_g', '0'), 'g/day', GREEN_LIGHT),
    ]
    
    mw = (cw - 24) / 4
    for i, (lbl, val, unit, color) in enumerate(macros):
        mx = x + i * (mw + 8)
        rrect(c, mx, my-60, mw, 55, 7, WHITE, color, 0.8)
        circle(c, mx + mw/2, my-20, 18, color)
        tc(c, val, mx + mw/2, my-25, 'P-Bold', 15, WHITE)
        tc(c, lbl, mx + mw/2, my-42, 'P-Light', 8, GRAY)
        tc(c, unit, mx + mw/2, my-52, 'P-Light', 7, GRAY)
    
    c.showPage()

# ═══════════════════════════════════════════════
# PAGE 3 - MEALS (Larger text for readability)
# ═══════════════════════════════════════════════

def p3_meals(c, data):
    fill_bg(c, BG_CREAM)
    chrome(c, 'DAILY MEAL PLAN', 3, data)
    x, y, cw = content_area()
    
    tc(c, 'DAILY MEAL PLAN', x + cw/2, y - 10, 'P-Bold', 24, GREEN)
    hline(c, x, y - 18, cw, GREEN, 0.8)
    
    meals = data.get('meals', [])
    icons = ['🥣', '💪', '🍗', '🥗', '🍝', '🥤']
    
    my = y - 35
    for i, meal in enumerate(meals[:6]):
        icon = icons[i] if i < len(icons) else '🍽️'
        mh = 120
        
        rrect(c, x, my-mh, cw, mh-3, 7, WHITE, GREEN_DIM, 0.3)
        fill_rect(c, x, my-mh, 4, mh, GREEN)
        
        # Icon circle - top left
        circle(c, x+30, my-28, 18, GREEN_DIM)
        tc(c, icon, x+30, my-32, 'P-Reg', 16, BLACK)
        
        # Meal name + type - top right
        tr(c, meal.get('name', ''), x+cw-12, my-16, 'P-Bold', 13, BLACK)
        tr(c, meal.get('type', ''), x+cw-12, my-30, 'P-Reg', 8, GRAY)
        
        # Calories + macros - left side below icon
        tl(c, f'{meal.get("calories", "0")} kcal', x+56, my-44, 'P-Bold', 18, GREEN)
        tl(c, f'P:{meal.get("protein","0")}g | C:{meal.get("carbs","0")}g | F:{meal.get("fat","0")}g', x+56, my-58, 'P-Reg', 9, GRAY)
        
        # Ingredients - right side, BIGGER font
        ingredients = meal.get('ingredients', [])
        ing_y = my - 44
        if isinstance(ingredients, list):
            for ing in ingredients[:4]:
                tr(c, f'• {ing}', x+cw-12, ing_y, 'P-Reg', 11, GRAY_DARK)
                ing_y -= 14
        else:
            tr(c, f'• {ingredients[:55]}', x+cw-12, ing_y, 'P-Reg', 11, GRAY_DARK)
        
        # Alternative - left side at bottom
        alt = meal.get('alternative', '')
        if alt:
            tl(c, f'🔄 {alt[:60]}', x+12, my-mh+14, 'P-Reg', 9, GREEN)
        
        my -= mh + 3
    
    if my > FTR_H + 50:
        rrect(c, x, my-38, cw, 34, 7, GREEN_DIM, GREEN, 1)
        tc(c, f'Total: {data.get("total_calories", "0")} kcal/day', x + cw/2, my-16, 'P-Bold', 15, GREEN)
    
    c.showPage()

# ═══════════════════════════════════════════════
# PAGE 4 - GUIDELINES
# ═══════════════════════════════════════════════

def p4_guidelines(c, data):
    fill_bg(c, BG_CREAM)
    chrome(c, 'GUIDELINES', 4, data)
    x, y, cw = content_area()
    
    tc(c, 'DAILY GUIDELINES', x + cw/2, y - 10, 'P-Bold', 24, GREEN)
    hline(c, x, y - 18, cw, GREEN, 0.8)
    
    wy = y - 35
    rrect(c, x, wy-50, cw, 46, 7, WHITE, GREEN, 1.2)
    fill_rect(c, x, wy-50, 4, 46, GREEN)
    tc(c, '💧 DAILY HYDRATION', x + cw/2, wy-16, 'P-Bold', 12, GREEN)
    tc(c, f'{data.get("water", "4-6 L")} per day', x + cw/2, wy-36, 'P-Bold', 20, BLACK)
    
    gy = wy - 65
    gw = (cw - 12) / 2
    guidelines = [
        ('Meal Timing', data.get('meal_timing', '')),
        ('Food Weighing', data.get('food_weighing', '')),
        ('Drinks', data.get('drinks', '')),
        ('Restricted', data.get('sweets', '')),
    ]
    
    for i, (title, body) in enumerate(guidelines):
        col = i % 2
        row = i // 2
        gx = x + col * (gw + 12)
        gyy = gy - row * 58
        
        rrect(c, gx, gyy-46, gw, 42, 5, WHITE, GREEN_DIM, 0.3)
        fill_rect(c, gx, gyy-46, 3, 42, GREEN)
        tl(c, title, gx+8, gyy-16, 'P-Bold', 10, GREEN)
        tr(c, body[:40], gx+gw-8, gyy-16, 'P-Reg', 9, GRAY)
    
    oy = gy - 130
    rrect(c, x, oy-32, cw, 28, 5, WHITE, GREEN_DIM, 0.4)
    tl(c, '🐟 Omega-3:', x+10, oy-12, 'P-Bold', 10, GREEN)
    tr(c, data.get('omega', ''), x+cw-10, oy-12, 'P-Reg', 10, GRAY)
    
    sy = oy - 48
    tc(c, 'SUPPLEMENTS', x + cw/2, sy, 'P-Bold', 15, GREEN)
    hline(c, x, sy-5, cw, GOLD, 0.4)
    
    supplements = data.get('supplements', [])
    for i, sup in enumerate(supplements[:4]):
        sr = sy - 20 - i * 35
        rrect(c, x, sr-26, cw, 24, 4, WHITE, GREEN_DIM, 0.2)
        circle(c, x+18, sr-14, 10, GREEN)
        tc(c, str(i+1), x+18, sr-17, 'P-Bold', 7, WHITE)
        tl(c, sup.get('name', ''), x+34, sr-6, 'P-Bold', 10, BLACK)
        tr(c, f'{sup.get("dose", "")} - {sup.get("benefit", "")}'[:45], x+cw-10, sr-6, 'P-Reg', 9, GRAY)
    
    c.showPage()

# ═══════════════════════════════════════════════
# PAGE 5 - RECIPES
# ═══════════════════════════════════════════════

def p5_recipes(c, data):
    fill_bg(c, BG_CREAM)
    chrome(c, 'RECIPES', 5, data)
    x, y, cw = content_area()
    
    tc(c, 'RECIPE LIBRARY', x + cw/2, y - 10, 'P-Bold', 24, GREEN)
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
        
        circle(c, rx + rw/2, ryy-40, 24, GREEN_DIM)
        circle(c, rx + rw/2, ryy-40, 18, GREEN)
        tc(c, '🍽️', rx + rw/2, ryy-44, 'P-Reg', 15, WHITE)
        
        tc(c, recipe.get('name', '')[:16], rx + rw/2, ryy-68, 'P-Bold', 10, BLACK)
        tc(c, recipe.get('desc', '')[:22], rx + rw/2, ryy-82, 'P-Reg', 8, GRAY)
        
        rrect(c, rx+10, ryy-104, rw-20, 18, 4, GREEN)
        tc(c, 'Watch', rx + rw/2, ryy-94, 'P-Bold', 8, WHITE)
        
        link = recipe.get('link', '#')
        if link and link != '#':
            c.linkURL(link, (rx+10, ryy-104, rx+rw-10, ryy-86))
    
    qy = ry - 280
    if qy > FTR_H + 50:
        rrect(c, x, qy-44, cw, 40, 7, GREEN_DIM, GREEN, 0.8)
        tc(c, '"Stay consistent, stay disciplined."', x + cw/2, qy-16, 'P-Bold', 12, GREEN)
        tc(c, '- Ahmed Teka', x + cw/2, qy-32, 'P-Reg', 10, GRAY)
    
    c.showPage()

# ═══════════════════════════════════════════════
# PAGE 6 - COACH
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
    
    fill_rect(c, 0, H-48, W, 48, Color(0,0,0,0.8))
    hline(c, 0, H-48, W, GREEN_MID, 0.8)
    tl(c, 'AHMED', STRIPE_W+16, H-30, 'P-Bold', 18, GREEN_MID)
    tl(c, 'TEKA', STRIPE_W+82, H-30, 'P-Bold', 18, WHITE)
    tr(c, 'YOUR COACH', W-16, H-30, 'P-Reg', 9, GRAY_LIGHT)
    
    cy = H * 0.55
    tc(c, 'AHMED TEKA', W/2, cy, 'P-Bold', 48, GREEN_MID)
    tc(c, 'NUTRITION COACH', W/2, cy-34, 'P-Reg', 14, WHITE)
    
    fill_rect(c, 0, 0, W, 75, Color(0,0,0,0.8))
    hline(c, 0, 75, W, GREEN_MID, 0.7)
    
    btn_w = 150; btn_h = 32
    total_w = 2*btn_w + 12
    bx_start = W/2 - total_w/2
    
    for i, (lbl, color) in enumerate([
        ('@coach.teka1', GREEN_MID),
        ('01033047057', GOLD2),
    ]):
        bx = bx_start + i*(btn_w+12)
        by = 22
        rrect(c, bx, by, btn_w, btn_h, 5, Color(0,0,0,0.4), color, 1)
        tc(c, lbl, bx+btn_w/2, by+btn_h/2-4, 'P-Bold', 10, WHITE)
    
    tr(c, f'{TOTAL_PAGES} / {TOTAL_PAGES}', W-14, 85, 'P-Bold', 9, GREEN_MID)
    
    c.showPage()

# ═══════════════════════════════════════════════
# BUILD
# ═══════════════════════════════════════════════

def generate_nutrition_pdf(data):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    c.setTitle('AHMED TEKA - Nutrition Plan')
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
    return pdf_bytes