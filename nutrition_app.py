import streamlit as st
from datetime import datetime
from nutrition_generator import generate_nutrition_pdf

st.set_page_config(page_title='AHMED TEKA - Nutrition Plan', page_icon='🥗', layout='wide')

# Force Arabic font support on cloud
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Tajawal:wght@400;500;700;900&display=swap" rel="stylesheet">
<style>
@import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;500;700;900&display=swap');
*{font-family:'Tajawal',sans-serif!important}
html, body, [class*="css"] {font-family:'Tajawal',sans-serif!important}
.main-header{background:linear-gradient(135deg,#F8F8F8,#E8F5F0);padding:1.5rem;border-radius:15px;text-align:center;border:2px solid #2E7D64;margin-bottom:1.5rem}
.main-header h1{color:#2E7D64;font-size:2rem;font-weight:900;margin:0}
.main-header p{color:#555;margin:0.3rem 0 0 0}
.stButton>button{background:linear-gradient(135deg,#2E7D64,#4CAF50);color:#FFF;font-weight:700;font-size:1.2rem;padding:1rem;border-radius:10px;border:none;width:100%}
.stButton>button:hover{background:linear-gradient(135deg,#4CAF50,#81C784)}
label{color:#2E7D64!important;font-weight:600!important}
input,textarea,select{background-color:#FFF!important;color:#1A1A1A!important;border:2px solid #C8E6C9!important;border-radius:8px!important;font-family:'Tajawal',sans-serif!important}
input:focus,textarea:focus{border-color:#2E7D64!important;box-shadow:0 0 5px rgba(46,125,100,0.3)!important}
.day-header{background:linear-gradient(135deg,#E8F5F0,#FFF);padding:1rem;border-radius:10px;border-left:5px solid #2E7D64;margin:1rem 0}
.day-header h4{color:#1B5E20;margin:0}
.success-box{background:linear-gradient(135deg,#E8F5F0,#FFF);border:2px solid #2E7D64;border-radius:10px;padding:2rem;text-align:center;color:#2E7D64;font-size:1.3rem;font-weight:700}
.section-desc{color:#777;font-size:0.85rem;margin-bottom:1rem}
.gen-btn>button{background:linear-gradient(135deg,#2E7D64,#D4AF37)!important;font-size:1.4rem!important;padding:1.5rem!important;font-weight:900!important;animation:pulse 2s infinite}
@keyframes pulse{0%{box-shadow:0 0 0 0 rgba(46,125,100,0.4)}70%{box-shadow:0 0 0 20px rgba(46,125,100,0)}100%{box-shadow:0 0 0 0 rgba(46,125,100,0)}}
.counter-btn>button{background:#E8F5F0!important;color:#2E7D64!important;border:2px solid #2E7D64!important;font-weight:700!important}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-header"><h1>🥗 AHMED TEKA — NUTRITION PLAN</h1><p>Professional · Personalized Meal Plan Generator</p></div>', unsafe_allow_html=True)

# Initialize session states for dynamic counts
if 'supplements_count' not in st.session_state:
    st.session_state.supplements_count = 3
if 'preworkout_count' not in st.session_state:
    st.session_state.preworkout_count = 2
if 'recipes_count' not in st.session_state:
    st.session_state.recipes_count = 6

with st.form('nutrition_form'):
    
    # ═══════════════════════════════════════════════
    # COVER PAGE INFO
    # ═══════════════════════════════════════════════
    st.markdown('## 📋 COVER PAGE INFORMATION')
    st.markdown('<p class="section-desc">These details appear on the cover page of the PDF.</p>', unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns(3)
    with c1:
        client_name = st.text_input('👤 Client Name', 'محمد', help='Client name displayed prominently on the cover page.')
        full_name = st.text_input('📛 Full Name', 'محمد أحمد', help='Full name for the profile page.')
        age = st.text_input('🎂 Age', '28 سنة', help='Client age.')
    with c2:
        weight = st.text_input('⚖️ Weight', '80 كجم', help='Current body weight.')
        height = st.text_input('📏 Height', '175 سم', help='Client height.')
        goal = st.text_input('🎯 Goal', 'بناء عضلي', help='Primary nutrition goal. Examples: بناء عضلي, تنشيف, زيادة وزن')
    with c3:
        duration = st.text_input('⏱️ Duration', '12 أسبوع', help='Plan duration. Example: 12 أسبوع, 8 أسابيع')
        meals_count = st.text_input('🍽️ Meals Count', '4 وجبات', help='Number of meals per day. Example: 4 وجبات, 5 وجبات')
        start_date = st.text_input('📅 Start Date', 'يونيو 2026', help='Program start month/year.')
    
    notes = st.text_area('📝 Coach Notes', 'نظام مخصص بالكامل لزيادة الكتلة العضلية تحت إشراف المدرب أحمد تيكا', height=70,
        help='Special notes from the coach. Appears on the profile page.')
    
    # ═══════════════════════════════════════════════
    # MACROS
    # ═══════════════════════════════════════════════
    st.markdown('---')
    st.markdown('## 📊 MACRONUTRIENTS')
    st.markdown('<p class="section-desc">Daily macronutrient distribution.</p>', unsafe_allow_html=True)
    
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        protein_g = st.text_input('🥩 Protein (g/day)', '180', help='Daily protein intake in grams.')
    with m2:
        carbs_g = st.text_input('🍚 Carbs (g/day)', '280', help='Daily carbohydrate intake in grams.')
    with m3:
        fat_g = st.text_input('🧈 Fat (g/day)', '65', help='Daily fat intake in grams.')
    with m4:
        main_meals = st.text_input('🍽️ Main Meals/Day', '4', help='Number of main meals per day.')
    
    total_calories = st.text_input('🔥 Total Daily Calories', '2502', help='Total daily caloric intake.')
    
    # ═══════════════════════════════════════════════
    # MEALS
    # ═══════════════════════════════════════════════
    st.markdown('---')
    st.markdown('## 🍽️ MEALS')
    st.markdown('<p class="section-desc">Configure each meal with its details.</p>', unsafe_allow_html=True)
    
    num_meals = st.number_input('Number of meals', 1, 8, 4, help='How many meals in the plan? (1-8)')
    meals = []
    
    food_icons = ['🥣 Breakfast', '💪 Pre-Workout', '🍗 Lunch', '🥗 Dinner', '🍝 Snack 1', '🥤 Snack 2', '🍎 Snack 3', '🥜 Snack 4']
    
    for i in range(int(num_meals)):
        st.markdown(f'<div class="day-header"><h4>{food_icons[i] if i < 8 else "🍽️"} Meal {i+1}</h4></div>', unsafe_allow_html=True)
        
        mc1, mc2 = st.columns([2, 1])
        with mc1:
            meal_name = st.text_input(f'🍳 Meal Name {i+1}',
                value=['وجبة الإفطار', 'وجبة ما قبل التمرين', 'الوجبة الرئيسية الثالثة', 'وجبة العشاء'][i] if i < 4 else f'وجبة {i+1}',
                key=f'name_{i}', help=f'Name of meal {i+1}.')
        with mc2:
            meal_type = st.text_input(f'📋 Meal Type {i+1}',
                value=['الوجبة الأولى', 'الوجبة الثانية', 'الوجبة الثالثة', 'الوجبة الرابعة'][i] if i < 4 else f'الوجبة {i+1}',
                key=f'type_{i}', help=f'Type/label for meal {i+1}.')
        
        mc3, mc4, mc5, mc6 = st.columns(4)
        with mc3:
            meal_cal = st.text_input(f'🔥 Calories {i+1}', value=['747','750','523','482'][i] if i < 4 else '400', key=f'cal_{i}', help=f'Calories for meal {i+1}.')
        with mc4:
            meal_protein = st.text_input(f'🥩 Protein (g) {i+1}', value=['36','55','45','42'][i] if i < 4 else '30', key=f'prot_{i}', help=f'Protein in grams for meal {i+1}.')
        with mc5:
            meal_carbs = st.text_input(f'🍚 Carbs (g) {i+1}', value=['110','110','55','15'][i] if i < 4 else '40', key=f'carb_{i}', help=f'Carbs in grams for meal {i+1}.')
        with mc6:
            meal_fat = st.text_input(f'🧈 Fat (g) {i+1}', value=['18','36','18','12'][i] if i < 4 else '15', key=f'fat_{i}', help=f'Fat in grams for meal {i+1}.')
        
        ingredients = st.text_area(f'🛒 Ingredients {i+1} (one per line)',
            value='\n'.join([
                'شيكلات أوتس 100 جم', 'حليب كامل الدسم 200 مل', 'موز حبة واحدة', 'مكسرات ملعقة كبيرة',
                'أرز أبيض مسلوق 150 جم', 'صدر دجاج مشوي 200 جم', 'خضار مشكلة', 'زيت زيتون ملعقة',
                'أرز بني 100 جم', 'لحم بقري مفروم 150 جم', 'طماطم وبصل', 'خضار سلطة',
                'بيض 3 حبات', 'جبن قريش 100 جم', 'خيار وطماطم', 'زيت زيتون ملعقة',
            ][i*4:(i+1)*4]) if i < 4 else 'مكون 1\nمكون 2\nمكون 3\nمكون 4',
            height=80, key=f'ing_{i}', help=f'Ingredients for meal {i+1}. One per line.')
        
        alternative = st.text_input(f'🔄 Healthy Alternative {i+1}',
            value=['يمكن استبدال الأوتس بـ 4 توست + بيضتان مسلوقتان',
                   'يمكن استبدال الأرز بـ بطاطس مسلوقة 200 جم',
                   'يمكن استبدال اللحم بـ سمك تونة 200 جم',
                   'يمكن استبدال البيض بـ صدر دجاج 120 جم'][i] if i < 4 else 'بديل صحي',
            key=f'alt_{i}', help=f'Healthy alternative for meal {i+1}.')
        
        meals.append({
            'name': meal_name, 'type': meal_type,
            'calories': meal_cal, 'protein': meal_protein,
            'carbs': meal_carbs, 'fat': meal_fat,
            'ingredients': [x.strip() for x in ingredients.split('\n') if x.strip()],
            'alternative': alternative,
        })
    
    # ═══════════════════════════════════════════════
    # GUIDELINES
    # ═══════════════════════════════════════════════
    st.markdown('---')
    st.markdown('## 📋 GUIDELINES')
    st.markdown('<p class="section-desc">Daily guidelines and rules for the client.</p>', unsafe_allow_html=True)
    
    water = st.text_input('💧 Daily Water Intake', '4-6 لتر', help='Recommended daily water intake.')
    
    g1, g2 = st.columns(2)
    with g1:
        meal_timing = st.text_area('⏰ Meal Timing', 'الفترة بين الوجبات 2-3 ساعات لتعزيز الأيض والاستشفاء', height=70,
            help='Guidelines for meal spacing and timing.')
        drinks = st.text_area('🥤 Drinks', 'ممنوع السكريات والمشروبات المحلاة، فقط ماء وشاي بدون سكر', height=70,
            help='Allowed and prohibited drinks.')
    with g2:
        food_weighing = st.text_area('⚖️ Food Weighing', 'وزن الأطعمة بالميزان بعد الطهي لضبط السعرات بدقة', height=70,
            help='Instructions for weighing and measuring food.')
        sweets = st.text_area('🚫 Restricted Foods', 'السكريات والمنتجات المصنعة ممنوعة للحفاظ على الكورتيزول', height=70,
            help='Foods to avoid during the plan.')
    
    omega = st.text_input('🐟 Omega-3', '5-3 جم أوميجا 3 يومياً موزعاً على الوجبات', help='Omega-3 supplementation guidelines.')
    
    # ═══════════════════════════════════════════════
    # SUPPLEMENTS - DYNAMIC ADD/REMOVE
    # ═══════════════════════════════════════════════
    st.markdown('---')
    st.markdown('## 💊 SUPPLEMENTS')
    st.markdown('<p class="section-desc">Add or remove supplements. Each supplement has: Name, Dose, Benefit.</p>', unsafe_allow_html=True)
    
    # Add/Remove buttons
    sup_col1, sup_col2, sup_col3 = st.columns([1, 1, 4])
    with sup_col1:
        if st.form_submit_button('➕ Add Supplement', use_container_width=True, type='secondary'):
            st.session_state.supplements_count += 1
    with sup_col2:
        if st.form_submit_button('➖ Remove', use_container_width=True, type='secondary') and st.session_state.supplements_count > 1:
            st.session_state.supplements_count -= 1
    
    supplements = []
    for i in range(st.session_state.supplements_count):
        st.markdown(f'**Supplement {i+1}**')
        sc1, sc2, sc3 = st.columns([2, 1, 2])
        with sc1:
            sup_name = st.text_input(f'Name {i+1}',
                value=['Vitamin D3', 'Omega 3', 'C + Zinc'][i] if i < 3 else '',
                key=f'sup_name_{i}', help=f'Supplement {i+1} name.')
        with sc2:
            sup_dose = st.text_input(f'Dose {i+1}',
                value=['2000 IU', 'يومياً', 'يومياً'][i] if i < 3 else '',
                key=f'sup_dose_{i}', help=f'Supplement {i+1} dosage.')
        with sc3:
            sup_benefit = st.text_input(f'Benefit {i+1}',
                value=['دعم المناعة والعظام', 'صحة المفاصل والقلب', 'مناعة + تعافي عضلي'][i] if i < 3 else '',
                key=f'sup_ben_{i}', help=f'Supplement {i+1} benefit.')
        
        if sup_name.strip():
            supplements.append({'name': sup_name.strip(), 'dose': sup_dose.strip(), 'benefit': sup_benefit.strip()})
    
    # ═══════════════════════════════════════════════
    # PRE-WORKOUT - DYNAMIC ADD/REMOVE
    # ═══════════════════════════════════════════════
    st.markdown('---')
    st.markdown('## ⚡ PRE-WORKOUT PROTOCOL')
    st.markdown('<p class="section-desc">Add or remove pre-workout items. Each has: Time, Item.</p>', unsafe_allow_html=True)
    
    pw_col1, pw_col2, pw_col3 = st.columns([1, 1, 4])
    with pw_col1:
        if st.form_submit_button('➕ Add Pre-Workout', use_container_width=True, type='secondary'):
            st.session_state.preworkout_count += 1
    with pw_col2:
        if st.form_submit_button('➖ Remove', use_container_width=True, type='secondary', key='pw_remove') and st.session_state.preworkout_count > 1:
            st.session_state.preworkout_count -= 1
    
    preworkout = []
    for i in range(st.session_state.preworkout_count):
        st.markdown(f'**Pre-Workout Item {i+1}**')
        pw1, pw2 = st.columns([1, 2])
        with pw1:
            pw_time = st.text_input(f'Time {i+1}',
                value=['قبل 45 دقيقة', 'قبل 30 دقيقة'][i] if i < 2 else '',
                key=f'pw_time_{i}', help=f'When to take this item.')
        with pw2:
            pw_item = st.text_input(f'Item {i+1}',
                value=['30 جرام بروتين + 100 جرام تمر + عصير رمان طازج', 'فنجان قهوة سوداء بدون سكر'][i] if i < 2 else '',
                key=f'pw_item_{i}', help=f'What to take.')
        
        if pw_time.strip() and pw_item.strip():
            preworkout.append({'time': pw_time.strip(), 'item': pw_item.strip()})
    
    # ═══════════════════════════════════════════════
    # RECIPES - DYNAMIC ADD/REMOVE
    # ═══════════════════════════════════════════════
    st.markdown('---')
    st.markdown('## 🍳 RECIPES')
    st.markdown('<p class="section-desc">Add or remove recipe cards. Each recipe has: Name, Description, YouTube Link.</p>', unsafe_allow_html=True)
    
    rec_col1, rec_col2, rec_col3 = st.columns([1, 1, 4])
    with rec_col1:
        if st.form_submit_button('➕ Add Recipe', use_container_width=True, type='secondary'):
            st.session_state.recipes_count += 1
    with rec_col2:
        if st.form_submit_button('➖ Remove', use_container_width=True, type='secondary', key='rec_remove') and st.session_state.recipes_count > 1:
            st.session_state.recipes_count -= 1
    
    recipes = []
    for i in range(st.session_state.recipes_count):
        st.markdown(f'**Recipe {i+1}**')
        rc1, rc2, rc3 = st.columns([2, 2, 1])
        with rc1:
            rname = st.text_input(f'Name {i+1}',
                value=['السيرة', 'صدور الدجاج', 'الأرز الصحي', 'سلطة فواكه', 'الباكيج الصحي', 'الوجبة السحرة'][i] if i < 6 else '',
                key=f'rname_{i}', help=f'Recipe {i+1} name.')
        with rc2:
            rdesc = st.text_input(f'Description {i+1}',
                value=['شوربة احترافي', 'تتبيل مثالي وإتقان', 'طريقة طهي صحية', 'وصفة غنية غذائياً', 'بروتين + طاقة', 'سناكس مستقبلة'][i] if i < 6 else '',
                key=f'rdesc_{i}', help=f'Recipe {i+1} description.')
        with rc3:
            rlink = st.text_input(f'Link {i+1}', 'https://youtube.com/watch?v=example', key=f'rlink_{i}', help=f'YouTube link.')
        
        if rname.strip():
            recipes.append({'name': rname.strip(), 'desc': rdesc.strip(), 'link': rlink.strip()})
    
    # ═══════════════════════════════════════════════
    # COACH INFO
    # ═══════════════════════════════════════════════
    st.markdown('---')
    st.markdown('## 🧑‍🏫 COACH INFORMATION')
    st.markdown('<p class="section-desc">Your contact details for the PDF.</p>', unsafe_allow_html=True)
    
    cc1, cc2, cc3 = st.columns(3)
    with cc1:
        coach_name = st.text_input('Coach Name', 'Ahmed Teka', help='Your full name.')
    with cc2:
        instagram = st.text_input('Instagram', '@coach.teka1', help='Your Instagram handle.')
    with cc3:
        phone = st.text_input('Phone', '01033047057', help='Your phone number.')
    
    # ═══════════════════════════════════════════════
    # GENERATE BUTTON
    # ═══════════════════════════════════════════════
    st.markdown('---')
    st.markdown('<div class="gen-btn">', unsafe_allow_html=True)
    submitted = st.form_submit_button('🥗 GENERATE NUTRITION PLAN PDF', use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

if submitted:
    if not client_name:
        st.error('❌ Please enter client name.')
    else:
        with st.spinner('🔄 Creating your premium nutrition plan...'):
            try:
                data = {
                    'client_name': client_name, 'full_name': full_name,
                    'age': age, 'weight': weight, 'height': height,
                    'goal': goal, 'notes': notes,
                    'duration': duration, 'meals_count': meals_count,
                    'start_date': start_date,
                    'protein_g': protein_g, 'carbs_g': carbs_g, 'fat_g': fat_g,
                    'main_meals': main_meals, 'total_calories': total_calories,
                    'water': water, 'meals': meals,
                    'meal_timing': meal_timing, 'food_weighing': food_weighing,
                    'drinks': drinks, 'sweets': sweets, 'omega': omega,
                    'supplements': supplements, 'preworkout': preworkout,
                    'recipes': recipes,
                    'coach_name': coach_name, 'instagram': instagram, 'phone': phone,
                }
                
                pdf_bytes = generate_nutrition_pdf(data)
                st.markdown('<div class="success-box">✅ NUTRITION PLAN PDF GENERATED!</div>', unsafe_allow_html=True)
                st.download_button('📥 DOWNLOAD PDF', data=pdf_bytes, file_name=f'AhmedTeka_Nutrition_{client_name}.pdf', mime='application/pdf', use_container_width=True)
                
            except Exception as e:
                st.error(f'❌ Error: {str(e)}')
                import traceback
                st.code(traceback.format_exc())

st.markdown('---')
st.markdown('<p style="text-align:center;color:#777">© AHMED TEKA · @coach.teka1 · 01033047057</p>', unsafe_allow_html=True)