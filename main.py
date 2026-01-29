import streamlit as st
import requests
import streamlit.components.v1 as components
import json

# --- 1. БАЗА БАПТАУЛАРЫ ---
URL = "https://iuqdbdvmbewaedgydaah.supabase.co"
KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Iml1cWRiZHZtYmV3YWVkZ3lkYWFoIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjkzMjE5ODgsImV4cCI6MjA4NDg5Nzk4OH0.a_PPVZWcA3qOfT4cNaXNE_a3xuSv0CHyrY8LbTgjWww"

st.set_page_config(page_title="Физика БЖБ - 9 сынып", layout="wide")

if 'submitted' not in st.session_state:
    st.session_state.submitted = False

# --- 2. СТИЛЬ ---
st.markdown("""
    <style>
    * { -webkit-user-select: none; user-select: none; } 
    .stRadio > div { background-color: white; padding: 15px; border-radius: 10px; border: 1px solid #e0e0e0; margin-bottom: 5px; }
    .stTextInput > div > div > input, .stTextArea > div > div > textarea { background-color: #f9f9f9; }
    </style>
""", unsafe_allow_html=True)

def send_data(payload):
    headers = {"apikey": KEY, "Authorization": f"Bearer {KEY}", "Content-Type": "application/json"}
    # Кестенің атын өзгертусіз қалдырдым, бірақ деректер қазақша барады
    return requests.post(f"{URL}/rest/v1/tjb_9_rus", json=payload, headers=headers)

# --- 3. БАСТЫ БЕТ ---
st.title("🪐 Физика: 1-жартыжылдық бойынша БЖБ")
st.write("9-сынып | Уақыты: 45 минут | Жалпы ұпай: 25")

if st.session_state.submitted:
    st.balloons()
    st.success("✅ Жұмысыңыз сәтті қабылданды! Нәтижені төмендегі іздеу бөлімінен тексере аласыз.")
