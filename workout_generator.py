import os
import io
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.colors import Color, HexColor
from config import *

W, H = A4

# Use built-in Helvetica as fallback for all platforms
from reportlab.lib.fonts import addMapping
addMapping('P-Bold', 0, 0, 'Helvetica-Bold')
addMapping('P-Med', 0, 0, 'Helvetica')
addMapping('P-Reg', 0, 0, 'Helvetica')
addMapping('P-Light', 0, 0, 'Helvetica')

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

def tl(c, s, x, y, f='P-Reg', sz=10, col=WHITE):
    c.setFillColor(col); c.setFont(f, sz); c.drawString(x, y, str(s))

def tc(c, s, x, y, f='P-Reg', sz=10, col=WHITE):
    c.setFillColor(col); c.setFont(f, sz); c.drawCentredString(x, y, str(s))

def tr(c, s, x, y, f='P-Reg', sz=10, col=WHITE):
    c.setFillColor(col); c.setFont(f, sz); c.drawRightString(x, y, str(s))

def hline(c, x, y, w, col=GOLD, lw=0.8):
    c.setStrokeColor(col); c.setLineWidth(lw); c.line(x, y, x+w, y)

def left_stripe(c):
    grad_v(c, 0, 0, STRIPE_W, H, GOLD4, GOLD3)

def wrap(c, text, x, y, maxw, f, sz, col, lh=None):
    lh = lh or sz * 1.55
    c.setFillColor(col); c.setFont(f, sz)
    words = text.split()
    line = []
    for word in words:
        if c.stringWidth(' '.join(line + [word]), f, sz) <= maxw:
            line.append(word)
        else:
            if line: c.drawString(x, y, ' '.join(line)); y -= lh
            line = [word]
    if line: c.drawString(x, y, ' '.join(line)); y -= lh
    return y

def content_area():
    x = STRIPE_W + M
    w = W - x - M
    return x, H - HDR_H - M, w

def chrome(c, section, pgnum, data, accent=GOLD):
    left_stripe(c)
    fill_rect(c, 0, H-HDR_H, W, HDR_H, Color(0.04, 0.06, 0.1, 1))
    hline(c, 0, H-HDR_H, W, accent, 1.0)
    tl(c, 'AHMED', STRIPE_W+12, H-HDR_H+17, 'P-Bold', 13, GOLD)
    tl(c, 'TEKA', STRIPE_W+68, H-HDR_H+17, 'P-Bold', 13, WHITE)
    tc(c, section, W/2, H-HDR_H+17, 'P-Med', 8.5, SILVER)
    fill_rect(c, 0, 0, W, FTR_H, Color(0.04, 0.06, 0.1, 1))
    hline(c, 0, FTR_H, W, accent, 0.7)
    tc(c, data.get('instagram','@coach.teka1'), W/2-60, FTR_H/2-4, 'P-Med', 7.5, GOLD)
    tc(c, data.get('phone','01033047057'), W/2+60, FTR_H/2-4, 'P-Reg', 7.5, SILVER)
    tr(c, f'{pgnum} / {TOTAL_PAGES}', W-12, FTR_H/2-4, 'P-Bold', 8.5, accent)

def p1_cover(c, data):
    fill_bg(c)
    grad_v(c, 0, 0, W, H, BG4, BG)
    c.setFillColor(Color(0,0,0,0.7))
    c.rect(0,0,W,H,stroke=0,fill=1)
    left_stripe(c)
    fill_rect(c,0,H-52,W,52,Color(0,0,0,0.85))
    hline(c,0,H-52,W,GOLD,1.2)
    tl(c,'AHMED',STRIPE_W+16,H-32,'P-Bold',18,GOLD)
    tl(c,'TEKA',STRIPE_W+84,H-32,'P-Bold',18,WHITE)
    hline(c,STRIPE_W+16,H-40,100,GOLD,0.6)
    ty=H-120
    tc(c,data.get('program','PUSH // PULL // LEGS').replace('//','●'),W/2,ty,'P-Bold',36,WHITE)
    rrect(c,W/2-35,ty-35,70,18,3,GOLD_DIM,GOLD,0.8)
    tc(c,'VOL.1',W/2,ty-29,'P-Bold',9,GOLD)
    by=130
    rrect(c,STRIPE_W+16,by,W-STRIPE_W-32,54,6,Color(0,0,0,0.78),GOLD,1.2)
    fill_rect(c,STRIPE_W+16,by,4,54,GOLD)
    tl(c,'CLIENT',STRIPE_W+28,by+40,'P-Light',7,GOLD)
    tl(c,data.get('client_name','CLIENT'),STRIPE_W+28,by+16,'P-Bold',28,WHITE)
    tr(c,data.get('goal','FITNESS'),W-24,by+30,'P-Med',8.5,GOLD)
    pw=(W-STRIPE_W-36)/3-5
    pills=[('DURATION',data.get('duration','8 WEEKS')),('FREQUENCY',data.get('frequency','6 DAYS/WK')),('START',data.get('start_date','JUNE 2026'))]
    for i,(lbl,val) in enumerate(pills):
        px=STRIPE_W+16+i*(pw+7.5)
        rrect(c,px,by-58,pw,50,4,Color(0,0,0,0.70),GOLD3,0.6)
        tl(c,lbl,px+10,by-24,'P-Light',7,GRAY)
        tl(c,val,px+10,by-44,'P-Bold',12,GOLD)
    fill_rect(c,0,0,W,40,Color(0,0,0,0.88))
    hline(c,0,40,W,GOLD,0.8)
    tl(c,data.get('instagram','@coach.teka1'),STRIPE_W+16,15,'P-Med',8,GOLD)
    tc(c,data.get('phone','01033047057'),W/2,15,'P-Reg',8,SILVER)
    tr(c,f'Coach {data.get("coach_name","AHMED TEKA")}',W-14,15,'P-Bold',9,GOLD)
    c.showPage()

