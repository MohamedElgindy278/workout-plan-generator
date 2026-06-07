import streamlit as st
from datetime import datetime
from nutrition_generator import generate_nutrition_pdf

st.set_page_config(page_title='AHMED TEKA - Nutrition Plan', page_icon='🥗', layout='wide')

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;900&display=swap');
*{font-family:'Cairo',sans-serif!important}
.main-header{background:linear-gradient(135deg,#F8F8F8,#E8F5F0);padding:1.5rem;border-radius:15px;text-align:center;border:2px solid #2E7D64;margin-bottom:1.5rem}
.main-header h1{color:#2E7D64;font-size:2rem;font-weight:900;margin:0}
.stButton>button{background:linear-gradient(135deg,#2E7D64,#3A9B7A);color:#FFF;font-weight:700;font-size:1.2rem;padding:1rem;border-radius:10px;border:none;width:100%}
.stButton>button:hover{background:linear-gradient(135deg,#3A9B7A,#D4AF37)}
label{color:#2E7D64!important;font-weight:600!important}
input,textarea,select{background-color:#FFF!important;color:#1A1A1A!important;border:2px solid #E0E0E0!important;border-radius:8px!important}
input:focus,textarea:focus{border-color:#2E7D64!important;box-shadow:0 0 5px rgba(46,125,100,0.3)!important}
.day-header{background:linear-gradient(135deg,#E8F5F0,#FFF);padding:1rem;border-radius:10px;border-left:5px solid #2E7D64;margin:1rem 0}
.success-box{background:linear-gradient(135deg,#E8F5F0,#FFF);border:2px solid #2E7D64;border-radius:10px;padding:2rem;text-align:center;color:#2E7D64;font-size:1.3rem;font-weight:700}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-header"><h1>🥗 AHMED TEKA — NUTRITION PLAN</h1><p>Personalized Meal Plan Generator</p></div>', unsafe_allow_html=True)

with st.form('nutrition_form'):
    st.markdown('## 👤 CLIENT INFORMATION')
    
    col1, col2, col3 = st.columns(3)
    with col1:
        client_name = st.text_input('Client Name', 'Mohamed', help='Name on the cover page')
        age = st.text_input('Age', '28', help='Client age')
        weight = st.text_input('Weight (kg)', '80', help='Current weight')
    with col2:
        full_name = st.text_input('Full Name', 'Mohamed Ahmed', help='Full name for profile page')
        height = st.text_input('Height (cm)', '175', help='Client height')
        goal = st.text_input('Goal', 'Muscle Building', help='Training goal')
    with col3:
        duration = st.text_input('Duration', '12 Weeks', help='Plan duration')
        meals_count = st.text_input('Meals per Day', '4', help='Number of meals')
        start_date = st.text_input('Start Date', datetime.now().strftime('%B %Y').upper(), help='Start month/year')
    
    notes = st.text_area('Coach Notes', 'Customized meal plan for muscle building under Coach Ahmed Teka supervision.', height=70)
    
    st.markdown('---')
    st.markdown('## 📊 MACRONUTRIENTS')
    
    mcol1, mcol2, mcol3, mcol4 = st.columns(4)
    with mcol1:
        protein_g = st.text_input('Protein (g/day)', '180')
    with mcol2:
        carbs_g = st.text_input('Carbs (g/day)', '280')
    with mcol3:
        fat_g = st.text_input('Fat (g/day)', '65')
    with mcol4:
        water = st.text_input('Water (L/day)', '4-6')
    
    total_calories = st.text_input('Total Daily Calories', '2502')
    
    st.markdown('---')
    st.markdown('## 🍽️ MEALS')
    
    num_meals = st.number_input('Number of meals', 1, 8, 4)
    meals = []
    
    food_icons = ['🍳 Breakfast', '💪 Pre-Workout', '🍗 Lunch', '🥗 Dinner', '🍝 Snack 1', '🥤 Snack 2']
    
    for i in range(int(num_meals)):
        st.markdown(f'<div class="day-header"><h4>{food_icons[i] if i < 6 else "🍽️"} Meal {i+1}</h4></div>', unsafe_allow_html=True)
        
        mc1, mc2 = st.columns([2,1])
        with mc1:
            meal_name = st.text_input(f'Meal Name {i+1}', 
                value=['Breakfast', 'Pre-Workout Meal', 'Lunch', 'Dinner'][i] if i < 4 else f'Meal {i+1}',
                key=f'name_{i}')
        with mc2:
            meal_type = st.text_input(f'Type {i+1}', value=f'Meal {i+1}', key=f'type_{i}')
        
        mc3, mc4, mc5, mc6 = st.columns(4)
        with mc3:
            meal_cal = st.text_input(f'Calories {i+1}', value=['747','750','523','482'][i] if i < 4 else '400', key=f'cal_{i}')
        with mc4:
            meal_protein = st.text_input(f'Protein (g) {i+1}', value=['36','55','45','42'][i] if i < 4 else '30', key=f'prot_{i}')
        with mc5:
            meal_carbs = st.text_input(f'Carbs (g) {i+1}', value=['110','110','55','15'][i] if i < 4 else '40', key=f'carb_{i}')
        with mc6:
            meal_fat = st.text_input(f'Fat (g) {i+1}', value=['18','36','18','12'][i] if i < 4 else '15', key=f'fat_{i}')
        
        ingredients = st.text_area(f'Ingredients {i+1} (one per line)',
            value='\n'.join([
                'Oats 100g', 'Whole milk 200ml', 'Banana 1', 'Nuts 1 tbsp',
                'White rice 150g', 'Chicken breast 200g', 'Mixed vegetables', 'Olive oil 1 tbsp',
                'Brown rice 100g', 'Ground beef 150g', 'Tomato & onion', 'Salad',
                'Eggs 3', 'Cottage cheese 100g', 'Cucumber & tomato', 'Olive oil 1 tbsp',
            ][i*4:(i+1)*4]) if i < 4 else 'Food item 1\nFood item 2\nFood item 3\nFood item 4',
            height=80, key=f'ing_{i}')
        
        alternative = st.text_input(f'Healthy Alternative {i+1}',
            value=['Can replace oats with 4 toast + 2 boiled eggs',
                   'Can replace rice with 200g boiled potato',
                   'Can replace beef with 200g tuna',
                   'Can replace eggs with 120g chicken breast'][i] if i < 4 else 'Healthy alternative option',
            key=f'alt_{i}')
        
        meals.append({
            'name': meal_name, 'type': meal_type,
            'calories': meal_cal, 'protein': meal_protein,
            'carbs': meal_carbs, 'fat': meal_fat,
            'ingredients': [x.strip() for x in ingredients.split('\n') if x.strip()],
            'alternative': alternative,
        })
    
    st.markdown('---')
    
    # Guidelines
    with st.expander('📋 GUIDELINES & SUPPLEMENTS', expanded=False):
        meal_timing = st.text_area('Meal Timing', '2-3 hours between meals to boost metabolism and recovery.', height=60)
        food_weighing = st.text_area('Food Weighing', 'Weigh food after cooking for accurate calorie tracking.', height=60)
        drinks = st.text_area('Drinks', 'No sugary drinks or sweetened beverages. Only water and unsweetened tea.', height=60)
        sweets = st.text_area('Restricted Foods', 'Sugar and processed products are prohibited to maintain cortisol levels.', height=60)
        omega = st.text_input('Omega 3', '3-5g Omega 3 daily distributed across meals')
        
        st.markdown('**Supplements**')
        sup_text = st.text_area('Supplements (name | dose | benefit per line)',
            'Vitamin D3 | 2000 IU | Immune & bone support\nOmega 3 | Daily | Joint & heart health\nC + Zinc | Daily | Immunity + muscle recovery',
            height=80)
        
        supplements = []
        for line in sup_text.split('\n'):
            if '|' in line:
                parts = line.split('|')
                supplements.append({'name': parts[0].strip(), 'dose': parts[1].strip(), 'benefit': parts[2].strip() if len(parts) > 2 else ''})
        
        st.markdown('**Pre-Workout Protocol**')
        pw_text = st.text_area('Pre-workout (time | item per line)',
            '45 min before | 30g protein + 100g dates + fresh pomegranate juice\n30 min before | Cup of black coffee without sugar',
            height=80)
        
        preworkout = []
        for line in pw_text.split('\n'):
            if '|' in line:
                parts = line.split('|')
                preworkout.append({'time': parts[0].strip(), 'item': parts[1].strip()})
    
    # Recipes
    with st.expander('🍳 RECIPES', expanded=False):
        recipes = []
        for i in range(6):
            st.markdown(f'**Recipe {i+1}**')
            rc1, rc2 = st.columns([2,1])
            with rc1:
                rname = st.text_input(f'Name {i+1}', 
                    value=['Oatmeal Protein', 'Chicken Breast', 'Healthy Rice', 'Fruit Salad', 'Protein Pack', 'Magic Smoothie'][i],
                    key=f'rname_{i}')
            with rc2:
                rlink = st.text_input(f'Link {i+1}', 'https://youtube.com/watch?v=example', key=f'rlink_{i}')
            rdesc = st.text_input(f'Description {i+1}', 'Delicious and healthy recipe', key=f'rdesc_{i}')
            recipes.append({'name': rname, 'desc': rdesc, 'link': rlink})
    
    # Coach
    with st.expander('🧑‍🏫 COACH INFO', expanded=False):
        coach_name = st.text_input('Coach Name', 'AHMED TEKA')
        instagram = st.text_input('Instagram', '@coach.teka1')
        phone = st.text_input('Phone', '01033047057')
    
    submitted = st.form_submit_button('🥗 GENERATE NUTRITION PLAN PDF', use_container_width=True)

if submitted:
    if not client_name:
        st.error('Please enter client name')
    else:
        with st.spinner('Creating your nutrition plan...'):
            try:
                data = {
                    'client_name': client_name, 'full_name': full_name,
                    'age': age, 'weight': weight, 'height': height,
                    'goal': goal, 'notes': notes,
                    'duration': duration, 'meals_count': f'{meals_count} Meals',
                    'start_date': start_date,
                    'protein_g': protein_g, 'carbs_g': carbs_g, 'fat_g': fat_g,
                    'water': f'{water} L', 'total_calories': total_calories,
                    'meals': meals,
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
                st.error(f'Error: {str(e)}')

st.markdown('---')
st.markdown('<p style="text-align:center;color:#666">© AHMED TEKA · @coach.teka1 · 01033047057</p>', unsafe_allow_html=True)