else:
    st.info("⚠️ Назар аударыңыз: Беттен шығып кетсеңіз немесе басқа вкладкаға өтсеңіз, жұмыс АННУЛИРОВАТЬ етіледі!")
    
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Оқушының аты-жөні:", placeholder="Мысалы: Асанов Арман")
    with col2:
        s_class = st.selectbox("Сыныбы:", ["9 А", "9 Б", "9 В", "9 Г"])

    if name:
        # --- ANTI-CHEAT JS (ТЕК ДАБЫЛ ДЫБЫСЫ) ---
        components.html(f"""
            <script>
            let isSubmitting = false;

            // Дабыл дыбысын шығару функциясы (Beep sound)
            function playAlarm() {{
                if (isSubmitting) return;
                
                try {{
                    const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
                    const oscillator = audioCtx.createOscillator();
                    const gainNode = audioCtx.createGain();

                    oscillator.type = 'sawtooth'; // Дыбыс түрі (өткір дабыл үшін)
                    oscillator.frequency.setValueAtTime(880, audioCtx.currentTime); // Жиілігі (Гц)
                    gainNode.gain.setValueAtTime(0.1, audioCtx.currentTime); // Дыбыс қаттылығы

                    oscillator.connect(gainNode);
                    gainNode.connect(audioCtx.destination);

                    oscillator.start();
                    // 0.5 секундтан кейін дыбысты тоқтату
                    setTimeout(() => oscillator.stop(), 500);
                }} catch (e) {{
                    console.log("Audio error:", e);
                }}
            }}

            // Беттен шығуды бақылау
            document.addEventListener("visibilitychange", function() {{
                if (document.hidden && !isSubmitting) {{
                    // Бірден дабыл қағу
                    playAlarm();
                    
                    // 1 секунд сайын қайталап дабыл қағу
                    let alarmInterval = setInterval(playAlarm, 1000);
                    
                    setTimeout(function() {{
                        if (document.hidden && !isSubmitting) {{
                            clearInterval(alarmInterval); // Интервалды тоқтату
                            
                            fetch('{URL}/rest/v1/tjb_9_rus', {{
                                method: 'POST',
                                headers: {{ 
                                    'apikey': '{KEY}', 
                                    'Authorization': 'Bearer {KEY}', 
                                    'Content-Type': 'application/json' 
                                }},
                                body: JSON.stringify({{
                                    student_name: "{name}",
                                    student_class: "{s_class}",
                                    status: "cheated",
                                    ai_feedback: "Жұмыс ЖОЙЫЛДЫ: Тест кезінде басқа вкладкаға өткені үшін."
                                }})
                            }}).then(() => {{ 
                                isSubmitting = true;
                                window.parent.location.reload(); 
                            }});
                        }} else {{
                            clearInterval(alarmInterval);
                        }}
                    }}, 5000); // 5 секунд ішінде қайтып келмесе - аннулировать
                }}
            }});

            window.onbeforeunload = function() {{
                isSubmitting = true;
            }};
            </script>
        """, height=0)

        # ТЕСТ ФОРМАСЫ
        with st.form("exam_form"):
            st.subheader("📍 А БӨЛІМІ: Тест тапсырмалары (10 ұпай)")
            
            q1 = st.radio("1. Материялық нүкте шеңбер бойымен қозғалып, бастапқы нүктесіне қайта келді. Орын ауыстыруы (S) мен жүрген жолы (l) қандай болады?", 
                          ["A) S = 2πR; l = 0", "B) S = 0; l = 2πR", "C) S = 0; l = 0", "D) S = 2πR; l = 2πR"], index=None)
            
            q2 = st.radio("2. Дене 5 секунд ішінде жылдамдығын 0-ден 10 м/с-қа дейін бірқалыпты арттырды. Дененің үдеуін анықтаңыз:", 
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
            
            q10 = st.radio("10. Лифт 10 м/с² үдеумен (g-ге тең) төмен құлағанда, жолаушының салмағы қандай болады?", 
                           ["A) P = mg", "B) P = 2mg", "C) P = 0 (Салмақсыздық)", "D) P = m(g-a)"], index=None)

            st.subheader("📍 В БӨЛІМІ: Қысқа жауапты тапсырмалар (8 ұпай)")
            st.write("**11-тапсырма. Инерция құбылысы**")
            q11a = st.text_input("11а. Автобус кенет тоқтағанда жолаушылардың алға еңкею құбылысы қалай аталады?")
            q11b = st.text_input("11б. Өмірден инерцияға тағы бір мысал келтіріңіз:")
            
            st.write("**12-тапсырма. Динамика есебі**")
            q12_form = st.text_input("12а. Массасы 2 кг денеге 8 Н күш әсер етеді. Үдеудің формуласын жазыңыз (F=ma):")
            q12_calc = st.text_area("12б. Есептелуі және жауабы (м/с²):")
            q12_change = st.text_input("12в. Егер күшті 2 есе арттырсақ, үдеу қалай өзгереді?")
            
            st.write("**13-тапсырма. Астрономия**")
            q13a = st.text_input("13а. Жұлдыз бен ғаламшардың басты айырмашылығы:")
            q13b = st.text_input("13б. Күн жүйесіндегі ең үлкен ғаламшар:")

            st.subheader("📍 С БӨЛІМІ: Құрылымдалған тапсырма (7 ұпай)")
            st.write("**14-тапсырма. Горизонталь лақтырылған дене (h=20м, v0=10м/с)**")
            q14a = st.text_input("14а. Доптың жерге түсу уақыты t (с):")
            q14b = st.text_input("14б. Доптың түсу қашықтығы L (м):")

            submitted_btn = st.form_submit_button("ЖҰМЫСТЫ АЯҚТАУ ✅")

            if submitted_btn:
                all_answers = {
                    "section_a": [q1, q2, q3, q4, q5, q6, q7, q8, q9, q10],
                    "section_bc": {
                        "11": [q11a, q11b], 
                        "12": [q12_form, q12_calc, q12_change], 
                        "13": [q13a, q13b],
                        "14": [q14a, q14b]
                    }
                }
                
                payload = {
                    "student_name": name, "student_class": s_class,
                    "answers": json.dumps(all_answers), "status": "pending"
                }
                
                resp = send_data(payload)
                if resp.status_code in [200, 201]:
                    st.session_state.submitted = True
                    st.rerun()

# --- 4. НӘТИЖЕНІ ІЗДЕУ ---
st.markdown("---")
st.subheader("🔎 Нәтижені тексеру")
search_query = st.text_input("Аты-жөніңізді жазыңыз:")
if search_query:
    res = requests.get(f"{URL}/rest/v1/tjb_9_rus?student_name=eq.{search_query}&select=*&order=id.desc", headers={"apikey": KEY, "Authorization": f"Bearer {KEY}"})
    results = res.json()
    if results:
        data = results[0]
        if data['status'] == 'cheated': 
            st.error("🚫 Жұмыс жойылды: тест кезінде басқа бетке өткеніңіз үшін.")
        elif data['status'] == 'pending': 
            st.warning("⏳ Мұғалім әлі тексерген жоқ. Күте тұрыңыз...")
        else:
            st.success(f"✅ Балыңыз: {data.get('score', 0)} / 25")
            st.info(f"💬 Мұғалім пікірі: {data.get('ai_feedback', 'Керемет!')}")
    else:
        st.write("Мұндай есім табылмады. Дұрыс жазылғанын тексеріңіз.")