def p2_intro(c, data):
    fill_bg(c)
    c.setFillColor(Color(0,0,0,0.75))
    c.rect(0,0,W,H,stroke=0,fill=1)
    chrome(c,'INTRODUCTION',2,data)
    x,y,cw=content_area()
    tl(c,'PROGRAM',x,y,'P-Bold',26,SILVER)
    tw=c.stringWidth('PROGRAM ','P-Bold',26)
    tl(c,'OVERVIEW',x+tw,y,'P-Bold',26,WHITE)
    hline(c,x,y-7,200,GOLD,1.5)
    wrap(c,data.get('philosophy',''),x+10,y-30,cw-20,'P-Reg',8.8,SILVER,lh=15)
    stats_y=FTR_H+M+52
    stats=[('8','WEEKS'),('3','SPLITS'),('6','DAYS/WK'),('24+','EXERCISES')]
    sw2=cw/4
    hline(c,x,stats_y+50,cw,Color(1,1,1,0.07),0.4)
    for i,(val,lbl) in enumerate(stats):
        sx=x+i*sw2
        rrect(c,sx,stats_y,sw2-5,34,4,BG3,GOLD_DIM,0.5)
        tc(c,val,sx+(sw2-5)/2,stats_y+22,'P-Bold',18,GOLD)
        tc(c,lbl,sx+(sw2-5)/2,stats_y+6,'P-Light',6.5,GRAY)
    c.showPage()

def p_exercise(c, data, day_key, pgnum, accent=GOLD):
    fill_bg(c)
    exercises=data.get('exercises',[])
    day_exercises=[ex for ex in exercises if ex.get('day','')==day_key]
    if not day_exercises:
        day_exercises=[ex for ex in exercises if ex.get('day','')=='']
    day_label=day_key.replace('_',' ').upper()
    chrome(c,f'{day_label} DAY',pgnum,data,accent)
    x,y,cw=content_area()
    tc(c,day_label,x+cw/2,y-10,'P-Bold',44,WHITE)
    tc(c,'EXERCISE SESSION',x+cw/2,y-32,'P-Med',10,accent)
    hline(c,x,y-40,cw,accent,1.0)
    cx_arr=[x,x+188,x+234,x+282,x+336]
    cw_arr=[188,46,48,54,cw-(336-x)]
    hdrs=['EXERCISE','SETS','REPS','REST','NOTES']
    ccx=[cx_arr[i]+cw_arr[i]/2 for i in range(5)]
    ey=y-60
    rrect(c,x,ey-TBL_HDR_H,cw,TBL_HDR_H,4,CHARCOAL,accent,0.7)
    fill_rect(c,x,ey-TBL_HDR_H,4,TBL_HDR_H,accent)
    for i,hdr in enumerate(hdrs):
        tc(c,hdr,ccx[i],ey-TBL_HDR_H+10,'P-Bold',8,accent)
    ey-=TBL_HDR_H
    for idx,ex in enumerate(day_exercises[:8]):
        rb=BG4 if idx%2==0 else BG3
        fill_rect(c,x,ey-ROW_H,cw,ROW_H,rb)
        fill_rect(c,x,ey-ROW_H,3,ROW_H,accent if idx%2==0 else GRAY2)
        tl(c,ex.get('name',f'Exercise {idx+1}'),cx_arr[0]+10,ey-12,'P-Bold',9.5,WHITE)
        desc=ex.get('desc','')[:56]+'..' if len(ex.get('desc',''))>56 else ex.get('desc','')
        tl(c,desc,cx_arr[0]+10,ey-24,'P-Reg',6.5,GRAY)
        tc(c,str(ex.get('sets','3')),ccx[1],ey-17,'P-Bold',13,accent)
        tc(c,str(ex.get('reps','10-12')),ccx[2],ey-17,'P-Med',9,OFF_WHITE)
        tc(c,str(ex.get('rest','90s')),ccx[3],ey-17,'P-Reg',8.5,SILVER)
        tc(c,'●',ccx[4],ey-17,'P-Bold',12,accent)
        ey-=ROW_H
    hline(c,x,ey,cw,accent,0.8)
    coach_y=ey-16
    tl(c,'COACH',x,coach_y-20,'P-Light',8,GRAY)
    tl(c,data.get('coach_name','AHMED TEKA'),x,coach_y-36,'P-Bold',16,GOLD)
    hline(c,x,coach_y-42,130,GOLD3,0.6)
    c.showPage()

