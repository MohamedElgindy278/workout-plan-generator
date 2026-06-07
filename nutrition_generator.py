import os
import io
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.colors import Color, HexColor

W, H = A4

# ═══════════════════════════════════════════════
# COLORS - White + Green + Gold
# ═══════════════════════════════════════════════
BG          = HexColor('#FFFFFF')
BG_CREAM    = HexColor('#F8F8F8')
CARD_BG     = HexColor('#F0F7F4')
GREEN       = HexColor('#2E7D64')
GREEN_LIGHT = HexColor('#3A9B7A')
GOLD        = HexColor('#D4AF37')
GRAY_DARK   = HexColor('#4A4A4A')
GRAY        = HexColor('#666666')
GRAY_LIGHT  = HexColor('#999999')
BLACK_SOFT  = HexColor('#1A1A1A')
WHITE       = HexColor('#FFFFFF')
RED_SOFT    = HexColor('#E8D5D5')
GREEN_DIM   = HexColor('#E8F5F0')

TOTAL_PAGES = 6

# ═══════════════════════════════════════════════
# HELPERS
# ═══════════════════════════════════════════════

def fill_bg(c, col=None):
    c.setFillColor(col or BG)
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

def tl(c, s, x, y, f='Helvetica', sz=10, col=BLACK_SOFT):
    c.setFillColor(col); c.setFont(f, sz); c.drawString(x, y, str(s))

def tc(c, s, x, y, f='Helvetica', sz=10, col=BLACK_SOFT):
    c.setFillColor(col); c.setFont(f, sz); c.drawCentredString(x, y, str(s))

def tr(c, s, x, y, f='Helvetica', sz=10, col=BLACK_SOFT):
    c.setFillColor(col); c.setFont(f, sz); c.drawRightString(x, y, str(s))

def hline(c, x, y, w, col=GREEN, lw=1.0):
    c.setStrokeColor(col); c.setLineWidth(lw); c.line(x, y, x+w, y)

def circle(c, cx, cy, r, col):
    c.setFillColor(col); c.circle(cx, cy, r, fill=1, stroke=0)

def stripe(c):
    fill_rect(c, 0, 0, 4, H, GREEN)

def header_footer(c, page, title):
    # Header
    fill_rect(c, 0, H-36, W, 36, BG_CREAM)
    hline(c, 0, H-36, W, GREEN, 0.8)
    tl(c, 'AHMED TEKA', 16, H-24, 'Helvetica-Bold', 10, GREEN)
    tc(c, title, W/2, H-24, 'Helvetica', 8, GRAY)
    tr(c, 'Nutrition Plan', W-16, H-24, 'Helvetica-Bold', 10, GOLD)
    # Footer
    fill_rect(c, 0, 0, W, 28, BG_CREAM)
    hline(c, 0, 28, W, GREEN, 0.6)
    tl(c, '@coach.teka1', 16, 9, 'Helvetica', 7, GRAY)
    tc(c, '01033047057', W/2, 9, 'Helvetica', 7, GRAY)
    tr(c, f'{page} / {TOTAL_PAGES}', W-16, 9, 'Helvetica-Bold', 8, GREEN)

# ═══════════════════════════════════════════════
# PAGE 1 - COVER
# ═══════════════════════════════════════════════

