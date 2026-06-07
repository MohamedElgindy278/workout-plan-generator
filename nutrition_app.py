import streamlit as st
from datetime import datetime
from nutrition_generator import generate_nutrition_pdf

st.set_page_config(page_title='AHMED TEKA - Nutrition Plan', page_icon='🥗', layout='wide')

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;900&display=swap');
*{font-family:'Cairo',sans-serif!important}
html, body, [class*="css"] {font-family:'Cairo',sans-serif!important}
.main-header{background:linear-gradient(135deg,#080B12,#1A2235);padding:1.5rem;border-radius:15px;text-align:center;border:2px solid #D4AF37;margin-bottom:1.5rem}
.main-header h1{color:#D4AF37;font-size:2rem;font-weight:900;margin:0}
.main-header p{color:#9BA3B2;margin:0.3rem 0 0 0}
.stButton>button{background:linear-gradient(135deg,#D4AF37,#A0832A);color:#080B12;font-weight:700;font-size:1.2rem;padding:1rem;border-radius:10px;border:none;width:100%}
.stButton>button:hover{background:linear-gradient(135deg,#E8C84A,#D4AF37)}
.gen-btn>button{background:linear-gradient(135deg,#D4AF37,#FF6B35)!important;color:#000!important;font-size:1.5rem!important;padding:1.5rem!important;font-weight:900!important;animation:pulse 1.5s infinite}
@keyframes pulse{0%{box-shadow:0 0 0 0 rgba(212,175,55,0.4)}70%{box-shadow:0 0 0 25px rgba(212,175,55,0)}100%{box-shadow:0 0 0 0 rgba(212,175,55,0)}}
label{color:#D4AF37!important;font-weight:600!important}
input,textarea,select{background-color:#1A2235!important;color:#E8E4DC!important;border:2px solid #374151!important;border-radius:8px!important;font-family:'Cairo',sans-serif!important}
input:focus,textarea:focus{border-color:#D4AF37!important;box-shadow:0 0 5px rgba(212,175,55,0.3)!important}
.day-header{background:linear-gradient(135deg,#1A2235,#080B12);padding:1rem;border-radius:10px;border-left:5px solid #D4AF37;margin:1rem 0}
.day-header h4{color:#D4AF37;margin:0}
.success-box{background:linear-gradient(135deg,#1C1A08,#2A2208);border:2px solid #D4AF37;border-radius:10px;padding:2rem;text-align:center;color:#D4AF37;font-size:1.5rem;font-weight:900}
.section-desc{color:#6B7280;font-size:0.85rem;margin-bottom:1rem}
div[data-baseweb="tooltip"]{background-color:#FFFFFF!important;color:#080B12!important;font-weight:600!important;border:2px solid #D4AF37!important}
div[data-baseweb="tooltip"] p{color:#080B12!important;font-weight:500!important}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-header"><h1>🥗 AHMED TEKA — NUTRITION PLAN</h1><p>Professional · Personalized Meal Plan Generator</p></div>', unsafe_allow_html=True)

# Initialize session states
for i in range(8):
    if f'ing_count_{i}' not in st.session_state:
        st.session_state[f'ing_count_{i}'] = 4

with st.form('nutrition_form'):
    
    st.markdown('## 📋 COVER PAGE INFORMATION')
    st.markdown('<p class="section-desc">These details appear on the cover page of the PDF.</p>', unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns(3)
    with c1:
        client_name = st.text_input('👤 Client Name', 'محمد', help='Client name displayed on the cover page.')
        full_name = st.text_input('📛 Full Name', 'محمد أحمد', help='Full name for the profile page.')
        age = st.text_input('🎂 Age', '28 سنة', help='Client age.')
    with c2:
        weight = st.text_input('⚖️ Weight', '80 كجم', help='Current body weight.')
        height = st.text_input('📏 Height', '175 سم', help='Client height.')
        goal = st.text_input('🎯 Goal', 'بناء عضلي', help='Primary nutrition goal.')
    with c3:
        duration = st.text_input('⏱️ Duration', '12 أسبوع', help='Plan duration.')
        meals_count_text = st.text_input('🍽️ Meals Count', '4 وجبات', help='Number of meals per day.')
        start_date = st.text_input('📅 Start Date', 'يونيو 2026', help='Program start month/year.')
    
    notes = st.text_area('📝 Coach Notes', 'نظام مخصص بالكامل لزيادة الكتلة العضلية تحت إشراف المدرب أحمد تيكا', height=70,
        help='Special notes from the coach.')
    
    st.markdown('---')
    st.markdown('## 📊 MACRONUTRIENTS')
    
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        protein_g = st.text_input('🥩 Protein (g/day)', '180')
    with m2:
        carbs_g = st.text_input('🍚 Carbs (g/day)', '280')
    with m3:
        fat_g = st.text_input('🧈 Fat (g/day)', '65')
    with m4:
        main_meals = st.text_input('🍽️ Main Meals/Day', '4')
    
    total_calories = st.text_input('🔥 Total Daily Calories', '2502')
    
    st.markdown('---')
    st.markdown('## 🍽️ MEALS')
    st.markdown('<p class="section-desc">Configure each meal. Paste an image URL for the meal icon.</p>', unsafe_allow_html=True)
    
    num_meals = st.number_input('Number of meals', 1, 8, 4, help='How many meals in the plan? (1-8)')
    meals = []
    
    for i in range(int(num_meals)):
        st.markdown(f'<div class="day-header"><h4>Meal {i+1}</h4></div>', unsafe_allow_html=True)
        
        mc1, mc2, mc3 = st.columns([2, 2, 1])
        with mc1:
            meal_name = st.text_input(f'🍳 Meal Name {i+1}',
                value=['وجبة الإفطار', 'وجبة ما قبل التمرين', 'الوجبة الرئيسية الثالثة', 'وجبة العشاء'][i] if i < 4 else f'وجبة {i+1}',
                key=f'name_{i}')
        with mc2:
            meal_type = st.text_input(f'📋 Meal Type {i+1}',
                value=['الوجبة الأولى', 'الوجبة الثانية', 'الوجبة الثالثة', 'الوجبة الرابعة'][i] if i < 4 else f'الوجبة {i+1}',
                key=f'type_{i}')
        with mc3:
            meal_icon_url = st.text_input(f'🖼️ Icon URL {i+1}',
                value='',
                key=f'micon_{i}',
                placeholder='https://...',
                help='Paste an image URL for the meal icon (e.g., from imgur.com)')
        
        mc4, mc5, mc6, mc7 = st.columns(4)
        with mc4:
            meal_cal = st.text_input(f'🔥 Calories {i+1}', value=['747','750','523','482'][i] if i < 4 else '400', key=f'cal_{i}')
        with mc5:
            meal_protein = st.text_input(f'🥩 Protein (g) {i+1}', value=['36','55','45','42'][i] if i < 4 else '30', key=f'prot_{i}')
        with mc6:
            meal_carbs = st.text_input(f'🍚 Carbs (g) {i+1}', value=['110','110','55','15'][i] if i < 4 else '40', key=f'carb_{i}')
        with mc7:
            meal_fat = st.text_input(f'🧈 Fat (g) {i+1}', value=['18','36','18','12'][i] if i < 4 else '15', key=f'fat_{i}')
        
        alternative = st.text_input(f'🔄 Healthy Alternative {i+1}',
            value=['يمكن استبدال الأوتس بـ 4 توست + بيضتان مسلوقتان',
                   'يمكن استبدال الأرز بـ بطاطس مسلوقة 200 جم',
                   'يمكن استبدال اللحم بـ سمك تونة 200 جم',
                   'يمكن استبدال البيض بـ صدر دجاج 120 جم'][i] if i < 4 else 'بديل صحي',
            key=f'alt_{i}')
        
        st.markdown(f'**🛒 Ingredients**')
        ing_col1, ing_col2, ing_col3 = st.columns([1, 1, 4])
        with ing_col1:
            if st.form_submit_button(f'➕ Add', use_container_width=True, key=f'add_ing_{i}'):
                st.session_state[f'ing_count_{i}'] += 1
        with ing_col2:
            if st.form_submit_button(f'➖ Remove', use_container_width=True, key=f'rem_ing_{i}') and st.session_state[f'ing_count_{i}'] > 1:
                st.session_state[f'ing_count_{i}'] -= 1
        
        ingredients = []
        default_ingredients = [
            ['شيكلات أوتس 100 جم', 'حليب كامل الدسم 200 مل', 'موز حبة واحدة', 'مكسرات ملعقة كبيرة'],
            ['أرز أبيض مسلوق 150 جم', 'صدر دجاج مشوي 200 جم', 'خضار مشكلة', 'زيت زيتون ملعقة'],
            ['أرز بني 100 جم', 'لحم بقري مفروم 150 جم', 'طماطم وبصل', 'خضار سلطة'],
            ['بيض 3 حبات', 'جبن قريش 100 جم', 'خيار وطماطم', 'زيت زيتون ملعقة'],
        ]
        
        for j in range(st.session_state[f'ing_count_{i}']):
            default_val = default_ingredients[i][j] if i < 4 and j < len(default_ingredients[i]) else f'مكون {j+1}'
            ing = st.text_input(f'{j+1}', value=default_val, key=f'ing_{i}_{j}', label_visibility='collapsed')
            if ing.strip():
                ingredients.append(ing.strip())
        
        meals.append({
            'name': meal_name, 'type': meal_type, 'icon': meal_icon_url,
            'calories': meal_cal, 'protein': meal_protein,
            'carbs': meal_carbs, 'fat': meal_fat,
            'ingredients': ingredients, 'alternative': alternative,
        })
    
    st.markdown('---')
    st.markdown('## 📋 GUIDELINES')
    
    water = st.text_input('💧 Daily Water Intake', '4-6 لتر')
    
    g1, g2 = st.columns(2)
    with g1:
        meal_timing = st.text_area('⏰ Meal Timing', 'الفترة بين الوجبات 2-3 ساعات لتعزيز الأيض والاستشفاء', height=70)
        drinks = st.text_area('🥤 Drinks', 'ممنوع السكريات والمشروبات المحلاة، فقط ماء وشاي بدون سكر', height=70)
    with g2:
        food_weighing = st.text_area('⚖️ Food Weighing', 'وزن الأطعمة بالميزان بعد الطهي لضبط السعرات بدقة', height=70)
        sweets = st.text_area('🚫 Restricted Foods', 'السكريات والمنتجات المصنعة ممنوعة للحفاظ على الكورتيزول', height=70)
    
    omega = st.text_input('🐟 Omega-3', '5-3 جم أوميجا 3 يومياً موزعاً على الوجبات')
    
    st.markdown('---')
    st.markdown('## 💊 SUPPLEMENTS')
    
    sup_text = st.text_area('Supplements (name | dose | benefit per line)',
        'Vitamin D3 | 2000 IU | دعم المناعة والعظام\nOmega 3 | يومياً | صحة المفاصل والقلب\nC + Zinc | يومياً | مناعة + تعافي عضلي',
        height=80)
    
    supplements = []
    for line in sup_text.split('\n'):
        if '|' in line:
            parts = line.split('|')
            supplements.append({'name': parts[0].strip(), 'dose': parts[1].strip(), 'benefit': parts[2].strip() if len(parts) > 2 else ''})
    
    st.markdown('---')
    st.markdown('## ⚡ PRE-WORKOUT PROTOCOL')
    
    pw_text = st.text_area('Pre-workout (time | item per line)',
        'قبل 45 دقيقة | 30 جرام بروتين + 100 جرام تمر + عصير رمان طازج\nقبل 30 دقيقة | فنجان قهوة سوداء بدون سكر',
        height=80)
    
    preworkout = []
    for line in pw_text.split('\n'):
        if '|' in line:
            parts = line.split('|')
            preworkout.append({'time': parts[0].strip(), 'item': parts[1].strip()})
    
    st.markdown('---')
    st.markdown('## 🍳 RECIPES')
    st.markdown('<p class="section-desc">Paste image URLs for recipe photos. Also add YouTube links.</p>', unsafe_allow_html=True)
    
    recipes = []
    for i in range(6):
        rc1, rc2, rc3, rc4 = st.columns([2, 2, 1, 1])
        with rc1:
            rname = st.text_input(f'Name {i+1}',
                value=['السيرة', 'صدور الدجاج', 'الأرز الصحي', 'سلطة فواكه', 'الباكيج الصحي', 'الوجبة السحرة'][i],
                key=f'rname_{i}')
        with rc2:
            rdesc = st.text_input(f'Description {i+1}',
                value=['شوربة احترافي', 'تتبيل مثالي وإتقان', 'طريقة طهي صحية', 'وصفة غنية غذائياً', 'بروتين + طاقة', 'سناكس مستقبلة'][i],
                key=f'rdesc_{i}')
        with rc3:
            rlink = st.text_input(f'Video Link {i+1}', 'https://youtube.com/watch?v=example', key=f'rlink_{i}')
        with rc4:
            rimage = st.text_input(f'Image URL {i+1}', '', key=f'rimage_{i}', placeholder='https://...',
                help='Paste an image URL for the recipe photo')
        if rname.strip():
            recipes.append({'name': rname.strip(), 'desc': rdesc.strip(), 'link': rlink.strip(), 'image': rimage.strip()})
    
    st.markdown('---')
    st.markdown('## 🧑‍🏫 COACH INFORMATION')
    
    cc1, cc2, cc3 = st.columns(3)
    with cc1:
        coach_name = st.text_input('Coach Name', 'Ahmed Teka')
    with cc2:
        instagram = st.text_input('Instagram', '@coach.teka1')
    with cc3:
        phone = st.text_input('Phone', '01033047057')
    
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
                    'duration': duration, 'meals_count': meals_count_text,
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
st.markdown('<p style="text-align:center;color:#6B7280">© AHMED TEKA · @coach.teka1 · 01033047057</p>', unsafe_allow_html=True)