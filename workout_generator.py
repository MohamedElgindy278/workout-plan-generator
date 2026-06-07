import os
import io
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.colors import Color, HexColor
from config import *

W, H = A4

# ═══════════════════════════════════════════════
# FONTS - Use built-in Helvetica for cloud
# ═══════════════════════════════════════════════

# ═══════════════════════════════════════════════
# PRIMITIVES
# ═══════════════════════════════════════════════

def fill_bg(c, col=None):
    c.setFillColor(col or BG)
    c.rect(0, 0, W, H, stroke=0, fill=1)

def fill_rect(c, x, y, w, h, col):
    c.setFillColor(col)
    c.rect(x, y, w, h, stroke=0, fill=1)

def rrect(c, x, y, w, h, r, fc, sc=None, sw=0.8):
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

def grad_v(c, x, y, w, h, c1, c2, n=40):
    r1,g1,b1 = c1.red, c1.green, c1.blue
    r2,g2,b2 = c2.red, c2.green, c2.blue
    sh = h/n
    for i in range(n):
        t = i/n
        c.setFillColor(Color(r1+(r2-r1)*t, g1+(g2-g1)*t, b1+(b2-b1)*t))
        c.rect(x, y+h-(i+1)*sh, w, sh+0.6, stroke=0, fill=1)

def tl(c, s, x, y, f='Helvetica', sz=10, col=WHITE):
    c.setFillColor(col); c.setFont(f, sz); c.drawString(x, y, str(s))

def tc(c, s, x, y, f='Helvetica', sz=10, col=WHITE):
    c.setFillColor(col); c.setFont(f, sz); c.drawCentredString(x, y, str(s))

def tr(c, s, x, y, f='Helvetica', sz=10, col=WHITE):
    c.setFillColor(col); c.setFont(f, sz); c.drawRightString(x, y, str(s))

def hline(c, x, y, w, col=GOLD, lw=0.8):
    c.setStrokeColor(col); c.setLineWidth(lw); c.line(x, y, x+w, y)

def vline(c, x, y0, y1, col=GRAY2, lw=0.5):
    c.setStrokeColor(col); c.setLineWidth(lw); c.line(x, y0, x, y1)

def diamond(c, cx, cy, sz, col):
    p = c.beginPath()
    p.moveTo(cx, cy+sz); p.lineTo(cx+sz*0.55, cy)
    p.lineTo(cx, cy-sz); p.lineTo(cx-sz*0.55, cy); p.close()
    c.setFillColor(col); c.drawPath(p, fill=1, stroke=0)

def left_stripe(c):
    grad_v(c, 0, 0, STRIPE_W, H, GOLD4, GOLD3)

def wrap(c, text, x, y, maxw, f, sz, col, lh=None):
    lh = lh or sz * 1.55
    c.setFillColor(col); c.setFont(f, sz)
    for para in text.split('\n\n'):
        line = []
        for word in para.replace('\n', ' ').split():
            if c.stringWidth(' '.join(line + [word]), f, sz) <= maxw:
                line.append(word)
            else:
                if line: c.drawString(x, y, ' '.join(line)); y -= lh
                line = [word]
        if line: c.drawString(x, y, ' '.join(line)); y -= lh
        y -= lh * 0.35
    return y

def content_area():
    x = STRIPE_W + M
    w = W - x - M
    return x, H - HDR_H - M, w

# ═══════════════════════════════════════════════
# SHARED CHROME
# ═══════════════════════════════════════════════