def p1_cover(c, data):
    fill_bg(c)
    
    # Cover photo
    cover_photo = 'images/AhmedTeka_image1.jpeg'
    try:
        if os.path.exists(cover_photo):
            c.drawImage(cover_photo, 0, 0, W, H, preserveAspectRatio=True)
    except:
        pass
    
    c.setFillColor(Color(0, 0, 0, alpha=0.5))
    c.rect(0, 0, W, H, stroke=0, fill=1)
    stripe(c)
    
    # Top bar
    fill_rect(c, 0, H-40, W, 40, Color(0,0,0,0.4))
    tr(c, 'AHMED TEKA', W-16, H-26, 'Helvetica-Bold', 12, GREEN_LIGHT)
    
    # Title
    ty = H - 160
    tc(c, 'NUTRITION', W/2, ty + 50, 'Helvetica-Bold', 52, WHITE)
    tc(c, 'PLAN', W/2, ty, 'Helvetica-Bold', 52, GREEN_LIGHT)
    tc(c, 'Personalized Meal Plan', W/2, ty - 25, 'Helvetica', 11, Color(1,1,1,0.7))
    
    # Client card
    cy = ty - 90
    rrect(c, 20, cy, W-40, 55, 8, Color(0,0,0,0.6), GREEN, 1)
    tl(c, 'CLIENT', 32, cy+40, 'Helvetica', 7, GRAY_LIGHT)
    tl(c, data.get('client_name', 'CLIENT'), 32, cy+16, 'Helvetica-Bold', 22, WHITE)
    tr(c, data.get('goal', 'FITNESS'), W-32, cy+28, 'Helvetica', 9, GREEN_LIGHT)
    
    # Info pills
    ry = cy - 70
    pw = (W-50)/3
    pills = [
        ('DURATION', data.get('duration', '12 WEEKS')),
        ('MEALS', data.get('meals_count', '4 MEALS')),
        ('START', data.get('start_date', 'JUNE 2026')),
    ]
    for i, (lbl, val) in enumerate(pills):
        px = 20 + i*(pw+5)
        rrect(c, px, ry, pw-5, 45, 6, Color(0,0,0,0.5), GOLD, 0.5)
        tl(c, lbl, px+10, ry+30, 'Helvetica', 7, GRAY_LIGHT)
        tl(c, val, px+10, ry+10, 'Helvetica-Bold', 12, GREEN_LIGHT)
    
    # Bottom
    tr(c, f'Coach: {data.get("coach_name", "AHMED TEKA")}', W-20, 60, 'Helvetica-Bold', 12, WHITE)
    
    c.showPage()

# ═══════════════════════════════════════════════
# PAGE 2 - PROFILE
# ═══════════════════════════════════════════════

def p2_profile(c, data):
    fill_bg(c, BG_CREAM)
    header_footer(c, 2, 'CLIENT PROFILE')
    stripe(c)
    
    x = 20
    y = H - 70
    cw = W - 40
    
    tc(c, 'CLIENT PROFILE', W/2, y, 'Helvetica-Bold', 24, GREEN)
    hline(c, x, y-10, cw, GOLD, 1.2)
    y -= 35
    
    # Info cards
    info_items = [
        ('Full Name', data.get('full_name', 'N/A')),
        ('Age', data.get('age', 'N/A')),
        ('Weight', data.get('weight', 'N/A')),
        ('Height', data.get('height', 'N/A')),
        ('Goal', data.get('goal', 'N/A')),
    ]
    
    bw = (cw-20)/2
    for i, (lbl, val) in enumerate(info_items):
        col = i % 2
        row = i // 2
        cx = x + col*(bw+10)
        cy = y - row*55
        
        rrect(c, cx, cy-40, bw, 42, 6, WHITE, GREEN_DIM, 0.3)
        tl(c, lbl, cx+10, cy-12, 'Helvetica', 7, GRAY)
        tl(c, str(val), cx+10, cy-30, 'Helvetica-Bold', 12, BLACK_SOFT)
    
    y -= 175
    
    # Notes
    if data.get('notes'):
        rrect(c, x, y-45, cw, 42, 6, WHITE, GOLD, 0.5)
        tl(c, 'COACH NOTES', x+10, y-15, 'Helvetica-Bold', 9, GREEN)
        tl(c, str(data.get('notes', ''))[:80], x+10, y-32, 'Helvetica', 8, GRAY)
        y -= 55
    
    # Macros section
    tc(c, 'DAILY MACRONUTRIENTS', W/2, y, 'Helvetica-Bold', 16, GREEN)
    hline(c, x, y-8, cw, GOLD, 0.8)
    y -= 30
    
    macros = [
        ('PROTEIN', data.get('protein_g', '0'), 'g/day', GREEN),
        ('CARBS', data.get('carbs_g', '0'), 'g/day', GOLD),
        ('FAT', data.get('fat_g', '0'), 'g/day', GREEN_LIGHT),
    ]
    
    mw = (cw-30)/3
    for i, (lbl, val, unit, color) in enumerate(macros):
        mx = x + i*(mw+10)
        rrect(c, mx, y-55, mw, 52, 8, WHITE, color, 1)
        tc(c, lbl, mx+mw/2, y-15, 'Helvetica-Bold', 9, color)
        tc(c, val, mx+mw/2, y-35, 'Helvetica-Bold', 20, BLACK_SOFT)
        tc(c, unit, mx+mw/2, y-45, 'Helvetica', 7, GRAY)
    
    c.showPage()

