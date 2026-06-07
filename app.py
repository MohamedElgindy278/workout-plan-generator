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
.stButton>button{background:linear-gradient(135deg,#D4AF37,#A0832A);color:#080B12;font-weight:700;font-size:1.2rem;padding:1rem;border-radius:10px;border:none;width:100%}
.gen-btn>button{background:linear-gradient(135deg,#D4AF37,#FF6B35)!important;color:#000!important;font-size:1.5rem!important;padding:1.5rem!important;font-weight:900!important;animation:pulse 2s infinite}
@keyframes pulse{0%{box-shadow:0 0 0 0 rgba(212,175,55,0.4)}70%{box-shadow:0 0 0 20px rgba(212,175,55,0)}100%{box-shadow:0 0 0 0 rgba(212,175,55,0)}}
label{color:#D4AF37!important;font-weight:600!important}
input,textarea,select{background-color:#1A2235!important;color:#E8E4DC!important;border:2px solid #374151!important;border-radius:8px!important}
.exercise-card{background:#111827;border:1px solid #D4AF37;border-radius:10px;padding:1rem;margin:0.5rem 0}
.exercise-card h4{color:#D4AF37;margin:0 0 0.5rem 0}
.day-header{background:linear-gradient(135deg,#1A2235,#080B12);padding:1rem;border-radius:10px;border-left:5px solid #D4AF37;margin:1rem 0}
.day-header h3{color:#D4AF37;margin:0}
.success-box{background:linear-gradient(135deg,#1C1A08,#2A2208);border:2px solid #D4AF37;border-radius:10px;padding:2rem;text-align:center;color:#D4AF37;font-size:1.5rem;font-weight:900}
.info-box{background:#0C1020;border:1px solid #374151;border-radius:8px;padding:1rem;margin:0.5rem 0}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-header"><h1>🏋️ AHMED TEKA</h1><p>PREMIUM WORKOUT PLAN GENERATOR</p></div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════
# PROGRAM TYPES CONFIG
# ═══════════════════════════════════════════════
PROGRAM_CONFIGS = {
    'PUSH // PULL // LEGS': {
        'days': [
            {'key': 'push_day', 'label': 'PUSH', 'subtitle': 'CHEST · SHOULDERS · TRICEPS', 'desc': 'Prioritize chest activation on horizontal movements, shoulder engagement on overhead work, and full tricep lockout on isolation exercises.', 'rest_note': 'REST 90-120 SECONDS BETWEEN ALL WORKING SETS'},
            {'key': 'pull_day', 'label': 'PULL', 'subtitle': 'BACK · BICEPS · REAR DELTS', 'desc': 'Drive elbows — not hands — on all row variations. Maintain scapular retraction throughout.', 'rest_note': 'REST 90-120 SECONDS BETWEEN ALL WORKING SETS'},
            {'key': 'legs_day', 'label': 'LEGS', 'subtitle': 'QUADS · HAMSTRINGS · GLUTES · CALVES', 'desc': 'Heavy compound movements first. Never skip posterior chain work.', 'rest_note': 'REST 2 FULL MINUTES AFTER SQUATS AND LEG PRESS'},
        ]
    },
    'ARNOLD SPLIT': {
        'days': [
            {'key': 'chest_back_day', 'label': 'CHEST & BACK', 'subtitle': 'CHEST · LATS · RHOMBOIDS', 'desc': 'Superset chest and back movements for maximum pump and efficiency.', 'rest_note': 'REST 60-90 SECONDS BETWEEN SUPERSETS'},
            {'key': 'shoulders_arms_day', 'label': 'SHOULDERS & ARMS', 'subtitle': 'DELTS · BICEPS · TRICEPS', 'desc': 'Focus on deltoid isolation followed by arm supersets.', 'rest_note': 'REST 45-60 SECONDS BETWEEN SETS'},
            {'key': 'legs_day', 'label': 'LEGS & ABS', 'subtitle': 'QUADS · HAMSTRINGS · CALVES · CORE', 'desc': 'Heavy leg compounds followed by core work.', 'rest_note': 'REST 2 MINUTES AFTER HEAVY COMPOUNDS'},
        ]
    },
    'UPPER / LOWER': {
        'days': [
            {'key': 'upper_day', 'label': 'UPPER BODY', 'subtitle': 'CHEST · BACK · SHOULDERS · ARMS', 'desc': 'Complete upper body workout focusing on compound and isolation movements.', 'rest_note': 'REST 90-120 SECONDS ON COMPOUNDS, 60S ON ISOLATION'},
            {'key': 'lower_day', 'label': 'LOWER BODY', 'subtitle': 'QUADS · HAMSTRINGS · GLUTES · CALVES', 'desc': 'Full lower body session with both bilateral and unilateral work.', 'rest_note': 'REST 2 MINUTES ON HEAVY SETS'},
        ]
    },
    'BRO SPLIT': {
        'days': [
            {'key': 'chest_day', 'label': 'CHEST', 'subtitle': 'PECTORALS · FRONT DELTS', 'desc': 'Full chest development with flat, incline, and isolation work.', 'rest_note': 'REST 90 SECONDS BETWEEN SETS'},
            {'key': 'back_day', 'label': 'BACK', 'subtitle': 'LATS · TRAPS · RHOMBOIDS', 'desc': 'Width and thickness focused back training.', 'rest_note': 'REST 90 SECONDS BETWEEN SETS'},
            {'key': 'shoulders_day', 'label': 'SHOULDERS', 'subtitle': 'ALL DELTOID HEADS', 'desc': 'Complete shoulder development focusing on all three heads.', 'rest_note': 'REST 60-90 SECONDS BETWEEN SETS'},
            {'key': 'arms_day', 'label': 'ARMS', 'subtitle': 'BICEPS · TRICEPS · FOREARMS', 'desc': 'Isolation work for maximum arm pump and growth.', 'rest_note': 'REST 45-60 SECONDS BETWEEN SETS'},
            {'key': 'legs_day', 'label': 'LEGS', 'subtitle': 'QUADS · HAMSTRINGS · GLUTES · CALVES', 'desc': 'Complete leg development from heavy compounds to isolation.', 'rest_note': 'REST 2 MINUTES ON HEAVY SETS'},
        ]
    },
    'FULL BODY': {
        'days': [
            {'key': 'full_body_a', 'label': 'FULL BODY A', 'subtitle': 'STRENGTH FOCUS', 'desc': 'Full body workout emphasizing strength on main compounds.', 'rest_note': 'REST 2-3 MINUTES ON MAIN LIFTS'},
            {'key': 'full_body_b', 'label': 'FULL BODY B', 'subtitle': 'HYPERTROPHY FOCUS', 'desc': 'Full body workout with higher volume for muscle growth.', 'rest_note': 'REST 60-90 SECONDS BETWEEN SETS'},
        ]
    },
}

# ═══════════════════════════════════════════════
# FORM
# ═══════════════════════════════════════════════
st.markdown("## 📋 CLIENT INFORMATION")

col1, col2, col3 = st.columns(3)
with col1:
    client_name = st.text_input('👤 Client Name', 'MOHAMED')
    weight = st.text_input('⚖️ Weight (kg)', '75')
    start_date = st.text_input('📅 Start Date', datetime.now().strftime('%B %Y').upper())
with col2:
    goal = st.text_input('🎯 Goal', 'HYPERTROPHY & STRENGTH')
    volume = st.text_input('📊 Volume', 'VOL.1')
    duration = st.text_input('⏱️ Duration', '8 WEEKS')
with col3:
    tagline = st.text_input('💬 Tagline', 'ENGINEERED FOR DOMINANCE')
    frequency = st.text_input('🔄 Frequency', '6 DAYS / WEEK')
    
    # PROGRAM TYPE SELECT
    program_type = st.selectbox('📋 Program Type', list(PROGRAM_CONFIGS.keys()), index=0)

# COACH
st.markdown("---")
col_c1, col_c2, col_c3 = st.columns(3)
with col_c1:
    coach_name = st.text_input('🧑‍🏫 Coach Name', 'AHMED TEKA')
with col_c2:
    instagram = st.text_input('📸 Instagram', '@coach.teka1')
with col_c3:
    phone = st.text_input('📞 Phone', '01033047057')
instagram_link = st.text_input('🔗 Instagram Link', 'https://instagram.com/coach.teka1')

# PHILOSOPHY
st.markdown("---")
st.markdown("## 📖 PROGRAM PHILOSOPHY")
philosophy = st.text_area('Training Philosophy', 
    value="This program is not about going through the motions. It is about training with intention, precision, and relentless focus. Every set, every rep, every second of rest is calculated to push your body beyond its limits and force adaptation.\n\nThe Push Pull Legs split allows optimal muscle recovery while maintaining high training frequency. You will train each muscle group twice per week across 6 sessions, with one full rest day for complete systemic recovery.\n\nAdhere strictly to prescribed rest intervals. Progressive overload — adding weight or reps each week — is your primary growth driver. Track every session. Outperform yesterday.",
    height=150)

st.markdown("---")

# ═══════════════════════════════════════════════
# DYNAMIC EXERCISE SECTIONS
# ═══════════════════════════════════════════════
st.markdown(f"## 💪 {program_type} — EXERCISES")

config = PROGRAM_CONFIGS[program_type]
all_exercises = {}

for day_idx, day in enumerate(config['days']):
    st.markdown(f'<div class="day-header"><h3>🏆 {day["label"]} DAY — {day["subtitle"]}</h3><p style="color:#9BA3B2;margin:0.5rem 0 0 0">{day["desc"]}</p></div>', unsafe_allow_html=True)
    
    # Description
    day_desc = st.text_area(f'Description for {day["label"]} Day', value=day['desc'], height=70, key=f'desc_{day["key"]}')
    day_rest = st.text_input(f'Rest Note for {day["label"]} Day', value=day['rest_note'], key=f'rest_{day["key"]}')
    
    st.markdown(f"**Exercises for {day['label']} Day**")
    
    # Number of exercises for this day
    num_exercises = st.number_input(f'Number of exercises for {day["label"]}', min_value=1, max_value=20, value=8, key=f'num_{day["key"]}')
    
    day_exercises = []
    
    # Create columns for headers
    hcol1, hcol2, hcol3, hcol4, hcol5, hcol6 = st.columns([3, 1, 1, 1, 3, 2])
    with hcol1:
        st.markdown('<p style="color:#D4AF37;font-weight:700;font-size:0.85rem">EXERCISE NAME</p>', unsafe_allow_html=True)
    with hcol2:
        st.markdown('<p style="color:#D4AF37;font-weight:700;font-size:0.85rem">SETS</p>', unsafe_allow_html=True)
    with hcol3:
        st.markdown('<p style="color:#D4AF37;font-weight:700;font-size:0.85rem">REPS</p>', unsafe_allow_html=True)
    with hcol4:
        st.markdown('<p style="color:#D4AF37;font-weight:700;font-size:0.85rem">REST</p>', unsafe_allow_html=True)
    with hcol5:
        st.markdown('<p style="color:#D4AF37;font-weight:700;font-size:0.85rem">DESCRIPTION</p>', unsafe_allow_html=True)
    with hcol6:
        st.markdown('<p style="color:#D4AF37;font-weight:700;font-size:0.85rem">VIDEO LINK</p>', unsafe_allow_html=True)
    
    for ex_idx in range(int(num_exercises)):
        exc1, exc2, exc3, exc4, exc5, exc6 = st.columns([3, 1, 1, 1, 3, 2])
        with exc1:
            ex_name = st.text_input('Name', value=f'Exercise {ex_idx+1}' if ex_idx >= 8 else '', placeholder=f'Ex: BENCH PRESS', key=f'name_{day["key"]}_{ex_idx}', label_visibility='collapsed')
        with exc2:
            ex_sets = st.text_input('Sets', value='3', key=f'sets_{day["key"]}_{ex_idx}', label_visibility='collapsed')
        with exc3:
            ex_reps = st.text_input('Reps', value='10-12', key=f'reps_{day["key"]}_{ex_idx}', label_visibility='collapsed')
        with exc4:
            ex_rest = st.text_input('Rest', value='90s', key=f'rest_{day["key"]}_{ex_idx}', label_visibility='collapsed')
        with exc5:
            ex_desc = st.text_input('Desc', value='', placeholder='Full ROM. Control movement.', key=f'desc_{day["key"]}_{ex_idx}', label_visibility='collapsed')
        with exc6:
            ex_link = st.text_input('Link', value='#', key=f'link_{day["key"]}_{ex_idx}', label_visibility='collapsed')
        
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

st.markdown("---")

# ═══════════════════════════════════════════════
# WARMUP
# ═══════════════════════════════════════════════
with st.expander("🔥 WARM-UP PROTOCOL (Click to edit)", expanded=False):
    wu_cardio = st.text_area('Cardio Phase', '5-10 MIN LIGHT CARDIO: Treadmill or bike at 60-65% max heart rate.', height=70)
    wc1, wc2 = st.columns(2)
    with wc1:
        wu_upper = st.text_area('Upper Body Warm-Up', 'Shoulder circles, band pull-aparts, arm swings, chest openers.', height=80)
    with wc2:
        wu_lower = st.text_area('Lower Body Warm-Up', 'Hip circles, leg swings, bodyweight squats, ankle rotations.', height=80)
    wu_protocol = st.text_area('Protocol Rules (one per line)', 'Never skip warm-up\nFull ROM on every drill\nWarm-up sets: 50% > 75% > working weight')

# ═══════════════════════════════════════════════
# TIPS
# ═══════════════════════════════════════════════
with st.expander("💡 TIPS & MOTIVATION (Click to edit)", expanded=False):
    tips_text = st.text_area('Tips (TITLE | BODY per line)', 
        value="PERFECT FORM | Every rep with perfect technique.\nPROGRESSIVE OVERLOAD | Add 2.5 kg or 2 reps weekly.\nSLEEP AS TRAINING | 7-9 hours nightly for recovery.\nFUEL YOUR SESSIONS | 1.8-2.2g protein per kg daily.\nHYDRATION DAILY | Minimum 4 liters of water.\nMENTAL EDGE | Visualize before every set.",
        height=150)
    cq1, cq2 = st.columns([3,1])
    with cq1:
        quote = st.text_area('Quote', 'THE BODY ACHIEVES WHAT THE MIND BELIEVES. DISCIPLINE IS THE BRIDGE BETWEEN GOALS AND GREATNESS.', height=80)
    with cq2:
        quote_author = st.text_input('Author', '— Ahmed Teka')

# ═══════════════════════════════════════════════
# GENERATE BUTTON
# ═══════════════════════════════════════════════
st.markdown("---")
st.markdown('<div class="gen-btn">', unsafe_allow_html=True)
if st.button('🔥 GENERATE PREMIUM 8-PAGE PDF NOW 🔥', use_container_width=True, key='generate'):
    st.markdown('</div>', unsafe_allow_html=True)
    
    if not client_name:
        st.error('❌ Please enter client name')
    else:
        with st.spinner('⚡ Creating your premium workout plan...'):
            try:
                # Collect all exercises
                all_ex_list = []
                for day_key, day_data in all_exercises.items():
                    all_ex_list.extend(day_data['exercises'])
                
                # Default exercises if empty
                if not all_ex_list:
                    for day_key, day_data in all_exercises.items():
                        all_ex_list.append({
                            'name': f'{day_data["label"]} EXERCISE 1',
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
                
                if not tips:
                    tips = [{'title': 'QUALITY FIRST', 'icon': '01', 'body': 'Focus on form over weight.'}]
                
                data = {
                    'client_name': client_name, 'program': program_type, 'volume': volume,
                    'tagline': tagline, 'duration': duration, 'frequency': frequency,
                    'start_date': start_date, 'goal': goal, 'coach_name': coach_name,
                    'instagram': instagram, 'instagram_link': instagram_link, 'phone': phone,
                    'philosophy': philosophy, 'exercises': all_ex_list, 'tips': tips,
                    'quote': quote, 'quote_author': quote_author,
                    'timeline': [
                        {'week': 'WEEK 1-2', 'phase': 'FOUNDATION', 'desc': 'Master form. Build mind-muscle connection.'},
                        {'week': 'WEEK 3-4', 'phase': 'PROGRESSION', 'desc': 'Increase load by 5-10%.'},
                        {'week': 'WEEK 5-6', 'phase': 'INTENSIFICATION', 'desc': 'Push beyond comfort zones.'},
                        {'week': 'WEEK 7-8', 'phase': 'PEAK OUTPUT', 'desc': 'Maximum effort on all lifts.'},
                    ],
                    'warmup': {
                        'cardio': wu_cardio,
                        'upper_note': wu_upper,
                        'lower_note': wu_lower,
                        'upper_link': '#',
                        'lower_link': '#',
                        'protocol': wu_protocol.split('\n'),
                    },
                }
                
                pdf_bytes = generate_pdf(data)
                st.markdown('<div class="success-box">🔥 PDF GENERATED SUCCESSFULLY! 🔥</div>', unsafe_allow_html=True)
                st.download_button('📥 DOWNLOAD YOUR PREMIUM PDF', data=pdf_bytes, file_name=f'AhmedTeka_{client_name.replace(" ","_")}.pdf', mime='application/pdf', use_container_width=True)
                
            except Exception as e:
                st.error(f'Error: {str(e)}')
                import traceback
                st.code(traceback.format_exc())

st.markdown('---')
st.markdown('<p style="text-align:center;color:#6B7280">© AHMED TEKA · @coach.teka1 · 01033047057</p>', unsafe_allow_html=True)