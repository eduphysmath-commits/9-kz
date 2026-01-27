import streamlit as st
import requests
import streamlit.components.v1 as components
import json

# --- БАПТАУЛАР ---
URL = "https://iuqdbdvmbewaedgydaah.supabase.co"
KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Iml1cWRiZHZtYmV3YWVkZ3lkYWFoIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjkzMjE5ODgsImV4cCI6MjA4NDg5Nzk4OH0.a_PPVZWcA3qOfT4cNaXNE_a3xuSv0CHyrY8LbTgjWww"

# --- ЖАҢА КЕСТЕ АТАУЫ ---
TABLE_NAME = "tjb_9_kaz"  # Осы жерді өзгерттік (tjb_9_rus -> tjb_9_kaz)

st.set_page_config(page_title="Физика 9-сынып БЖБ", layout="wide", page_icon="🪐")

if 'submitted' not in st.session_state:
    st.session_state.submitted = False

# --- 1. КӨШІРУДЕН ҚОРҒАУ (CSS) ---
st.markdown("""
    <style>
    * { -webkit-user-select: none; user-select: none; } 
    .stRadio > div { background-color: white; padding: 15px; border-radius: 10px; border: 1px solid #e0e0e0; margin-bottom: 10px; }
    .main { background-color: #f8f9fa; }
    </style>
    <script>
    document.addEventListener('contextmenu', event => event.preventDefault()); 
    document.onkeydown = function(e) {
        if (e.ctrlKey && (e.keyCode === 67 || e.keyCode === 85 || e.keyCode === 83 || e.keyCode === 73)) return false; 
    };
    </script>
    """, unsafe_allow_html=True)

def post_to_supabase(data):
    headers = {"apikey": KEY, "Authorization": f"Bearer {KEY}", "Content-Type": "application/json"}
    # Сілтеме енді жаңа кестеге бағытталды
    return requests.post(f"{URL}/rest/v1/{TABLE_NAME}", json=data, headers=headers)

# --- 2. ИНТЕРФЕЙС ---
st.title("🪐 ФИЗИКА, 9-СЫНЫП. 1-ЖАРТЫЖЫЛДЫҚ БОЙЫНША ЖИЫНТЫҚ БАҒАЛАУ")

if not st.session_state.submitted:
    st.info("⏱ Уақыты: 45 минут | Жалпы ұпай: 25 ұпай")
    
    st.subheader("👤 Оқушы туралы мәлімет")
    col1, col2 = st.columns(2)
    with col1:
        student_name = st.text_input("Аты-жөнінізді жазыңыз:", placeholder="Мысалы: Асан Үсенов")
    with col2:
        student_class = st.selectbox("Сыныбыңызды таңдаңыз:", ["9 А", "9 Ә", "9 Б", "9 В"])
    
    if not student_name:
        st.warning("☝️ Тестті бастау үшін аты-жөнінізді жазыңыз.")
    else:
        st.success(f"Сәлем, {student_name}! Тапсырмаларды орындауға кірісуіңізге болады.")
        st.warning("⚠️ Назар аударыңыз: Беттен 5 секундтан артық шығып кетсеңіз, жұмыс жойылады!")

# --- 3. ANTI-CHEAT JS ---
if not st.session_state.submitted and 'student_name' in locals() and student_name:
    components.html(f"""
        <script>
        let timeout;
        let audioUnlocked = false;

        function unlockAudio() {{
            if (!audioUnlocked) {{
                const msg = new SpeechSynthesisUtterance("");
                window.speechSynthesis.speak(msg);
                audioUnlocked = true;
            }}
        }}
        window.parent.document.addEventListener('mousedown', unlockAudio);

        function speak(text) {{
            window.speechSynthesis.cancel(); 
            const msg = new SpeechSynthesisUtterance(text);
            msg.lang = 'ru-RU'; 
            window.speechSynthesis.speak(msg);
        }}

        document.addEventListener("visibilitychange", function() {{
            if (document.hidden) {{
                speak("Назар аударыңыз! Тестке дереу қайта оралыңыз! 5 секундыңыз қалды!");
                alert("НАЗАР АУДАРЫҢЫЗ! Сіз беттен шығып кеттіңіз. 5 секундтан кейін жұмыс жойылады!");
                
                timeout = setTimeout(function() {{
                    fetch('{URL}/rest/v1/{TABLE_NAME}', {{
                        method: 'POST',
                        headers: {{ 'apikey': '{KEY}', 'Authorization': 'Bearer {KEY}', 'Content-Type': 'application/json' }},
                        body: JSON.stringify({{
                            student_name: '{student_name}',
                            student_class: '{student_class}',
                            status: 'cheated',
                            ai_feedback: 'Жұмыс ЖОЙЫЛДЫ: оқушы басқа бетке өтіп кетті.'
                        }})
                    }}).then(() => {{ window.parent.location.reload(); }});
                }}, 5000);
            }} else {{
                clearTimeout(timeout);
                window.speechSynthesis.cancel();
            }}
        }});
        </script>
    """, height=0)