# ═══════════════════════════════════════════════
# PAGE 3 - MEALS (Arabic with food icons)
# ═══════════════════════════════════════════════

def p3_meals(c, data):
    fill_bg(c, BG_CREAM)
    header_footer(c, 3, 'MEAL PLAN')
    stripe(c)
    
    x = 20
    y = H - 65
    cw = W - 40
    
    # Arabic title
    tc(c, 'خطة الوجبات اليومية', W/2, y, 'Helvetica-Bold', 22, GREEN)
    hline(c, x, y-8, cw, GOLD, 1)
    y -= 30
    
    meals = data.get('meals', [])
    food_icons = ['🍳', '💪', '🍗', '🥗', '🍝', '🥤']
    
    for i, meal in enumerate(meals[:6]):
        icon = food_icons[i] if i < len(food_icons) else '🍽️'
        mh = 105
        
        rrect(c, x, y-mh, cw, mh-3, 8, WHITE, GREEN_DIM, 0.3)
        
        # Icon circle
        circle(c, 40, y-22, 16, GREEN_DIM)
        tc(c, icon, 40, y-25, 'Helvetica', 14, BLACK_SOFT)
        
        # Meal name
        tl(c, f'Meal {i+1}: {meal.get("name", "")}', 62, y-12, 'Helvetica-Bold', 11, BLACK_SOFT)
        tl(c, meal.get('type', ''), 62, y-24, 'Helvetica', 8, GRAY)
        
        # Calories
        tl(c, f'{meal.get("calories", "0")} kcal', 62, y-40, 'Helvetica-Bold', 16, GREEN)
        
        # Macros
        tl(c, f'P: {meal.get("protein", "0")}g | C: {meal.get("carbs", "0")}g | F: {meal.get("fat", "0")}g', 62, y-52, 'Helvetica', 8, GRAY)
        
        # Ingredients
        ingredients = meal.get('ingredients', [])
        ing_text = ' | '.join(ingredients[:4]) if isinstance(ingredients, list) else str(ingredients)
        tl(c, ing_text[:80], 62, y-64, 'Helvetica', 7, GRAY)
        
        # Alternative
        alt = meal.get('alternative', '')
        if alt:
            tl(c, f'🔄 Alternative: {str(alt)[:70]}', 62, y-78, 'Helvetica', 7, GREEN)
        
        y -= mh + 4
    
    # Total calories
    if y > 80:
        rrect(c, x, y-40, cw, 36, 8, GREEN_DIM, GREEN, 1)
        tc(c, f'Total Daily Calories: {data.get("total_calories", "0")} kcal', W/2, y-18, 'Helvetica-Bold', 14, GREEN)
    
    c.showPage()

# ═══════════════════════════════════════════════
# PAGE 4 - GUIDELINES & SUPPLEMENTS
# ═══════════════════════════════════════════════