def chrome(c, section, pgnum, data, accent=GOLD):
    left_stripe(c)
    fill_rect(c, 0, H-HDR_H, W, HDR_H, Color(0.04, 0.06, 0.1, 1))
    hline(c, 0, H-HDR_H, W, accent, 1.0)
    tl(c, 'AHMED', STRIPE_W+12, H-HDR_H+17, 'Helvetica-Bold', 13, GOLD)
    tl(c, 'TEKA', STRIPE_W+68, H-HDR_H+17, 'Helvetica-Bold', 13, WHITE)
    tc(c, section, W/2, H-HDR_H+17, 'Helvetica', 8.5, SILVER)
    fill_rect(c, 0, 0, W, FTR_H, Color(0.04, 0.06, 0.1, 1))
    hline(c, 0, FTR_H, W, accent, 0.7)
    ig_x = STRIPE_W + 12
    c.setStrokeColor(GOLD); c.setLineWidth(0.7)
    c.roundRect(ig_x, FTR_H/2-6, 11, 11, 2.5, fill=0, stroke=1)
    c.circle(ig_x+5.5, FTR_H/2, 3, fill=0, stroke=1)
    c.setFillColor(GOLD); c.circle(ig_x+9, FTR_H/2+4.5, 1.2, fill=1, stroke=0)
    tl(c, data.get('instagram','@coach.teka1'), ig_x+15, FTR_H/2-4, 'Helvetica', 7.5, GOLD)
    tc(c, data.get('phone','01033047057'), W/2, FTR_H/2-4, 'Helvetica', 7.5, SILVER)
    tr(c, f'{pgnum} / {TOTAL_PAGES}', W-12, FTR_H/2-4, 'Helvetica-Bold', 8.5, accent)

# ═══════════════════════════════════════════════
# PAGE 1 — COVER
# ═══════════════════════════════════════════════

def p1_cover(c, data):
    fill_bg(c)
    
    # Try to load cover photo
    cover_photo = data.get('photo_cover', '')
    try:
        if cover_photo and os.path.exists(cover_photo):
            c.drawImage(cover_photo, 0, 0, W, H, preserveAspectRatio=True)
        else:
            raise Exception()
    except:
        grad_v(c, 0, 0, W, H, BG4, BG)
    
    c.setFillColor(Color(0, 0, 0, alpha=0.55))
    c.rect(0, 0, W, H, stroke=0, fill=1)
    left_stripe(c)
    
    # TOP BAR
    fill_rect(c, 0, H-52, W, 52, Color(0,0,0,0.85))
    hline(c, 0, H-52, W, GOLD, 1.2)
    tl(c, 'AHMED', STRIPE_W+16, H-32, 'Helvetica-Bold', 18, GOLD)
    tl(c, 'TEKA', STRIPE_W+84, H-32, 'Helvetica-Bold', 18, WHITE)
    hline(c, STRIPE_W+16, H-40, 100, GOLD, 0.6)
    tr(c, data.get('tagline', 'ENGINEERED FOR DOMINANCE'), W-16, H-32, 'Helvetica', 8.5, SILVER)
    
    # MAIN TITLE
    ty = H - 120
    c.setStrokeColor(Color(1,1,1,0.4)); c.setLineWidth(1.2)
    c.line(STRIPE_W+20, ty+30, STRIPE_W+20+50, ty+30)
    c.line(W-20-50, ty+30, W-20, ty+30)
    
    program = data.get('program', 'PUSH // PULL // LEGS')
    words = program.replace('//', '●').split()
    
    c.setFont('Helvetica-Bold', 36)
    w1 = c.stringWidth(words[0] if len(words)>0 else 'PUSH', 'Helvetica-Bold', 36)
    w2 = c.stringWidth(words[2] if len(words)>2 else 'PULL', 'Helvetica-Bold', 36)
    w3 = c.stringWidth(words[4] if len(words)>4 else 'LEGS', 'Helvetica-Bold', 36)
    dot_w = c.stringWidth('●', 'Helvetica-Bold', 28)
    
    total_elements = 5
    gap = (W - (w1 + w2 + w3 + dot_w*2)) / (total_elements + 1)
    
    x1 = gap + w1/2
    x_dot1 = x1 + w1/2 + gap + dot_w/2
    x2 = x_dot1 + dot_w/2 + gap + w2/2
    x_dot2 = x2 + w2/2 + gap + dot_w/2
    x3 = x_dot2 + dot_w/2 + gap + w3/2
    
    tc(c, words[0] if len(words)>0 else 'PUSH', x1, ty, 'Helvetica-Bold', 36, WHITE)
    tc(c, '●', x_dot1, ty-2, 'Helvetica-Bold', 28, GOLD2)
    tc(c, words[2] if len(words)>2 else 'PULL', x2, ty, 'Helvetica-Bold', 36, WHITE)
    tc(c, '●', x_dot2, ty-2, 'Helvetica-Bold', 28, GOLD2)
    tc(c, words[4] if len(words)>4 else 'LEGS', x3, ty, 'Helvetica-Bold', 36, GOLD)
    
    rrect(c, W/2-35, ty-35, 70, 18, 3, GOLD_DIM, GOLD, 0.8)
    tc(c, data.get('volume', 'VOL.1'), W/2, ty-29, 'Helvetica-Bold', 9, GOLD)
    
    # CLIENT CARD
    by = 130
    rrect(c, STRIPE_W+16, by, W-STRIPE_W-32, 54, 6, Color(0,0,0,0.78), GOLD, 1.2)
    fill_rect(c, STRIPE_W+16, by, 4, 54, GOLD)
    tl(c, 'CLIENT', STRIPE_W+28, by+40, 'Helvetica', 7, GOLD)
    tl(c, data.get('client_name', 'CLIENT'), STRIPE_W+28, by+16, 'Helvetica-Bold', 28, WHITE)
    tr(c, data.get('goal', 'FITNESS'), W-24, by+30, 'Helvetica', 8.5, GOLD)
    
    # INFO PILLS
    pw = (W - STRIPE_W - 36) / 3 - 5
    pills = [
        ('DURATION', data.get('duration', '8 WEEKS')),
        ('FREQUENCY', data.get('frequency', '6 DAYS/WK')),
        ('START', data.get('start_date', 'JUNE 2026'))
    ]
    for i, (lbl, val) in enumerate(pills):
        px = STRIPE_W + 16 + i * (pw + 7.5)
        rrect(c, px, by-58, pw, 50, 4, Color(0,0,0,0.70), GOLD3, 0.6)
        tl(c, lbl, px+10, by-24, 'Helvetica', 7, GRAY)
        tl(c, val, px+10, by-44, 'Helvetica-Bold', 12, GOLD)
    
    # FOOTER
    fill_rect(c, 0, 0, W, 40, Color(0,0,0,0.88))
    hline(c, 0, 40, W, GOLD, 0.8)
    tl(c, data.get('instagram', '@coach.teka1'), STRIPE_W+16, 15, 'Helvetica', 8, GOLD)
    tc(c, data.get('phone', '01033047057'), W/2, 15, 'Helvetica', 8, SILVER)
    tr(c, f'Coach {data.get("coach_name", "AHMED TEKA")}', W-14, 15, 'Helvetica-Bold', 9, GOLD)
    
    c.showPage()