# --- 4. ТЕСТ ФОРМАСЫ ---
if not st.session_state.submitted:
    with st.form("main_physics_form"):
        # А БӨЛІМІ
        st.subheader("📍 А БӨЛІМІ: Тест тапсырмалары (10 ұпай)")
        
        q1 = st.radio("1. Материялық нүкте шеңбер бойымен қозғалып, бастапқы нүктесіне қайта келді. Орын ауыстыруы (S) мен жүрген жолы (l) қандай болады?", 
                      ["A) S = 2πR; l = 0", "B) S = 0; l = 2πR", "C) S = 0; l = 0", "D) S = 2πR; l = 2πR"], index=None)
        q2 = st.radio("2. Дене 5 секунд ішінде жылдамдығын 0-ден 10 м/с-қа дейін бірқалыпты арттырды. Дененің үдеуін анықтаңыз.", 
                      ["A) 5 м/с²", "B) 2 м/с²", "C) 10 м/с²", "D) 0 м/с²"], index=None)
        q3 = st.radio("3. Аспан сферасындағы жұлдыздардың өзара орналасуын сақтайтын тұрақты топтар қалай аталады?", 
                      ["A) Галактикалар", "B) Планеталар", "C) Шоқжұлдыздар", "D) Тұмандықтар"], index=None)
        q4 = st.radio("4. Инерциялық санақ жүйесі деп қандай жүйені айтамыз?", 
                      ["A) Дене үдеумен қозғалатын жүйе", "B) Дене тыныштықта болатын немесе бірқалыпты түзусызықты қозғалатын жүйе", "C) Дене шеңбер бойымен қозғалатын жүйе", "D) Кез келген санақ жүйесі"], index=None)
        q5 = st.radio("5. Жер бетіндегі денелерге әсер ететін ауырлық күшінің формуласы:", 
                      ["A) F = kx", "B) F = μN", "C) F = mg", "D) F = ma"], index=None)
        q6 = st.radio("6. Ньютонның үшінші заңы бойынша күштер:", 
                      ["A) Әр түрлі денелерге әсер етеді, бағыттары қарама-қарсы, шамалары тең", "B) Бір денеге әсер етеді, теңгеріледі", "C) Бағыттары бірдей, шамалары әр түрлі", "D) Тек тыныштықтағы денелерге әсер етеді"], index=None)
        q7 = st.radio("7. Егер екі дене арасындағы қашықтықты 2 есе арттырсақ, тартылыс күші қалай өзгереді?", 
                      ["A) 2 есе артады", "B) 2 есе кемиді", "C) 4 есе артады", "D) 4 есе кемиді"], index=None)
        q8 = st.radio("8. Кеплердің 1-заңы бойынша ғаламшарлар Күнді айнала қандай траекториямен қозғалады?", 
                      ["A) Шеңбер бойымен", "B) Эллипс бойымен", "C) Парабола бойымен", "D) Түзу сызық бойымен"], index=None)
        q9 = st.radio("9. Центрге тартқыш үдеудің формуласы:", 
                      ["A) a = v/t", "B) a = v²/R", "C) a = ωR", "D) a = 4π²R"], index=None)
        q10 = st.radio("10. Лифт 10 м/с² үдеумен (еркін түсу үдеуіне тең) төмен құлағанда, ішіндегі жолаушының салмағы қандай болады?", 
                      ["A) P = mg", "B) P = 2mg", "C) P = 0 (Салмақсыздық)", "D) P = m(g-a)"], index=None)

        # В БӨЛІМІ
        st.subheader("📍 В БӨЛІМІ: Қысқа жауапты және түсіндірмелі тапсырмалар (12 ұпай)")
        
        st.markdown("**11-тапсырма. Инерция құбылысы (4 ұпай)**")
        q11a = st.text_input("а) Бұл құбылыс физикада қалай аталады?")
        q11b = st.text_input("b) Өмірден осы құбылысқа тағы бір басқа мысал келтіріңіз:")
        
        st.markdown("**12-тапсырма. Динамика есебі (m = 2 кг, F = 8 Н) (5 ұпай)**")
        q12a = st.text_area("а) Дененің үдеуін есептеңіз (Формула және есептелуі):")
        q12b = st.text_area("b) Егер денеге әсер ететін күшті 2 есе арттырсақ, оның үдеуі қалай өзгереді? (Түсіндіріңіз):")
        
        st.markdown("**13-тапсырма. Астрономия (3 ұпай)**")
        q13a = st.text_input("а) Жұлдыз бен ғаламшардың (планетаның) ең негізгі айырмашылығы неде?")
        q13b = st.text_input("b) Күн жүйесіндегі ең үлкен ғаламшарды атаңыз:")

        # С БӨЛІМІ
        st.subheader("📍 С БӨЛІМІ: Құрылымдалған тапсырма (3 ұпай)")
        st.markdown("**14-тапсырма. Горизонталь лақтырылған дене (h=20м, v0=10м/с)**")
        q14a = st.text_input("a) Доптың жерге түсу уақытын (t) анықтаңыз (h = gt²/2):")
        q14b = st.text_input("b) Доп мұнара табанынан қандай қашықтыққа (L) түседі? (L = v₀ ∙ t):")
        q14c = st.text_input("c) Доптың траекториясы қандай пішінде болады?")

        submit = st.form_submit_button("Аяқтау және жіберу ✅")

    if submit:
        if 'student_name' not in locals() or not student_name:
            st.error("❌ Өтініш, беттің басында Аты-жөніңізді енгізіңіз!")
        else:
            all_answers = {
                "section_a": [q1, q2, q3, q4, q5, q6, q7, q8, q9, q10],
                "section_b": {"11": [q11a, q11b], "12": [q12a, q12b], "13": [q13a, q13b]},
                "section_c": {"14": [q14a, q14b, q14c]}
            }
            payload = {
                "student_name": student_name, "student_class": student_class,
                "answers": all_answers, "status": "pending"
            }
            res = post_to_supabase(payload)
            if res.status_code in [200, 201]:
                st.session_state.submitted = True
                st.balloons()
                st.success("Жауаптарыңыз сәтті жіберілді!")
                st.rerun()

# --- 5. НӘТИЖЕНІ ІЗДЕУ ---
st.markdown("---")
st.subheader("🔎 Нәтижені тексеру")
search_name = st.text_input("Нәтижені іздеу үшін аты-жөніңізді жазыңыз:")
if search_name:
    search_headers = {"apikey": KEY, "Authorization": f"Bearer {KEY}"}
    # Іздеу бөлімінде де жаңа кестені қолданамыз
    res = requests.get(f"{URL}/rest/v1/{TABLE_NAME}?student_name=eq.{search_name}&select=*&order=id.desc", headers=search_headers)
    if res.status_code == 200 and res.json():
        result = res.json()[0]
        if result['status'] == 'cheated':
            st.error(f"🚫 Жұмыс жойылды. Себебі: {result['ai_feedback']}")
        elif result['status'] == 'pending':
            st.warning("⏳ Жұмыс әлі тексерілуде...")
        else:
            st.metric("Балл:", f"{result.get('score', 0)} / 25")
            st.info(f"Мұғалім пікірі: {result['ai_feedback']}")
    else:
        st.info("Бұл атпен жұмыс табылмады.")