def p4_guidelines(c, data):
    fill_bg(c, BG_CREAM)
    header_footer(c, 4, 'GUIDELINES')
    stripe(c)
    
    x = 20
    y = H - 65
    cw = W - 40
    
    tc(c, 'DAILY GUIDELINES', W/2, y, 'Helvetica-Bold', 22, GREEN)
    hline(c, x, y-8, cw, GOLD, 1)
    y -= 30
    
    # Water card (big)
    rrect(c, x, y-55, cw, 50, 8, WHITE, GREEN, 1.5)
    tc(c, '💧 DAILY HYDRATION', W/2, y-18, 'Helvetica-Bold', 12, GREEN)
    tc(c, f'{data.get("water", "4-6 L")} of water per day', W/2, y-38, 'Helvetica-Bold', 18, BLACK_SOFT)
    y -= 65
    
    # Guidelines 2x2 grid
    guidelines = [
        ('⏰ Meal Timing', data.get('meal_timing', '2-3 hours between meals')),
        ('⚖️ Food Weighing', data.get('food_weighing', 'Weigh after cooking')),
        ('🥤 Drinks', data.get('drinks', 'No sugary drinks')),
        ('🚫 Avoid', data.get('sweets', 'No processed foods')),
    ]
    
    gw = (cw-15)/2
    for i, (title, body) in enumerate(guidelines):
        col = i % 2
        row = i // 2
        gx = x + col*(gw+10)
        gy = y - row*60
        
        rrect(c, gx, gy-48, gw, 44, 6, WHITE, GOLD, 0.4)
        tl(c, title, gx+8, gy-18, 'Helvetica-Bold', 10, GREEN)
        tl(c, str(body)[:50], gx+8, gy-34, 'Helvetica', 8, GRAY)
    
    y -= 140
    
    # Supplements
    tc(c, '💊 SUPPLEMENTS', W/2, y, 'Helvetica-Bold', 16, GREEN)
    hline(c, x, y-8, cw, GOLD, 0.6)
    y -= 25
    
    supplements = data.get('supplements', [])
    for i, sup in enumerate(supplements[:4]):
        rrect(c, x, y-30, cw, 26, 5, WHITE, GREEN_DIM, 0.3)
        circle(c, x+18, y-17, 10, GREEN)
        tc(c, str(i+1), x+18, y-20, 'Helvetica-Bold', 8, WHITE)
        tl(c, sup.get('name', ''), x+34, y-10, 'Helvetica-Bold', 10, BLACK_SOFT)
        tl(c, f'{sup.get("dose", "")} - {sup.get("benefit", "")}'[:60], x+34, y-22, 'Helvetica', 7, GRAY)
        y -= 35
    
    # Pre-workout
    if y > 80:
        tc(c, '⚡ PRE-WORKOUT PROTOCOL', W/2, y, 'Helvetica-Bold', 14, GREEN)
        hline(c, x, y-6, cw, GOLD, 0.5)
        y -= 20
        
        preworkout = data.get('preworkout', [])
        for pw in preworkout[:2]:
            rrect(c, x, y-28, cw, 24, 5, GREEN_DIM, GREEN, 0.3)
            tl(c, f'{pw.get("time", "")}: {pw.get("item", "")}'[:70], x+10, y-14, 'Helvetica', 8, BLACK_SOFT)
            y -= 32
    
    c.showPage()

# ═══════════════════════════════════════════════
# PAGE 5 - RECIPES
# ═══════════════════════════════════════════════