def p7_tips(c, data):
    fill_bg(c)
    chrome(c,'TIPS & MOTIVATION',7,data)
    x,y,cw=content_area()
    tl(c,'TIPS FOR',x,y,'P-Bold',26,SILVER)
    tw=c.stringWidth('TIPS FOR ','P-Bold',26)
    tl(c,'BEST RESULTS',x+tw,y,'P-Bold',26,WHITE)
    hline(c,x,y-7,cw,GOLD,0.9)
    tips=[{'title':'CONSISTENCY','body':'Show up every training day. Consistency beats intensity.'},{'title':'PROGRESSIVE OVERLOAD','body':'Increase weight or reps each week to force adaptation.'},{'title':'NUTRITION','body':'Fuel your body with proper nutrition for optimal results.'},{'title':'REST & RECOVERY','body':'Sleep 7-9 hours. Muscles grow during rest, not training.'},{'title':'FORM FIRST','body':'Perfect form prevents injury and ensures targeted muscle activation.'},{'title':'HYDRATION','body':'Drink 4+ liters of water daily for peak performance.'}]
    GAP=10;COLS=2;ROWS=3
    cw2=(cw-GAP*(COLS-1))/COLS
    ch2=90
    for i,tip in enumerate(tips):
        col_=i%COLS;row_=i//COLS
        tx=x+col_*(cw2+GAP)
        ty=y-24-row_*(ch2+GAP)
        rrect(c,tx,ty-ch2,cw2,ch2,6,BG3,GOLD3,0.5)
        fill_rect(c,tx,ty-ch2,3,ch2,GOLD3)
        fill_rect(c,tx,ty-2,cw2,2,GOLD)
        c.setFillColor(GOLD_DIM);c.circle(tx+20,ty-18,12,fill=1,stroke=0)
        tc(c,str(i+1),tx+20,ty-22,'P-Bold',9.5,GOLD)
        tl(c,tip['title'],tx+40,ty-14,'P-Bold',11,WHITE)
        hline(c,tx+40,ty-20,80,GOLD3,0.5)
        wrap(c,tip['body'],tx+12,ty-34,cw2-18,'P-Reg',8,GRAY,lh=13)
    c.showPage()

def p8_coach(c, data):
    fill_bg(c)
    c.setStrokeColor(Color(0.2,0.3,0.5,0.06));c.setLineWidth(0.4)
    for i in range(0,int(W)+30,28):c.line(i,0,i,H)
    for j in range(0,int(H)+30,28):c.line(0,j,W,j)
    grad_v(c,0,0,W,H,BG4,BG)
    c.setFillColor(Color(0,0,0,0.55))
    c.rect(0,0,W,H,stroke=0,fill=1)
    left_stripe(c)
    fill_rect(c,0,H-50,W,50,Color(0,0,0,0.85))
    hline(c,0,H-50,W,GOLD,1.0)
    tl(c,'AHMED',STRIPE_W+16,H-32,'P-Bold',18,GOLD)
    tl(c,'TEKA',STRIPE_W+86,H-32,'P-Bold',18,WHITE)
    hline(c,STRIPE_W+16,H-39,106,GOLD,0.7)
    tr(c,'YOUR COACH',W-16,H-32,'P-Light',9,SILVER)
    cy=H*0.55
    lw_c=70
    c.setStrokeColor(GOLD);c.setLineWidth(1.5)
    c.line(W/2-200,cy+25,W/2-200+lw_c,cy+25)
    c.line(W/2+200-lw_c,cy+25,W/2+200,cy+25)
    tc(c,data.get('coach_name','AHMED TEKA'),W/2,cy,'P-Bold',48,GOLD)
    BOT_BAND=80
    fill_rect(c,0,0,W,BOT_BAND,Color(0,0,0,0.85))
    hline(c,0,BOT_BAND,W,GOLD,0.8)
    tc(c,data.get('instagram','@coach.teka1'),W/2-60,BOT_BAND/2-4,'P-Bold',11,WHITE)
    tc(c,data.get('phone','01033047057'),W/2+60,BOT_BAND/2-4,'P-Bold',11,WHITE)
    tr(c,f'{TOTAL_PAGES}/{TOTAL_PAGES}',W-14,BOT_BAND/2-4,'P-Bold',9,GOLD)
    c.showPage()

def generate_pdf(data):
    buffer=io.BytesIO()
    c=canvas.Canvas(buffer,pagesize=A4)
    c.setTitle(f'AHMED TEKA - {data.get("program","Workout Plan")}')
    c.setAuthor(data.get('coach_name','AHMED TEKA'))
    p1_cover(c,data)
    p2_intro(c,data)
    days=[('push_day',4,GOLD),('pull_day',5,GOLD2),('legs_day',6,GOLD3)]
    for day_key,pgnum,accent in days:
        p_exercise(c,data,day_key,pgnum,accent)
    p7_tips(c,data)
    p8_coach(c,data)
    c.save()
    pdf_bytes=buffer.getvalue()
    buffer.close()
    return pdf_bytes
