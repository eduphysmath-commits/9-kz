import streamlit as st
import requests
import streamlit.components.v1 as components
import json

# --- БАПТАУЛАР ---
URL = "https://iuqdbdvmbewaedgydaah.supabase.co"
KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Iml1cWRiZHZtYmV3YWVkZ3lkYWFoIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjkzMjE5ODgsImV4cCI6MjA4NDg5Nzk4OH0.a_PPVZWcA3qOfT4cNaXNE_a3xuSv0CHyrY8LbTgjWww"

st.set_page_config(page_title="СОЧ по Физике 9 класс", layout="wide", page_icon="🪐")

if 'submitted' not in st.session_state:
    st.session_state.submitted = False

# --- 1. КӨШІРУДЕН ҚОРҒАУ (CSS) ---
st.markdown("""
    <style>
    * { -webkit-user-select: none; user-select: none; } 
    .stRadio > div { background-color: white; padding: 15px; border-radius: 10px; border: 1px solid #e0e0e0; margin-bottom: 10px; }
    /* Басты беттің фонын аздап өзгерту */
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
    return requests.post(f"{URL}/rest/v1/tjb_9_rus", json=data, headers=headers)

# --- 2. ИНТЕРФЕЙС ЖӘНЕ ДЕРЕКТЕРДІ ЕНГІЗУ ---
st.title("🪐 ФИЗИКА, 9 КЛАСС. СОЧ ЗА 1-Е ПОЛУГОДИЕ")

if not st.session_state.submitted:
    st.info("⏱ Время: 45 минут | Максимальный балл: 25 баллов")
    
    # --- ОҚУШЫ МӘЛІМЕТТЕРІ (Енді басты бетте) ---
    st.subheader("👤 Данные ученика")
    col1, col2 = st.columns(2)
    with col1:
        student_name = st.text_input("Введите Имя и Фамилия:", placeholder="Напр: Иван Иванов")
    with col2:
        student_class = st.selectbox("Выберите Класс:", ["9 А (рус)", "9 Б (рус)", "9 В (рус)"])
    
    if not student_name:
        st.warning("☝️ Пожалуйста, введите имя, чтобы начать тест.")
    else:
        st.success(f"Привет, {student_name}! Можешь приступать к заданиям.")
        st.warning("⚠️ Внимание: Выход из вкладки более чем на 5 секунд аннулирует работу!")

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
                speak("Внимание! Немедленно вернись к тесту! У тебя осталось 5 секунд!");
                alert("ВНИМАНИЕ! Вы покинули вкладку. Через 5 секунд работа будет аннулирована!");
                
                timeout = setTimeout(function() {{
                    fetch('{URL}/rest/v1/tjb_9_rus', {{
                        method: 'POST',
                        headers: {{ 'apikey': '{KEY}', 'Authorization': 'Bearer {KEY}', 'Content-Type': 'application/json' }},
                        body: JSON.stringify({{
                            student_name: '{student_name}',
                            student_class: '{student_class}',
                            status: 'cheated',
                            ai_feedback: 'Работа АННУЛИРОВАНА: зафиксирован выход из вкладки.'
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
        # РАЗДЕЛ А
        st.subheader("📍 РАЗДЕЛ А: Тестовые задания (10 баллов)")
        q1 = st.radio("1. Материальная точка, двигаясь по окружности, вернулась в исходную точку. Какими будут перемещение (S) и пройденный путь (l)?", 
                      ["A) S = 2πR; l = 0", "B) S = 0; l = 2πR", "C) S = 0; l = 0", "D) S = 2πR; l = 2πR"], index=None)
        q2 = st.radio("2. Тело в течение 5 секунд равномерно увеличило свою скорость от 0 до 10 м/с. Определите ускорение тела.", 
                      ["A) 5 м/с²", "B) 2 м/с²", "C) 10 м/с²", "D) 0 м/с²"], index=None)
        q3 = st.radio("3. Как называются постоянные группы звезд на небесной сфере, сохраняющие взаимное расположение?", 
                      ["A) Галактики", "B) Планеты", "C) Созвездия", "D) Туманности"], index=None)
        q4 = st.radio("4. Какую систему мы называем инерциальной системой отсчета?", 
                      ["A) Систему, в которой тело движется с ускорением", "B) Систему, в которой тело находится в покое или движется прямолинейно и равномерно", "C) Систему, в которой тело движется по окружности", "D) Любую систему отсчета"], index=None)
        q5 = st.radio("5. Формула силы тяжести, действующей на тела у поверхности Земли:", 
                      ["A) F = kx", "B) F = μN", "C) F = mg", "D) F = ma"], index=None)
        q6 = st.radio("6. Согласно третьему закону Ньютона, силы:", 
                      ["A) Приложены к разным телам, направлены противоположно, равны по модулю", "B) Приложены к одному телу, уравновешивают друг друга", "C) Направлены в одну сторону, различны по модулю", "D) Действуют только на тела, находящиеся в покое"], index=None)
        q7 = st.radio("7. Если расстояние между двумя телами увеличить в 2 раза, как изменится сила притяжения?", 
                      ["A) Увеличится в 2 раза", "B) Уменьшится в 2 раза", "C) Увеличится в 4 раза", "D) Уменьшится в 4 раза"], index=None)
        q8 = st.radio("8. По какой траектории движутся планеты вокруг Солнца согласно 1-му закону Кеплера?", 
                      ["A) По окружности", "B) По эллипсу", "C) По параболе", "D) По прямой линии"], index=None)
        q9 = st.radio("9. Формула центростремительного ускорения:", 
                      ["A) a = v / t", "B) a = v² / R", "C) a = ωR", "D) a = 4π²R"], index=None)
        q10 = st.radio("10. Каким будет вес пассажира в лифте, если он падает вниз с ускорением a = g = 10 м/с²?", 
                      ["A) P = mg", "B) P = 2mg", "C) P = 0 (Невесомость)", "D) P = m(g - a)"], index=None)

        # РАЗДЕЛ В
        st.subheader("📍 РАЗДЕЛ В: Задания с кратким ответом (12 баллов)")
        st.markdown("**Задание 11. Явление инерции**")
        q11a = st.text_input("а) Как называется явление наклона пассажиров вперед при резкой остановке автобуса?")
        q11b = st.text_input("b) Приведите еще один пример этого явления из жизни:")
        st.markdown("**Задание 12. Задача по динамике (m = 2 кг, F = 8 Н)**")
        q12a = st.text_area("а) Вычислите ускорение тела (формула и расчет):")
        q12b = st.text_area("b) Если силу увеличить в 2 раза, как изменится его ускорение? (Объясните):")
        st.markdown("**Задание 13. Астрономия**")
        q13a = st.text_input("а) В чем заключается главное различие между звездой и планетой?")
        q13b = st.text_input("b) Назовите самую большую планету в Солнечной системе:")

        # РАЗДЕЛ С
        st.subheader("📍 РАЗДЕЛ С: Структурированное задание (3 балла)")
        q14a = st.text_input("a) Определите время падения мяча на землю (t) при h=20м:")
        q14b = st.text_input("b) На каком расстоянии (L) упадет мяч при v0=10м/с:")
        q14c = st.text_input("c) Какую форму имеет траектория мяча?")

        submit = st.form_submit_button("Завершить и отправить работу ✅")

    if submit:
        if 'student_name' not in locals() or not student_name:
            st.error("❌ Пожалуйста, введите Ваше имя в начале страницы!")
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
                st.rerun()

# --- 5. НӘТИЖЕНІ ІЗДЕУ ---
st.markdown("---")
st.subheader("🔎 Проверить результат")
search_name = st.text_input("Введите имя для поиска результата:")
if search_name:
    search_headers = {"apikey": KEY, "Authorization": f"Bearer {KEY}"}
    res = requests.get(f"{URL}/rest/v1/tjb_9_rus?student_name=eq.{search_name}&select=*&order=id.desc", headers=search_headers)
    if res.status_code == 200 and res.json():
        result = res.json()[0]
        if result['status'] == 'cheated':
            st.error(f"🚫 Работа аннулирована. Причина: {result['ai_feedback']}")
        elif result['status'] == 'pending':
            st.warning("⏳ Работа еще проверяется ЖИ...")
        else:
            st.metric("Балл:", f"{result.get('score', 0)} / 25")
            st.info(f"Комментарий ЖИ: {result['ai_feedback']}")
    else:
        st.info("Работа не найдена.")