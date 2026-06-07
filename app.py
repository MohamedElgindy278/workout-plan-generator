import streamlit as st
from datetime import datetime
from workout_generator import generate_pdf

st.set_page_config(page_title='AHMED TEKA - Premium Workout Plan', page_icon='💪', layout='wide')

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;900&display=swap');
*{font-family:'Cairo',sans-serif!important}
.main-header{background:linear-gradient(135deg,#080B12,#1A2235);padding:1.5rem;border-radius:15px;text-align:center;border:2px solid #D4AF37;margin-bottom:1.5rem}
.main-header h1{color:#D4AF37;font-size:2rem;font-weight:900;margin:0}
.main-header p{color:#9BA3B2;margin:0.3rem 0 0 0}
.stButton>button{background:linear-gradient(135deg,#D4AF37,#A0832A);color:#080B12;font-weight:700;font-size:1.2rem;padding:1rem;border-radius:10px;border:none;width:100%}
.gen-btn>button{background:linear-gradient(135deg,#FF6B35,#D4AF37)!important;color:#000!important;font-size:1.5rem!important;padding:1.5rem!important;font-weight:900!important;animation:pulse 1.5s infinite}
@keyframes pulse{0%{box-shadow:0 0 0 0 rgba(212,175,55,0.4)}70%{box-shadow:0 0 0 25px rgba(212,175,55,0)}100%{box-shadow:0 0 0 0 rgba(212,175,55,0)}}
label{color:#D4AF37!important;font-weight:600!important}
input,textarea,select{background-color:#1A2235!important;color:#E8E4DC!important;border:2px solid #374151!important;border-radius:8px!important}
.exercise-card{background:#111827;border:1px solid #374151;border-radius:10px;padding:1rem;margin:0.5rem 0}
.exercise-card:hover{border-color:#D4AF37}
.day-header{background:linear-gradient(135deg,#1A2235,#080B12);padding:1rem;border-radius:10px;border-left:5px solid #D4AF37;margin:1rem 0}
.day-header h3{color:#D4AF37;margin:0}
.success-box{background:linear-gradient(135deg,#1C1A08,#2A2208);border:2px solid #D4AF37;border-radius:10px;padding:2rem;text-align:center;color:#D4AF37;font-size:1.5rem;font-weight:900}
.tooltip-icon{cursor:help;color:#D4AF37;font-size:0.9rem}
.section-desc{color:#6B7280;font-size:0.85rem;margin-bottom:1rem}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-header"><h1>🏋️ AHMED TEKA — PREMIUM WORKOUT PLAN</h1><p>Professional · Dark Premium · World-Class Quality</p></div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════
# PROGRAM CONFIGURATIONS
# ═══════════════════════════════════════════════
PROGRAM_CONFIGS = {
    'PUSH // PULL // LEGS': {
        'days': [
            {'key': 'push_day', 'label': 'PUSH', 'subtitle': 'CHEST · SHOULDERS · TRICEPS',
             'desc': 'Prioritize chest activation on horizontal movements, shoulder engagement on overhead work, and full tricep lockout on isolation exercises. Quality of contraction over quantity of weight.',
             'rest_note': 'REST 90-120 SECONDS BETWEEN ALL WORKING SETS'},
            {'key': 'pull_day', 'label': 'PULL', 'subtitle': 'BACK · BICEPS · REAR DELTS',
             'desc': 'Drive elbows — not hands — on all row variations. Maintain scapular retraction throughout. Feel the lats stretch at full extension on every pulldown and row.',
             'rest_note': 'REST 90-120 SECONDS BETWEEN ALL WORKING SETS'},
            {'key': 'legs_day', 'label': 'LEGS', 'subtitle': 'QUADS · HAMSTRINGS · GLUTES · CALVES',
             'desc': 'Heavy compound movements first. Never skip posterior chain work. Drive through the full foot on every squat variation — heel to toe engagement.',
             'rest_note': 'REST 2 FULL MINUTES AFTER SQUATS AND LEG PRESS'},
        ]
    },
    'ARNOLD SPLIT': {
        'days': [
            {'key': 'chest_back_day', 'label': 'CHEST & BACK', 'subtitle': 'CHEST · LATS · RHOMBOIDS',
             'desc': 'Superset chest and back movements for maximum pump and efficiency. Agonist-antagonist pairing increases blood flow and recovery between sets.',
             'rest_note': 'REST 60-90 SECONDS BETWEEN SUPERSETS'},
            {'key': 'shoulders_arms_day', 'label': 'SHOULDERS & ARMS', 'subtitle': 'DELTS · BICEPS · TRICEPS',
             'desc': 'Focus on deltoid isolation (all three heads) followed by arm supersets for complete upper body pump.',
             'rest_note': 'REST 45-60 SECONDS BETWEEN SETS'},
            {'key': 'legs_day', 'label': 'LEGS & CORE', 'subtitle': 'QUADS · HAMSTRINGS · CALVES · ABS',
             'desc': 'Heavy leg compounds followed by targeted core work for complete lower body development.',
             'rest_note': 'REST 2 MINUTES AFTER HEAVY COMPOUNDS'},
        ]
    },
    'UPPER / LOWER': {
        'days': [
            {'key': 'upper_day', 'label': 'UPPER BODY', 'subtitle': 'CHEST · BACK · SHOULDERS · ARMS',
             'desc': 'Complete upper body workout. Start with heavy compounds, progress to isolation for maximum development.',
             'rest_note': 'REST 90-120S ON COMPOUNDS | 60S ON ISOLATION'},
            {'key': 'lower_day', 'label': 'LOWER BODY', 'subtitle': 'QUADS · HAMSTRINGS · GLUTES · CALVES',
             'desc': 'Full lower body session with both bilateral and unilateral work for balanced leg development.',
             'rest_note': 'REST 2 MINUTES ON HEAVY SETS'},
        ]
    },
    'BRO SPLIT': {
        'days': [
            {'key': 'chest_day', 'label': 'CHEST', 'subtitle': 'PECTORALS · FRONT DELTS',
             'desc': 'Full chest development with flat, incline, decline, and isolation fly movements.',
             'rest_note': 'REST 90 SECONDS BETWEEN SETS'},
            {'key': 'back_day', 'label': 'BACK', 'subtitle': 'LATS · TRAPS · RHOMBOIDS',
             'desc': 'Width and thickness focused back training. Row for thickness, pulldown for width.',
             'rest_note': 'REST 90 SECONDS BETWEEN SETS'},
            {'key': 'shoulders_day', 'label': 'SHOULDERS', 'subtitle': 'ALL DELTOID HEADS',
             'desc': 'Complete shoulder development. Front, side, and rear delts with pressing and raising.',
             'rest_note': 'REST 60-90 SECONDS BETWEEN SETS'},
            {'key': 'arms_day', 'label': 'ARMS', 'subtitle': 'BICEPS · TRICEPS · FOREARMS',
             'desc': 'Isolation work for maximum arm pump. Superset biceps and triceps for efficiency.',
             'rest_note': 'REST 45-60 SECONDS BETWEEN SETS'},
            {'key': 'legs_day', 'label': 'LEGS', 'subtitle': 'QUADS · HAMSTRINGS · GLUTES · CALVES',
             'desc': 'Complete leg day. Squat, hinge, lunge, and isolate for full lower body development.',
             'rest_note': 'REST 2 MINUTES ON HEAVY SETS'},
        ]
    },
    'FULL BODY': {
        'days': [
            {'key': 'full_body_a', 'label': 'FULL BODY A', 'subtitle': 'STRENGTH FOCUS',
             'desc': 'Full body workout emphasizing strength on main compound lifts with lower volume.',
             'rest_note': 'REST 2-3 MINUTES ON MAIN LIFTS'},
            {'key': 'full_body_b', 'label': 'FULL BODY B', 'subtitle': 'HYPERTROPHY FOCUS',
             'desc': 'Full body workout with higher volume and moderate weight for muscle growth.',
             'rest_note': 'REST 60-90 SECONDS BETWEEN SETS'},
        ]
    },
}

# ═══════════════════════════════════════════════
# SECTION 1: CLIENT INFO
# ═══════════════════════════════════════════════
st.markdown("## 📋 CLIENT INFORMATION")
st.markdown('<p class="section-desc">Fill in the basic client details. This information appears on the cover page of the PDF.</p>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
with col1:
    client_name = st.text_input('👤 Client Name', 'MOHAMED', 
        help='Full name of the client as it will appear prominently on the cover page and throughout the PDF.')
    weight = st.text_input('⚖️ Weight (kg)', '75', 
        help='Client current body weight in kilograms. Used for reference in the plan.')
    start_date = st.text_input('📅 Start Date', datetime.now().strftime('%B %Y').upper(), 
        help='The month and year the program starts. Example: JUNE 2026')
with col2:
    goal = st.text_input('🎯 Goal', 'HYPERTROPHY & STRENGTH', 
        help='Primary training goal. Examples: HYPERTROPHY, STRENGTH, FAT LOSS, ENDURANCE')
    volume = st.text_input('📊 Volume', 'VOL.1', 
        help='Program volume/phase identifier. Example: VOL.1, PHASE 2, MESOCYCLE 1')
    duration = st.text_input('⏱️ Duration', '8 WEEKS', 
        help='Total length of the program. Example: 8 WEEKS, 12 WEEKS, 6 WEEKS')
with col3:
    tagline = st.text_input('💬 Tagline', 'ENGINEERED FOR DOMINANCE', 
        help='A motivational tagline that appears on the cover under the program name.')
    frequency = st.text_input('🔄 Frequency', '6 DAYS / WEEK', 
        help='How many days per week the client trains. Example: 6 DAYS / WEEK, 5 DAYS / WEEK')
    
    program_type = st.selectbox('📋 Program Type', list(PROGRAM_CONFIGS.keys()), index=0,
        help='Select the training split type. This determines the day layout in the PDF. Choose the one that matches your client needs.')

# ═══════════════════════════════════════════════
# SECTION 2: COACH INFO
# ═══════════════════════════════════════════════
st.markdown("---")
st.markdown("## 🧑‍🏫 COACH INFORMATION")
st.markdown('<p class="section-desc">Your contact details. These appear in the footer of every page and on the last page.</p>', unsafe_allow_html=True)

col_c1, col_c2, col_c3 = st.columns(3)
with col_c1:
    coach_name = st.text_input('Coach Name', 'AHMED TEKA', 
        help='Your full name as the coach. Displayed on the cover and last page.')
with col_c2:
    instagram = st.text_input('Instagram Username', '@coach.teka1', 
        help='Your Instagram handle. Shown in the footer with an IG icon.')
with col_c3:
    phone = st.text_input('Phone Number', '01033047057', 
        help='Your contact number. Displayed in the footer of every page.')

instagram_link = st.text_input('Instagram Full Link', 'https://instagram.com/coach.teka1', 
    help='The full clickable Instagram URL. Used for the link in the PDF footer.')

# ═══════════════════════════════════════════════
# SECTION 3: PHILOSOPHY
# ═══════════════════════════════════════════════
st.markdown("---")
st.markdown("## 📖 PROGRAM PHILOSOPHY")
st.markdown('<p class="section-desc">This text appears on Page 2 (Introduction). Write your training philosophy, program overview, and what the client should expect.</p>', unsafe_allow_html=True)

philosophy = st.text_area('Training Philosophy', 
    value="This program is not about going through the motions. It is about training with intention, precision, and relentless focus. Every set, every rep, every second of rest is calculated to push your body beyond its limits and force adaptation.\n\nThe Push Pull Legs split allows optimal muscle recovery while maintaining high training frequency. You will train each muscle group twice per week across 6 sessions, with one full rest day for complete systemic recovery.\n\nAdhere strictly to prescribed rest intervals. Progressive overload — adding weight or reps each week — is your primary growth driver. Track every session. Outperform yesterday.",
    height=150,
    help='Write a comprehensive training philosophy. This appears on the Introduction page (Page 2) of the PDF. Include your approach, methodology, and motivational message.')

# ═══════════════════════════════════════════════
# SECTION 4: EXERCISES
# ═══════════════════════════════════════════════
st.markdown("---")
st.markdown(f"## 💪 {program_type} — EXERCISES")
st.markdown('<p class="section-desc">Configure exercises for each training day. Fill in the exercise name, sets, reps, rest time, description, and optional YouTube link.</p>', unsafe_allow_html=True)

config = PROGRAM_CONFIGS[program_type]
all_exercises = {}

for day_idx, day in enumerate(config['days']):
    st.markdown(f'<div class="day-header"><h3>🏆 Day {day_idx+1}: {day["label"]} — {day["subtitle"]}</h3></div>', unsafe_allow_html=True)
    
    # Day description and rest note
    ecol1, ecol2 = st.columns([2,1])
    with ecol1:
        day_desc = st.text_area(f'📝 Description — {day["label"]} Day', value=day['desc'], height=70, key=f'desc_{day["key"]}',
            help=f'A brief description of the {day["label"]} training day focus and methodology.')
    with ecol2:
        day_rest = st.text_input(f'⏱️ Rest Note — {day["label"]} Day', value=day['rest_note'], key=f'rest_{day["key"]}',
            help=f'Rest period instructions for the {day["label"]} day exercises.')
    
    # Number of exercises
    num_exercises = st.number_input(f'Number of exercises for {day["label"]} Day', min_value=1, max_value=20, value=8, key=f'num_{day["key"]}',
        help=f'How many exercises for {day["label"]} day? You can add up to 20 exercises per day.')
    
    st.markdown(f"**📋 Exercise List — {day['label']} Day**")
    
    # Column headers
    hcol1, hcol2, hcol3, hcol4, hcol5, hcol6 = st.columns([3, 1, 1, 1, 3, 2])
    with hcol1:
        st.markdown('<p style="color:#D4AF37;font-weight:700;font-size:0.8rem">🏋️ EXERCISE NAME</p>', unsafe_allow_html=True)
    with hcol2:
        st.markdown('<p style="color:#D4AF37;font-weight:700;font-size:0.8rem">🔢 SETS</p>', unsafe_allow_html=True)
    with hcol3:
        st.markdown('<p style="color:#D4AF37;font-weight:700;font-size:0.8rem">🔁 REPS</p>', unsafe_allow_html=True)
    with hcol4:
        st.markdown('<p style="color:#D4AF37;font-weight:700;font-size:0.8rem">⏸️ REST</p>', unsafe_allow_html=True)
    with hcol5:
        st.markdown('<p style="color:#D4AF37;font-weight:700;font-size:0.8rem">📝 DESCRIPTION / NOTES</p>', unsafe_allow_html=True)
    with hcol6:
        st.markdown('<p style="color:#D4AF37;font-weight:700;font-size:0.8rem">🔗 VIDEO LINK</p>', unsafe_allow_html=True)
    
    day_exercises = []
    
    for ex_idx in range(int(num_exercises)):
        exc1, exc2, exc3, exc4, exc5, exc6 = st.columns([3, 1, 1, 1, 3, 2])
        with exc1:
            ex_name = st.text_input('Ex Name', value='', placeholder=f'Ex: BENCH PRESS', key=f'name_{day["key"]}_{ex_idx}', label_visibility='collapsed')
        with exc2:
            ex_sets = st.text_input('Sets', value='3', key=f'sets_{day["key"]}_{ex_idx}', label_visibility='collapsed')
        with exc3:
            ex_reps = st.text_input('Reps', value='10-12', key=f'reps_{day["key"]}_{ex_idx}', label_visibility='collapsed')
        with exc4:
            ex_rest = st.text_input('Rest', value='90s', key=f'rest_{day["key"]}_{ex_idx}', label_visibility='collapsed')
        with exc5:
            ex_desc = st.text_input('Description', value='', placeholder='Full ROM. Control movement.', key=f'descinput_{day["key"]}_{ex_idx}', label_visibility='collapsed')
        with exc6:
            ex_link = st.text_input('Video Link', value='#', key=f'link_{day["key"]}_{ex_idx}', label_visibility='collapsed')
        
        if ex_name.strip():
            day_exercises.append({
                'name': ex_name.strip(),
                'sets': ex_sets.strip() or '3',
                'reps': ex_reps.strip() or '10-12',
                'rest': ex_rest.strip() or '90s',
                'desc': ex_desc.strip() or 'Full ROM. Control the movement.',
                'link': ex_link.strip() or '#',
                'day': day['key']
            })
    
    all_exercises[day['key']] = {
        'exercises': day_exercises,
        'desc': day_desc,
        'rest_note': day_rest,
        'label': day['label'],
        'subtitle': day['subtitle']
    }

# ═══════════════════════════════════════════════
# SECTION 5: WARMUP
# ═══════════════════════════════════════════════
st.markdown("---")
with st.expander("🔥 WARM-UP PROTOCOL (Click to Edit)", expanded=False):
    st.markdown('<p class="section-desc">Configure the warm-up section. This appears on Page 3 of the PDF.</p>', unsafe_allow_html=True)
    
    wu_cardio = st.text_area('🏃 Cardio Phase', '5-10 MIN LIGHT CARDIO: Treadmill or bike at 60-65% max heart rate. Goal: elevate core temperature, increase joint lubrication, prime the cardiovascular system for heavy training.', height=70,
        help='Instructions for the initial cardio warm-up phase.')
    
    wc1, wc2 = st.columns(2)
    with wc1:
        wu_upper = st.text_area('💪 Upper Body Warm-Up Sequence', 'Shoulder circles, band pull-aparts, arm swings, chest openers, thoracic rotations. Perform 2 full rounds before every Push and Pull session.', height=100,
            help='Upper body dynamic warm-up exercises and instructions.')
    with wc2:
        wu_lower = st.text_area('🦵 Lower Body Warm-Up Sequence', 'Hip circles, leg swings, bodyweight squats, ankle rotations, glute bridges. Perform 2 full rounds before every Legs session.', height=100,
            help='Lower body dynamic warm-up exercises and instructions.')
    
    wu_protocol = st.text_area('📋 Protocol Rules (One per line)', 
        value='Never skip warm-up — injury prevention is non-negotiable\nFull range of motion on every drill\nUse warm-up sets: 50% > 75% > working weight\nNote restricted areas and spend extra time there',
        height=120,
        help='List of warm-up protocol rules. Each line becomes a bullet point in the PDF.')

# ═══════════════════════════════════════════════
# SECTION 6: TIPS & QUOTE
# ═══════════════════════════════════════════════
st.markdown("---")
with st.expander("💡 TIPS & MOTIVATION (Click to Edit)", expanded=False):
    st.markdown('<p class="section-desc">Tips appear on Page 7 in a 2x3 grid. Quote appears at the bottom of Page 7.</p>', unsafe_allow_html=True)
    
    tips_text = st.text_area('📝 Tips (Format: TITLE | BODY — One per line)', 
        value="PERFECT FORM | Every rep with compromised technique reinforces a harmful pattern. Reduce load, master the movement, then progress. Record yourself regularly.\nPROGRESSIVE OVERLOAD | Add 2.5 kg or 2 reps each week minimum. Log every session. If you are not progressing, you are regressing.\nSLEEP AS TRAINING | Growth hormone peaks during deep sleep. 7-9 hours nightly is not optional — it is where muscle protein synthesis occurs.\nFUEL YOUR SESSIONS | Target 1.8-2.2g protein per kg bodyweight daily. Eat a protein-rich meal 60-90 minutes before training. Log your nutrition.\nHYDRATION DAILY | Minimum 4 liters of water on training days. Even mild dehydration reduces force output by up to 20%.\nMENTAL EDGE | Controlled breathing and visualization before each set measurably increases power output. Train the mind first. The body follows.",
        height=200,
        help='Enter 6 tips. Each tip on a new line. Format: TITLE | BODY TEXT')
    
    cq1, cq2 = st.columns([3,1])
    with cq1:
        quote = st.text_area('💬 Motivational Quote', 'THE BODY ACHIEVES WHAT THE MIND BELIEVES. DISCIPLINE IS THE BRIDGE BETWEEN GOALS AND GREATNESS.', height=100,
            help='The main motivational quote displayed prominently on Page 7.')
    with cq2:
        quote_author = st.text_input('✍️ Quote Author', '— Ahmed Teka',
            help='Author attribution for the quote. Example: — Ahmed Teka')

# ═══════════════════════════════════════════════
# GENERATE BUTTON
# ═══════════════════════════════════════════════
st.markdown("---")
st.markdown('<div class="gen-btn">', unsafe_allow_html=True)
gen_clicked = st.button('🔥 GENERATE PREMIUM 8-PAGE PDF NOW 🔥', use_container_width=True, key='generate')
st.markdown('</div>', unsafe_allow_html=True)

if gen_clicked:
    if not client_name:
        st.error('❌ ERROR: Please enter the client name at minimum.')
    else:
        with st.spinner('⚡ Creating your premium 8-page workout plan PDF... This takes a few seconds...'):
            try:
                # Collect all exercises
                all_ex_list = []
                for day_key, day_data in all_exercises.items():
                    all_ex_list.extend(day_data['exercises'])
                
                # If no exercises entered, create defaults
                if not all_ex_list:
                    for day_key, day_data in all_exercises.items():
                        for i in range(3):
                            all_ex_list.append({
                                'name': f'{day_data["label"]} EXERCISE {i+1}',
                                'sets': '3', 'reps': '10-12', 'rest': '90s',
                                'desc': 'Full ROM. Control the movement.',
                                'link': '#', 'day': day_key
                            })
                
                # Parse tips
                tips = []
                for line in tips_text.strip().split('\n'):
                    if '|' in line:
                        t, b = line.split('|', 1)
                        tips.append({'title': t.strip(), 'icon': f'{len(tips)+1:02d}', 'body': b.strip()})
                
                if len(tips) < 6:
                    defaults = ['PERFECT FORM', 'PROGRESSIVE OVERLOAD', 'SLEEP AS TRAINING', 'FUEL YOUR SESSIONS', 'HYDRATION DAILY', 'MENTAL EDGE']
                    for i, t in enumerate(defaults):
                        if len(tips) <= i:
                            tips.append({'title': t, 'icon': f'{i+1:02d}', 'body': 'Focus on quality over quantity.'})
                
                # Build data
                data = {
                    'client_name': client_name, 'program': program_type, 'volume': volume,
                    'tagline': tagline, 'duration': duration, 'frequency': frequency,
                    'start_date': start_date, 'goal': goal, 'coach_name': coach_name,
                    'instagram': instagram, 'instagram_link': instagram_link, 'phone': phone,
                    'philosophy': philosophy, 'exercises': all_ex_list, 'tips': tips[:6],
                    'quote': quote, 'quote_author': quote_author,
                    'timeline': [
                        {'week': 'WEEK 1-2', 'phase': 'FOUNDATION', 'desc': 'Master form. Build mind-muscle connection. Establish baseline loads for all movements.'},
                        {'week': 'WEEK 3-4', 'phase': 'PROGRESSION', 'desc': 'Increase load by 5-10%. Volume ramps methodically. Training intensity begins to rise.'},
                        {'week': 'WEEK 5-6', 'phase': 'INTENSIFICATION', 'desc': 'Push beyond comfort zones. Drop sets introduced on the final exercise of each session.'},
                        {'week': 'WEEK 7-8', 'phase': 'PEAK OUTPUT', 'desc': 'Maximum effort on all lifts. Test your true capacity. Deload the final 3 days of week 8.'},
                    ],
                    'warmup': {
                        'cardio': wu_cardio,
                        'upper_note': wu_upper,
                        'lower_note': wu_lower,
                        'upper_link': '#',
                        'lower_link': '#',
                        'protocol': [p.strip() for p in wu_protocol.split('\n') if p.strip()],
                    },
                }
                
                pdf_bytes = generate_pdf(data)
                st.markdown('<div class="success-box">🔥 PDF GENERATED SUCCESSFULLY! 🔥<br><small>Your premium workout plan is ready for download.</small></div>', unsafe_allow_html=True)
                st.download_button('📥 DOWNLOAD PREMIUM PDF', data=pdf_bytes, file_name=f'AhmedTeka_{client_name.replace(" ","_")}.pdf', mime='application/pdf', use_container_width=True)
                
                # Success details
                st.success(f'✅ Client: {client_name} | Program: {program_type} | Exercises: {len(all_ex_list)} | Pages: 8')
                
            except Exception as e:
                st.error(f'❌ Error generating PDF: {str(e)}')
                import traceback
                st.code(traceback.format_exc())
                st.info('Please check all fields and try again. Contact support if the issue persists.')

st.markdown('---')
st.markdown("""
<div style="text-align:center;color:#6B7280;padding:1rem">
    <p style="font-size:1.1rem;color:#D4AF37;font-weight:700">© AHMED TEKA — PREMIUM WORKOUT PLANS</p>
    <p>📸 Instagram: @coach.teka1 | 📞 Phone: 01033047057</p>
    <p style="font-size:0.8rem">Professional Training Programs · Since 2020</p>
</div>
""", unsafe_allow_html=True)