# ═══════════════════════════════════════════════
# PAGE 2 — INTRODUCTION
# ═══════════════════════════════════════════════

def p2_intro(c, data):
    fill_bg(c)
    
    intro_photo = data.get('photo_intro', '')
    try:
        if intro_photo and os.path.exists(intro_photo):
            c.drawImage(intro_photo, 0, 0, W, H, preserveAspectRatio=True)
    except:
        pass
    
    c.setFillColor(Color(0, 0, 0, alpha=0.75))
    c.rect(0, 0, W, H, stroke=0, fill=1)
    chrome(c, 'INTRODUCTION', 2, data)
    x, y, cw = content_area()
    
    c.setFillColor(Color(1,1,1,0.015)); c.setFont('Helvetica-Bold', 120)
    c.drawString(M-4, FTR_H+6, 'PPL')
    
    tl(c, 'THE', x, y, 'Helvetica-Bold', 26, SILVER)
    tw = c.stringWidth('THE ', 'Helvetica-Bold', 26)
    tl(c, 'PHILOSOPHY', x+tw, y, 'Helvetica-Bold', 26, WHITE)
    hline(c, x, y-7, 200, GOLD, 1.5)
    hline(c, x, y-10, cw, Color(1,1,1,0.06), 0.4)
    
    COL_G = 18
    lw2 = cw * 0.54 - COL_G/2
    rw = cw * 0.46 - COL_G/2
    rx = x + lw2 + COL_G
    
    py = y - 26
    py = wrap(c, data.get('philosophy', ''), x, py, lw2, 'Helvetica', 8.8, SILVER, lh=15)
    
    pq_y = py - 16
    fill_rect(c, x, pq_y-46, 3, 42, GOLD)
    tl(c, '"', x+12, pq_y-5, 'Helvetica', 38, Color(0.83,0.69,0.22,0.22))
    tl(c, 'Train with intention.', x+16, pq_y-16, 'Helvetica', 11.5, GOLD3)
    tl(c, 'Progress with patience.', x+16, pq_y-32, 'Helvetica', 11.5, GOLD3)
    
    stats_y = FTR_H + M + 52
    stats = [('8','WEEKS'), ('3','SPLITS'), ('6','DAYS/WK'), ('24+','EXERCISES')]
    sw2 = lw2 / 4
    hline(c, x, stats_y+50, lw2, Color(1,1,1,0.07), 0.4)
    tl(c, 'PROGRAM AT A GLANCE', x, stats_y+42, 'Helvetica', 7.5, GRAY)
    for i, (val, lbl) in enumerate(stats):
        sx = x + i * sw2
        rrect(c, sx, stats_y, sw2-5, 34, 4, BG3, GOLD_DIM, 0.5)
        tc(c, val, sx+(sw2-5)/2, stats_y+22, 'Helvetica-Bold', 18, GOLD)
        tc(c, lbl, sx+(sw2-5)/2, stats_y+6, 'Helvetica', 6.5, GRAY)
    
    # TIMELINE
    ty2 = y - 2
    tl(c, 'PROGRAM TIMELINE', rx, ty2, 'Helvetica-Bold', 11, GOLD)
    hline(c, rx, ty2-5, rw, GOLD3, 0.5)
    ty2 -= 18
    
    timeline = data.get('timeline', [
        {'week': 'WEEK 1-2', 'phase': 'FOUNDATION', 'desc': 'Master form and build mind-muscle connection.'},
        {'week': 'WEEK 3-4', 'phase': 'PROGRESSION', 'desc': 'Increase load by 5-10%. Volume increases.'},
        {'week': 'WEEK 5-6', 'phase': 'INTENSIFICATION', 'desc': 'Push beyond comfort zones.'},
        {'week': 'WEEK 7-8', 'phase': 'PEAK OUTPUT', 'desc': 'Maximum effort on all lifts.'},
    ])
    
    for i, ph in enumerate(timeline):
        ch = 74
        rrect(c, rx, ty2-ch, rw, ch, 5, BG3, GOLD3 if i>0 else GOLD, 0.6)
        fill_rect(c, rx, ty2-ch, 3, ch, GOLD if i==0 else GOLD3)
        c.setFillColor(GOLD_DIM); c.circle(rx+16, ty2-14, 9, fill=1, stroke=0)
        tc(c, str(i+1), rx+16, ty2-18, 'Helvetica-Bold', 8.5, GOLD)
        tl(c, ph['week'], rx+32, ty2-11, 'Helvetica-Bold', 9.5, GOLD if i==0 else SILVER)
        tl(c, ph['phase'], rx+32, ty2-24, 'Helvetica', 8.5, WHITE)
        wrap(c, ph['desc'], rx+10, ty2-38, rw-16, 'Helvetica', 7.5, GRAY, lh=12)
        ty2 -= ch + 6
    
    sx2 = x + lw2 + COL_G/2
    c.setStrokeColor(GOLD3); c.setLineWidth(0.5); c.setDash([3, 7])
    c.line(sx2, y-18, sx2, stats_y+52); c.setDash([])
    
    c.showPage()