def p5_recipes(c, data):
    fill_bg(c, BG_CREAM)
    header_footer(c, 5, 'RECIPES')
    stripe(c)
    
    x = 20
    y = H - 65
    cw = W - 40
    
    tc(c, 'RECIPE LIBRARY', W/2, y, 'Helvetica-Bold', 22, GREEN)
    hline(c, x, y-8, cw, GOLD, 1)
    y -= 30
    
    recipes = data.get('recipes', [])
    rw = (cw-15)/3
    
    for i, recipe in enumerate(recipes[:6]):
        col = i % 3
        row = i // 3
        rx = x + col*(rw+7)
        ry = y - row*125
        
        rrect(c, rx, ry-110, rw, 106, 8, WHITE, GREEN_DIM, 0.3)
        
        # Icon
        circle(c, rx+rw/2, ry-40, 25, GREEN_DIM)
        circle(c, rx+rw/2, ry-40, 18, GREEN)
        tc(c, '🍽️', rx+rw/2, ry-44, 'Helvetica', 16, WHITE)
        
        tc(c, recipe.get('name', 'Recipe')[:20], rx+rw/2, ry-72, 'Helvetica-Bold', 9, BLACK_SOFT)
        tc(c, recipe.get('desc', '')[:30], rx+rw/2, ry-84, 'Helvetica', 7, GRAY)
        
        # Watch button
        rrect(c, rx+8, ry-106, rw-16, 18, 4, GREEN)
        tc(c, '▶ Watch Recipe', rx+rw/2, ry-98, 'Helvetica-Bold', 7, WHITE)
        
        link = recipe.get('link', '#')
        if link and link != '#':
            c.linkURL(link, (rx+8, ry-106, rx+rw-8, ry-88))
    
    y -= 280
    
    # Quote
    if y > 70:
        rrect(c, x, y-50, cw, 46, 8, GREEN_DIM, GREEN, 1)
        tc(c, '"Consistency is the key to success."', W/2, y-16, 'Helvetica-Bold', 12, GREEN)
        tc(c, f'— {data.get("coach_name", "AHMED TEKA")}', W/2, y-34, 'Helvetica', 10, GRAY)
    
    c.showPage()

# ═══════════════════════════════════════════════
# PAGE 6 - COACH
# ═══════════════════════════════════════════════

def p6_coach(c, data):
    fill_bg(c)
    
    # Coach photo
    coach_photo = 'images/AhmedTeka_image3.jpeg'
    try:
        if os.path.exists(coach_photo):
            c.drawImage(coach_photo, 0, 0, W, H, preserveAspectRatio=True)
    except:
        pass
    
    c.setFillColor(Color(0, 0, 0, alpha=0.5))
    c.rect(0, 0, W, H, stroke=0, fill=1)
    stripe(c)
    
    # Top bar
    fill_rect(c, 0, H-38, W, 38, Color(0,0,0,0.4))
    tl(c, 'AHMED TEKA', 16, H-26, 'Helvetica-Bold', 11, GREEN_LIGHT)
    tr(c, 'YOUR COACH', W-16, H-26, 'Helvetica', 9, GRAY_LIGHT)
    
    # Center name
    tc(c, data.get('coach_name', 'AHMED TEKA'), W/2, H/2+10, 'Helvetica-Bold', 42, WHITE)
    tc(c, 'NUTRITION COACH', W/2, H/2-25, 'Helvetica', 14, GREEN_LIGHT)
    
    # Bottom bar
    fill_rect(c, 0, 0, W, 70, Color(0,0,0,0.6))
    hline(c, 0, 70, W, GREEN, 1)
    
    # Contact buttons
    btn_w = 140; btn_h = 32
    total_w = 2*btn_w + 15
    bx_start = W/2 - total_w/2
    
    for i, (lbl, color) in enumerate([
        (f'@{data.get("instagram", "coach.teka1")}', GREEN),
        (data.get('phone', '01033047057'), GOLD),
    ]):
        bx = bx_start + i*(btn_w+15)
        by = 20
        rrect(c, bx, by, btn_w, btn_h, 5, Color(0,0,0,0.5), color, 1)
        tc(c, lbl, bx+btn_w/2, by+btn_h/2-4, 'Helvetica-Bold', 10, WHITE)
    
    c.showPage()

# ═══════════════════════════════════════════════
# BUILD
# ═══════════════════════════════════════════════

def generate_nutrition_pdf(data):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    c.setTitle(f'AHMED TEKA - Nutrition Plan')
    c.setAuthor(data.get('coach_name', 'AHMED TEKA'))
    
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