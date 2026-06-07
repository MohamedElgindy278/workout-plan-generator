import streamlit as st
import os
from datetime import datetime
from workout_generator import generate_pdf

st.set_page_config(page_title='Ahmed Teka - Workout Plan', page_icon='💪', layout='wide')

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;900&display=swap');
    *{font-family:'Cairo',sans-serif!important}
    .main-header{background:linear-gradient(135deg,#080B12,#1A2235);padding:2rem;border-radius:15px;text-align:center;border:2px solid #D4AF37;margin-bottom:2rem}
    .main-header h1{color:#D4AF37;font-size:2rem;font-weight:900}
    .stButton>button{background:linear-gradient(135deg,#D4AF37,#A0832A);color:#080B12;font-weight:700;font-size:1.3rem;padding:1rem;border-radius:10px;border:none;width:100%}
    .stButton>button:hover{background:linear-gradient(135deg,#E8C84A,#D4AF37)}
    label{color:#D4AF37!important;font-weight:600!important}
    .success-box{background:linear-gradient(135deg,#1C1A08,#2A2208);border:2px solid #D4AF37;border-radius:10px;padding:1.5rem;text-align:center;color:#D4AF37;font-size:1.2rem;font-weight:700}
</style>
""", unsafe_allow_html=True)

# Image paths - relative to app
IMAGES_DIR = "images"

st.markdown('<div class="main-header"><h1>🏋️ Ahmed Teka — Premium Workout Plan</h1><p>Push / Pull / Legs · Professional Quality</p></div>', unsafe_allow_html=True)

with st.form('workout_form'):
    st.markdown('### 📋 Client Data')
    
    col1, col2 = st.columns(2)
    with col1:
        client_name = st.text_input('👤 Client Name', placeholder='MOHAMED')
        weight = st.text_input('⚖️ Weight (kg)', placeholder='75')
        goal = st.text_input('🎯 Goal', placeholder='HYPERTROPHY & STRENGTH')
    with col2:
        program = st.text_input('📅 Program', value='PUSH // PULL // LEGS')
        duration = st.text_input('⏳ Duration', value='8 WEEKS')
        frequency = st.text_input('🔄 Frequency', value='6 DAYS / WEEK')
    
    st.markdown('---')
    st.markdown('### 📝 Custom Text')
    tagline = st.text_input('Tagline', value='ENGINEERED FOR DOMINANCE')
    philosophy = st.text_area('Philosophy', value='This program is about training with intention, precision, and relentless focus. Every set, every rep, every second of rest is calculated to push your body beyond its limits and force adaptation.', height=100)
    
    st.markdown('---')
    st.markdown('### 💪 Exercises (one per line: name - sets x reps)')
    exercises_text = st.text_area('Exercises', 
        value='''CHEST PRESS MACHINE - 3x10-12
DB INCLINE CHEST PRESS - 3x10-12
BUTTERFLY MACHINE - 3x10-12
DB SHOULDER PRESS - 3x10-12
SEATED LATERAL RAISE - 3x12-15
CABLE OVERHEAD TRICEP - 3x12-15
ROPE PUSHDOWN - 3x12-15
CABLE CRUNCH - 3x15-20''',
        height=200)
    
    submitted = st.form_submit_button('🚀 Generate Premium PDF', use_container_width=True)

if submitted:
    if not client_name:
        st.error('⚠️ Please enter client name')
    else:
        with st.spinner('🔄 Creating premium workout plan...'):
            try:
                exercises_list = []
                for line in exercises_text.strip().split('\n'):
                    if line.strip():
                        parts = line.split('-')
                        name = parts[0].strip()
                        sets_reps = parts[1].strip() if len(parts) > 1 else '3x10'
                        s, r = (sets_reps.split('x') if 'x' in sets_reps else ('3', '10'))
                        
                        # Assign day
                        name_lower = name.lower()
                        if any(w in name_lower for w in ['press', 'push', 'chest', 'shoulder', 'tricep', 'lateral', 'crunch']):
                            day = 'push_day'
                        elif any(w in name_lower for w in ['pull', 'row', 'curl', 'lat', 'shrug', 'back', 'rear']):
                            day = 'pull_day'
                        else:
                            day = 'legs_day'
                        
                        exercises_list.append({
                            'name': name, 'sets': s.strip(), 'reps': r.strip(),
                            'rest': '90s', 'desc': f'Full ROM. Control the movement.',
                            'link': '#', 'day': day
                        })
                
                if len(exercises_list) < 3:
                    st.error('Please enter at least 3 exercises')
                    st.stop()
                
                data = {
                    'client_name': client_name, 'program': program, 'volume': 'VOL.1',
                    'tagline': tagline, 'duration': duration, 'frequency': frequency,
                    'start_date': datetime.now().strftime('%B %Y').upper(),
                    'goal': goal, 'coach_name': 'AHMED TEKA',
                    'instagram': '@coach.teka1', 'instagram_link': 'https://instagram.com/coach.teka1',
                    'phone': '01033047057', 'philosophy': philosophy,
                    'exercises': exercises_list,
                    'photo_cover': os.path.join(IMAGES_DIR, 'cover.jpg'),
                    'photo_intro': os.path.join(IMAGES_DIR, 'intro.jpg'),
                    'photo_coach': os.path.join(IMAGES_DIR, 'coach.jpg'),
                    'timeline': [
                        {'week': 'WEEK 1-2', 'phase': 'FOUNDATION', 'desc': 'Master form. Build mind-muscle connection.'},
                        {'week': 'WEEK 3-4', 'phase': 'PROGRESSION', 'desc': 'Increase load by 5-10%.'},
                        {'week': 'WEEK 5-6', 'phase': 'INTENSIFICATION', 'desc': 'Push beyond comfort zones.'},
                        {'week': 'WEEK 7-8', 'phase': 'PEAK OUTPUT', 'desc': 'Maximum effort on all lifts.'},
                    ],
                    'warmup': {
                        'cardio': '5-10 MIN LIGHT CARDIO: Treadmill or bike at 60-65% max heart rate.',
                        'upper_note': 'Shoulder circles, band pull-aparts, arm swings, chest openers.',
                        'lower_note': 'Hip circles, leg swings, bodyweight squats, ankle rotations.',
                        'upper_link': 'https://youtube.com/watch?v=upper_warmup',
                        'lower_link': 'https://youtube.com/watch?v=lower_warmup',
                        'protocol': [
                            'Never skip warm-up — injury prevention is non-negotiable',
                            'Full range of motion on every drill',
                            'Use warm-up sets: 50% > 75% > working weight',
                            'Note restricted areas and spend extra time there',
                        ],
                    },
                    'tips': [
                        {'title': 'PERFECT FORM', 'icon': '01', 'body': 'Every rep with compromised technique reinforces a harmful pattern.'},
                        {'title': 'PROGRESSIVE OVERLOAD', 'icon': '02', 'body': 'Add 2.5 kg or 2 reps each week minimum.'},
                        {'title': 'SLEEP AS TRAINING', 'icon': '03', 'body': 'Growth hormone peaks during deep sleep. 7-9 hours nightly.'},
                        {'title': 'FUEL YOUR SESSIONS', 'icon': '04', 'body': 'Target 1.8-2.2g protein per kg bodyweight daily.'},
                        {'title': 'HYDRATION DAILY', 'icon': '05', 'body': 'Minimum 4 liters of water on training days.'},
                        {'title': 'MENTAL EDGE', 'icon': '06', 'body': 'Controlled breathing and visualization increases power.'},
                    ],
                    'quote': 'THE BODY ACHIEVES WHAT THE MIND BELIEVES. DISCIPLINE IS THE BRIDGE BETWEEN GOALS AND GREATNESS.',
                    'quote_author': '— Ahmed Teka',
                }
                
                pdf_bytes = generate_pdf(data)
                st.markdown('<div class="success-box">✅ Premium PDF Generated Successfully!</div>', unsafe_allow_html=True)
                st.download_button('📥 Download PDF', data=pdf_bytes, file_name=f'AhmedTeka_{client_name}.pdf', mime='application/pdf', use_container_width=True)
                
            except Exception as e:
                st.error(f'❌ Error: {str(e)}')

st.markdown('---')
st.markdown('<p style="text-align:center;color:#6B7280">© Ahmed Teka · @coach.teka1 · 01033047057</p>', unsafe_allow_html=True)