# ═══════════════════════════════════════════════
# PAGE 3 — WARM UP
# ═══════════════════════════════════════════════

def p3_warmup(c, data):
    fill_bg(c)
    chrome(c, 'WARM UP PROTOCOL', 3, data)
    x, y, cw = content_area()
    
    tl(c, 'WARM UP', x, y, 'Helvetica-Bold', 28, WHITE)
    hline(c, x, y-7, 130, GOLD, 1.5)
    tl(c, 'PRIME  ·  ACTIVATE  ·  PREVENT INJURY', x, y-20, 'Helvetica', 8.5, SILVER)
    hline(c, x, y-27, cw, Color(1,1,1,0.06), 0.4)
    
    warmup = data.get('warmup', {})
    cy = y - 48; ch1 = 66
    rrect(c, x, cy-ch1, cw, ch1, 6, BG4, GOLD, 1.0)
    fill_rect(c, x, cy-ch1, 4, ch1, GOLD)
    c.setFillColor(GOLD_DIM); c.circle(x+22, cy-ch1/2+2, 12, fill=1, stroke=0)
    c.setFillColor(GOLD); c.setFont('Helvetica-Bold', 11); c.drawCentredString(x+22, cy-ch1/2-2, '5')
    tl(c, 'CARDIO PHASE', x+44, cy-14, 'Helvetica-Bold', 12, GOLD)
    tl(c, 'DYNAMIC WARM-UP', x+44, cy-26, 'Helvetica', 7.5, GRAY)
    wrap(c, warmup.get('cardio', '5-10 MIN LIGHT CARDIO'), x+44, cy-40, cw-58, 'Helvetica', 8, SILVER, lh=13)
    
    btn_y = cy - ch1 - 14; btn_h = 96; btn_w = cw / 2 - 8
    for i, (lbl, note) in enumerate([
        ('UPPER BODY SEQUENCE', warmup.get('upper_note', '')),
        ('LOWER BODY SEQUENCE', warmup.get('lower_note', '')),
    ]):
        ac = GOLD if i == 0 else ACCENT
        bx = x + i * (btn_w + 16)
        fill_rect(c, bx+4, btn_y-btn_h-4, btn_w, btn_h, Color(0,0,0,0.5))
        rrect(c, bx, btn_y-btn_h, btn_w, btn_h, 6, BG3, ac, 1.0)
        fill_rect(c, bx, btn_y-3, btn_w, 3, ac)
        fill_rect(c, bx, btn_y-btn_h, 3, btn_h, ac)
        tl(c, 'WATCH ON YOUTUBE', bx+14, btn_y-14, 'Helvetica', 6.5, GRAY)
        tl(c, lbl, bx+14, btn_y-28, 'Helvetica-Bold', 11, WHITE)
        hline(c, bx+14, btn_y-34, 90, ac, 0.8)
        wrap(c, note, bx+14, btn_y-48, btn_w-24, 'Helvetica', 7.5, GRAY, lh=12)
        px2 = bx + btn_w - 34; py2 = btn_y - btn_h + 14
        c.setFillColor(ac); c.circle(px2+12, py2+10, 13, fill=1, stroke=0)
        tc(c, '>', px2+9, py2+7, 'Helvetica-Bold', 11, BG)
    
    # Protocol rules
    tp_y = btn_y - btn_h - 14; tp_h = 76
    rrect(c, x, tp_y-tp_h, cw, tp_h, 6, BG3, GOLD_DIM, 0.5)
    fill_rect(c, x, tp_y-tp_h, 4, tp_h, GOLD3)
    tl(c, 'WARM-UP PROTOCOL RULES', x+16, tp_y-14, 'Helvetica-Bold', 10.5, GOLD)
    hline(c, x+16, tp_y-20, cw-30, Color(1,1,1,0.08), 0.4)
    protocol = warmup.get('protocol', [
        'Never skip warm-up — injury prevention is non-negotiable',
        'Full range of motion on every drill',
        'Use warm-up sets: 50% > 75% > working weight',
        'Note restricted areas and spend extra time there',
    ])
    for ti, tip in enumerate(protocol):
        col_x = x + 16 + (ti % 2) * (cw / 2)
        row_y = tp_y - 32 - (ti // 2) * 16
        diamond(c, col_x + 4, row_y + 4, 3.5, GOLD)
        tl(c, tip, col_x + 12, row_y, 'Helvetica', 7.8, SILVER)
    
    c.showPage()

# ═══════════════════════════════════════════════
# EXERCISE PAGES (4, 5, 6)
# ═══════════════════════════════════════════════

def p_exercise(c, data, day_key, pgnum, accent=GOLD):
    fill_bg(c)
    
    exercises = data.get('exercises', [])
    day_exercises = [ex for ex in exercises if ex.get('day', '') == day_key]
    if not day_exercises:
        day_exercises = exercises[:8]
    
    day_names = {
        'push_day': {'label': 'PUSH', 'subtitle': 'CHEST · SHOULDERS · TRICEPS', 'desc': 'Prioritize chest activation on horizontal movements.'},
        'pull_day': {'label': 'PULL', 'subtitle': 'BACK · BICEPS · REAR DELTS', 'desc': 'Drive elbows — not hands — on all row variations.'},
        'legs_day': {'label': 'LEGS', 'subtitle': 'QUADS · HAMSTRINGS · GLUTES · CALVES', 'desc': 'Heavy compound movements first.'},
    }
    
    day_info = day_names.get(day_key, day_names['push_day'])
    
    chrome(c, f'{day_info["label"]} DAY', pgnum, data, accent)
    x, y, cw = content_area()
    
    c.saveState()
    c.setFillColor(Color(1, 1, 1, 0.045))
    c.setFont('Helvetica-Bold', 90)
    c.drawString(x-6, FTR_H+8, day_info['label'])
    c.restoreState()
    
    tc(c, day_info['label'], x + cw/2, y - 10, 'Helvetica-Bold', 44, WHITE)
    tc(c, day_info['subtitle'], x + cw/2, y - 32, 'Helvetica', 10, accent)
    hline(c, x, y - 40, cw, accent, 1.0)
    
    dy = y - 56
    wrap(c, day_info['desc'], x, dy, cw, 'Helvetica', 8.5, GRAY, lh=14)
    
    rn_y = dy - 34
    rrect(c, x, rn_y-18, cw, 17, 3, GOLD_PANEL, accent, 0.7)
    tc(c, 'REST 90-120 SECONDS BETWEEN ALL WORKING SETS', x + cw/2, rn_y - 11, 'Helvetica-Bold', 8.5, accent)
    
    cx_arr = [x, x+188, x+234, x+282, x+336]
    cw_arr = [188, 46, 48, 54, cw-(336-x)]
    hdrs = ['EXERCISE', 'SETS', 'REPS', 'REST', 'VIDEO']
    ccx = [cx_arr[i] + cw_arr[i]/2 for i in range(5)]
    
    ey = rn_y - 28
    rrect(c, x, ey-TBL_HDR_H, cw, TBL_HDR_H, 4, CHARCOAL, accent, 0.7)
    fill_rect(c, x, ey-TBL_HDR_H, 4, TBL_HDR_H, accent)
    for i, hdr in enumerate(hdrs):
        tc(c, hdr, ccx[i], ey-TBL_HDR_H+10, 'Helvetica-Bold', 8, accent)
    ey -= TBL_HDR_H
    
    for idx, ex in enumerate(day_exercises[:8]):
        rb = BG4 if idx % 2 == 0 else BG3
        fill_rect(c, x, ey-ROW_H, cw, ROW_H, rb)
        fill_rect(c, x, ey-ROW_H, 3, ROW_H, accent if idx % 2 == 0 else GRAY2)
        tl(c, ex.get('name', f'Exercise {idx+1}'), cx_arr[0]+10, ey-12, 'Helvetica-Bold', 9.5, WHITE)
        ds = ex.get('desc', '')[:56] + '..' if len(ex.get('desc', '')) > 56 else ex.get('desc', '')
        tl(c, ds, cx_arr[0]+10, ey-24, 'Helvetica', 6.5, GRAY)
        tc(c, str(ex.get('sets', '3')), ccx[1], ey-17, 'Helvetica-Bold', 13, accent)
        tc(c, str(ex.get('reps', '10-12')), ccx[2], ey-17, 'Helvetica', 9, OFF_WHITE)
        tc(c, str(ex.get('rest', '90s')), ccx[3], ey-17, 'Helvetica', 8.5, SILVER)
        bcx2 = ccx[4]; bcy = ey - ROW_H/2
        c.setFillColor(accent); c.circle(bcx2, bcy, 11, fill=1, stroke=0)
        tc(c, '>', bcx2-1, bcy-4, 'Helvetica-Bold', 9, BG)
        ey -= ROW_H
    
    hline(c, x, ey, cw, accent, 0.8)
    
    coach_y = ey - 16
    hline(c, x, coach_y - 4, cw, Color(1,1,1,0.05), 0.3)
    tl(c, 'COACH', x, coach_y - 20, 'Helvetica', 8, GRAY)
    tl(c, data.get('coach_name', 'AHMED TEKA'), x, coach_y - 36, 'Helvetica-Bold', 16, GOLD)
    hline(c, x, coach_y - 42, 130, GOLD3, 0.6)
    
    c.showPage()

# ═══════════════════════════════════════════════
# PAGE 7 — TIPS
# ═══════════════════════════════════════════════

def p7_tips(c, data):
    fill_bg(c)
    chrome(c, 'TIPS & MOTIVATION', 7, data)
    x, y, cw = content_area()
    
    tl(c, 'TIPS FOR', x, y, 'Helvetica-Bold', 26, SILVER)
    tw = c.stringWidth('TIPS FOR ', 'Helvetica-Bold', 26)
    tl(c, 'BEST RESULTS', x+tw, y, 'Helvetica-Bold', 26, WHITE)
    hline(c, x, y-7, cw, GOLD, 0.9)
    
    tips = data.get('tips', [
        {'title': 'PERFECT FORM', 'icon': '01', 'body': 'Every rep with perfect technique.'},
        {'title': 'PROGRESSIVE OVERLOAD', 'icon': '02', 'body': 'Add weight or reps weekly.'},
        {'title': 'SLEEP AS TRAINING', 'icon': '03', 'body': '7-9 hours nightly.'},
        {'title': 'FUEL YOUR SESSIONS', 'icon': '04', 'body': '1.8-2.2g protein per kg.'},
        {'title': 'HYDRATION DAILY', 'icon': '05', 'body': '4 liters of water minimum.'},
        {'title': 'MENTAL EDGE', 'icon': '06', 'body': 'Visualization increases power.'},
    ])
    
    GAP = 10; COLS = 2; ROWS = 3
    cw2 = (cw - GAP * (COLS-1)) / COLS
    ch2 = 90
    
    for i, tip in enumerate(tips[:6]):
        col_ = i % COLS; row_ = i // COLS
        tx = x + col_ * (cw2 + GAP)
        ty = y - 24 - row_ * (ch2 + GAP)
        rrect(c, tx, ty-ch2, cw2, ch2, 6, BG3, GOLD3, 0.5)
        fill_rect(c, tx, ty-ch2, 3, ch2, GOLD3)
        fill_rect(c, tx, ty-2, cw2, 2, GOLD)
        c.setFillColor(GOLD_DIM); c.circle(tx+20, ty-18, 12, fill=1, stroke=0)
        tc(c, tip.get('icon', str(i+1)), tx+20, ty-22, 'Helvetica-Bold', 9.5, GOLD)
        tl(c, tip['title'], tx+40, ty-14, 'Helvetica-Bold', 11, WHITE)
        hline(c, tx+40, ty-20, 80, GOLD3, 0.5)
        wrap(c, tip['body'], tx+12, ty-34, cw2-18, 'Helvetica', 8, GRAY, lh=13)
    
    # Quote
    qy = y - 24 - ROWS * (ch2 + GAP) - 12
    qh = 82
    rrect(c, x-2, qy-qh-2, cw+4, qh+4, 7, BG, GOLD3, 0.5)
    rrect(c, x, qy-qh, cw, qh, 6, Color(0.06,0.05,0.01,1), GOLD, 1.3)
    fill_rect(c, x, qy-2, cw, 2, GOLD)
    fill_rect(c, x, qy-qh, cw, 2, GOLD)
    fill_rect(c, x, qy-qh, 2, qh, GOLD)
    fill_rect(c, x+cw-2, qy-qh, 2, qh, GOLD)
    tl(c, '"', x+10, qy-7, 'Helvetica', 44, Color(0.83,0.69,0.22,0.20))
    tr(c, '"', x+cw-10, qy-qh+28, 'Helvetica', 44, Color(0.83,0.69,0.22,0.20))
    wrap(c, data.get('quote', 'THE BODY ACHIEVES WHAT THE MIND BELIEVES.'), x+22, qy-22, cw-44, 'Helvetica-Bold', 9.5, OFF_WHITE, lh=15)
    tr(c, data.get('quote_author', '— Ahmed Teka'), x+cw-14, qy-qh+14, 'Helvetica', 9, GOLD)
    
    c.showPage()

# ═══════════════════════════════════════════════
# PAGE 8 — COACH
# ═══════════════════════════════════════════════

def p8_coach(c, data):
    fill_bg(c)
    
    c.setStrokeColor(Color(0.2, 0.3, 0.5, 0.06)); c.setLineWidth(0.4)
    for i in range(0, int(W)+30, 28): c.line(i, 0, i, H)
    for j in range(0, int(H)+30, 28): c.line(0, j, W, j)
    
    coach_photo = data.get('photo_coach', '')
    try:
        if coach_photo and os.path.exists(coach_photo):
            c.drawImage(coach_photo, 0, 0, W, H, preserveAspectRatio=True)
        else:
            raise Exception()
    except:
        grad_v(c, 0, 0, W, H, BG4, BG)
    
    c.setFillColor(Color(0, 0, 0, alpha=0.55))
    c.rect(0, 0, W, H, stroke=0, fill=1)
    left_stripe(c)
    
    fill_rect(c, 0, H-50, W, 50, Color(0,0,0,0.85))
    hline(c, 0, H-50, W, GOLD, 1.0)
    tl(c, 'AHMED', STRIPE_W+16, H-32, 'Helvetica-Bold', 18, GOLD)
    tl(c, 'TEKA', STRIPE_W+86, H-32, 'Helvetica-Bold', 18, WHITE)
    hline(c, STRIPE_W+16, H-39, 106, GOLD, 0.7)
    tr(c, 'YOUR COACH', W-16, H-32, 'Helvetica', 9, SILVER)
    
    cy = H * 0.55
    lw_c = 70
    c.setStrokeColor(GOLD); c.setLineWidth(1.5)
    c.line(W/2 - 200, cy + 25, W/2 - 200 + lw_c, cy + 25)
    c.line(W/2 + 200 - lw_c, cy + 25, W/2 + 200, cy + 25)
    tc(c, data.get('coach_name', 'AHMED TEKA'), W/2, cy, 'Helvetica-Bold', 48, GOLD)
    
    BOT_BAND = 80
    fill_rect(c, 0, 0, W, BOT_BAND, Color(0,0,0,0.85))
    hline(c, 0, BOT_BAND, W, GOLD, 0.8)
    
    btn_h = 34; btn_w = 160; gap2 = 15
    total_btns = 2*btn_w + gap2
    bx_start = W/2 - total_btns/2
    
    for i, (lbl, ac) in enumerate([
        (data.get('instagram', '@coach.teka1'), GOLD),
        (data.get('phone', '01033047057'), ACCENT),
    ]):
        bx = bx_start + i*(btn_w+gap2)
        by = BOT_BAND/2 - btn_h/2
        fill_rect(c, bx+3, by-3, btn_w, btn_h, Color(0,0,0,0.5))
        rrect(c, bx, by, btn_w, btn_h, 5, Color(0.04,0.05,0.1,0.85), ac, 1.2)
        fill_rect(c, bx, by+btn_h-3, btn_w, 3, ac)
        tc(c, lbl, bx+btn_w/2, by+btn_h/2-4, 'Helvetica-Bold', 11, WHITE)
    
    tr(c, f'{TOTAL_PAGES} / {TOTAL_PAGES}', W-14, BOT_BAND/2-4, 'Helvetica-Bold', 9, GOLD)
    c.showPage()

# ═══════════════════════════════════════════════
# BUILD FUNCTION
# ═══════════════════════════════════════════════

def generate_pdf(data):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    c.setTitle(f'AHMED TEKA — {data.get("program", "Workout Plan")}')
    c.setAuthor(data.get('coach_name', 'AHMED TEKA'))
    c.setSubject('Professional Workout Plan')
    c.setCreator('Ahmed Teka PDF Engine v2')
    
    p1_cover(c, data)
    p2_intro(c, data)
    p3_warmup(c, data)
    p_exercise(c, data, 'push_day', 4, GOLD)
    p_exercise(c, data, 'pull_day', 5, GOLD2)
    p_exercise(c, data, 'legs_day', 6, GOLD3)
    p7_tips(c, data)
    p8_coach(c, data)
    
    c.save()
    pdf_bytes = buffer.getvalue()
    buffer.close()
    return pdf_bytes