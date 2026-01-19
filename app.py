import streamlit as st
import time
import random
from io import BytesIO

# --- 1. 核心相容性修復 ---
def safe_rerun():
    """自動判斷並執行重整"""
    try:
        st.rerun()
    except AttributeError:
        try:
            st.experimental_rerun()
        except:
            st.stop()

def safe_play_audio(text):
    """語音播放安全模式"""
    try:
        from gtts import gTTS
        # 使用印尼語 (id) 發音
        tts = gTTS(text=text, lang='id')
        fp = BytesIO()
        tts.write_to_fp(fp)
        st.audio(fp, format='audio/mp3')
    except Exception as e:
        st.caption(f"🔇 (語音生成暫時無法使用)")

# --- 0. 系統配置 ---
st.set_page_config(page_title="Unit 30: O Masamaamaanay", page_icon="🧩", layout="centered")

# --- CSS 美化 (多樣色彩) ---
st.markdown("""
    <style>
    body { font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; }
    .source-tag { font-size: 12px; color: #aaa; text-align: right; font-style: italic; }
    
    /* 單字卡 */
    .word-card {
        background: linear-gradient(135deg, #F5F5F5 0%, #ffffff 100%);
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        text-align: center;
        margin-bottom: 15px;
        border-bottom: 4px solid #9E9E9E;
    }
    .emoji-icon { font-size: 48px; margin-bottom: 10px; }
    .amis-text { font-size: 22px; font-weight: bold; color: #616161; }
    .chinese-text { font-size: 16px; color: #7f8c8d; }
    
    /* 句子框 */
    .sentence-box {
        background-color: #EEEEEE;
        border-left: 5px solid #BDBDBD;
        padding: 15px;
        margin: 10px 0;
        border-radius: 0 10px 10px 0;
    }

    /* 按鈕 */
    .stButton>button {
        width: 100%; border-radius: 12px; font-size: 20px; font-weight: 600;
        background-color: #E0E0E0; color: #424242; border: 2px solid #9E9E9E; padding: 12px;
    }
    .stButton>button:hover { background-color: #BDBDBD; border-color: #757575; }
    .stProgress > div > div > div > div { background-color: #9E9E9E; }
    </style>
""", unsafe_allow_html=True)

# --- 2. 資料庫 (Unit 30: 14個單字 - 句子提取核心詞) ---
vocab_data = [
    {"amis": "Singsi", "chi": "老師", "icon": "👩‍🏫", "source": "Row 9"},
    {"amis": "Ising", "chi": "醫生 / 醫治", "icon": "👨‍⚕️", "source": "Row 272"},
    {"amis": "Niyaro'", "chi": "部落", "icon": "🏡", "source": "Row 15"},
    {"amis": "Safa", "chi": "弟妹 / 年幼者", "icon": "👶", "source": "Row 268"},
    {"amis": "^Ekim", "chi": "黃金", "icon": "🪙", "source": "Row 564"},
    {"amis": "Tomay", "chi": "熊", "icon": "🐻", "source": "Row 1290"},
    {"amis": "Malicay", "chi": "被問 / 詢問", "icon": "❓", "source": "Row 209"},
    {"amis": "Cima", "chi": "誰", "icon": "👤", "source": "Row 9"},
    {"amis": "Maan", "chi": "什麼", "icon": "🤔", "source": "Row 13"},
    {"amis": "Talacowa", "chi": "去哪裡", "icon": "🗺️", "source": "Row 7"},
    {"amis": "Fali", "chi": "風", "icon": "💨", "source": "Row 555"},
    {"amis": "Ngangan", "chi": "名字", "icon": "🏷️", "source": "Row 9"},
    {"amis": "Posong", "chi": "台東", "icon": "📍", "source": "Row 19"},
    {"amis": "Matoka", "chi": "懶惰", "icon": "😴", "source": "Row 404"},
]

# --- 句子庫 (7句: 嚴格源自 CSV 並移除連字號) ---
sentences = [
    {"amis": "O singsi kora a kaying.", "chi": "那位小姐是老師。", "icon": "👩‍🏫", "source": "Row 9"},
    {"amis": "Cima ko ngangan ni ina?", "chi": "媽媽的名字是誰(什麼)？", "icon": "🏷️", "source": "Row 9"},
    {"amis": "Talacowa ko widang no miso?", "chi": "你的朋友去哪裡？", "icon": "🗺️", "source": "Row 7"},
    {"amis": "I cowa ko niyaro' no kapah?", "chi": "年輕人的部落在哪裡？", "icon": "🏡", "source": "Row 15"},
    {"amis": "O tada^ekim ko micakayan no miso.", "chi": "你買的是純金。", "icon": "🪙", "source": "Row 564"},
    {"amis": "Malicay ni ina no miso ko widang no mako.", "chi": "我的朋友被妳的媽媽詢問。", "icon": "❓", "source": "Row 209"},
    {"amis": "Matoka ko safa no miso.", "chi": "你的弟弟(妹妹)很懶惰。", "icon": "😴", "source": "Row 404"},
]

# --- 3. 隨機題庫 (Synced) ---
raw_quiz_pool = [
    {
        "q": "Talacowa ko widang no miso?",
        "audio": "Talacowa ko widang no miso",
        "options": ["你的朋友去哪裡？", "你的朋友在哪裡？", "你的朋友是誰？"],
        "ans": "你的朋友去哪裡？",
        "hint": "Talacowa (去哪裡) (Row 7)"
    },
    {
        "q": "Matoka ko safa no miso.",
        "audio": "Matoka ko safa no miso",
        "options": ["你的弟妹很懶惰", "你的弟妹很勤勞", "你的弟妹很聰明"],
        "ans": "你的弟妹很懶惰",
        "hint": "Matoka (懶惰) (Row 404)"
    },
    {
        "q": "單字測驗：^Ekim",
        "audio": "^Ekim",
        "options": ["黃金", "錢", "鐵"],
        "ans": "黃金",
        "hint": "Row 564: O tada^ekim (純金)"
    },
    {
        "q": "單字測驗：Cima",
        "audio": "Cima",
        "options": ["誰", "什麼", "哪裡"],
        "ans": "誰",
        "hint": "Cima ko ngangan? (名字是誰?) (Row 9)"
    },
    {
        "q": "I cowa ko niyaro' no kapah?",
        "audio": "I cowa ko niyaro' no kapah",
        "options": ["年輕人的部落在哪裡？", "年輕人的家在哪裡？", "年輕人的學校在哪裡？"],
        "ans": "年輕人的部落在哪裡？",
        "hint": "Niyaro' (部落) (Row 15)"
    },
    {
        "q": "單字測驗：Ising",
        "audio": "Ising",
        "options": ["醫生/醫治", "老師", "警察"],
        "ans": "醫生/醫治",
        "hint": "生病要找 Ising (Row 272)"
    },
    {
        "q": "單字測驗：Tomay",
        "audio": "Tomay",
        "options": ["熊", "豬", "羊"],
        "ans": "熊",
        "hint": "山上的動物 (Row 1290)"
    },
    {
        "q": "單字測驗：Singsi",
        "audio": "Singsi",
        "options": ["老師", "學生", "校長"],
        "ans": "老師",
        "hint": "在學校教書的人 (Row 9)"
    }
]

# --- 4. 狀態初始化 (洗牌邏輯) ---
if 'init' not in st.session_state:
    st.session_state.score = 0
    st.session_state.current_q_idx = 0
    st.session_state.quiz_id = str(random.randint(1000, 9999))
    
    # 抽題與洗牌
    selected_questions = random.sample(raw_quiz_pool, 3)
    final_questions = []
    for q in selected_questions:
        q_copy = q.copy()
        shuffled_opts = random.sample(q['options'], len(q['options']))
        q_copy['shuffled_options'] = shuffled_opts
        final_questions.append(q_copy)
        
    st.session_state.quiz_questions = final_questions
    st.session_state.init = True

# --- 5. 主介面 ---
st.markdown("<h1 style='text-align: center; color: #616161;'>Unit 30: O Masamaamaanay</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #666;'>各式各樣的事物 (Diverse Topics)</p>", unsafe_allow_html=True)

tab1, tab2 = st.tabs(["📚 詞彙與句型", "🎲 隨機挑戰"])

# === Tab 1: 學習模式 ===
with tab1:
    st.subheader("📝 核心單字 (從句子提取)")
    col1, col2 = st.columns(2)
    for i, word in enumerate(vocab_data):
        with (col1 if i % 2 == 0 else col2):
            st.markdown(f"""
            <div class="word-card">
                <div class="emoji-icon">{word['icon']}</div>
                <div class="amis-text">{word['amis']}</div>
                <div class="chinese-text">{word['chi']}</div>
                <div class="source-tag">src: {word['source']}</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"🔊 聽發音", key=f"btn_vocab_{i}"):
                safe_play_audio(word['amis'])

    st.markdown("---")
    st.subheader("🗣️ 實用句型 (Data-Driven)")
    for i, s in enumerate(sentences):
        st.markdown(f"""
        <div class="sentence-box">
            <div style="font-size: 20px; font-weight: bold; color: #616161;">{s['icon']} {s['amis']}</div>
            <div style="font-size: 16px; color: #555; margin-top: 5px;">{s['chi']}</div>
            <div class="source-tag">src: {s['source']}</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button(f"▶️ 播放句型", key=f"btn_sent_{i}"):
            safe_play_audio(s['amis'])

# === Tab 2: 隨機挑戰模式 ===
with tab2:
    st.markdown("### 🎲 隨機評量")
    
    if st.session_state.current_q_idx < len(st.session_state.quiz_questions):
        q_data = st.session_state.quiz_questions[st.session_state.current_q_idx]
        
        st.progress((st.session_state.current_q_idx) / 3)
        st.markdown(f"**Question {st.session_state.current_q_idx + 1} / 3**")
        
        st.markdown(f"### {q_data['q']}")
        if q_data['audio']:
            if st.button("🎧 播放題目音檔", key=f"btn_audio_{st.session_state.current_q_idx}"):
                safe_play_audio(q_data['audio'])
        
        # 使用洗牌後的選項
        unique_key = f"q_{st.session_state.quiz_id}_{st.session_state.current_q_idx}"
        user_choice = st.radio("請選擇正確答案：", q_data['shuffled_options'], key=unique_key)
        
        if st.button("送出答案", key=f"btn_submit_{st.session_state.current_q_idx}"):
            if user_choice == q_data['ans']:
                st.balloons()
                st.success("🎉 答對了！")
                time.sleep(1)
                st.session_state.score += 100
                st.session_state.current_q_idx += 1
                safe_rerun()
            else:
                st.error(f"不對喔！提示：{q_data['hint']}")
                
    else:
        st.progress(1.0)
        st.markdown(f"""
        <div style='text-align: center; padding: 30px; background-color: #E0E0E0; border-radius: 20px; margin-top: 20px;'>
            <h1 style='color: #616161;'>🏆 挑戰成功！</h1>
            <h3 style='color: #333;'>本次得分：{st.session_state.score}</h3>
            <p>你已經學會各式各樣的詞彙了！</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🔄 再來一局 (重新抽題)", key="btn_restart"):
            st.session_state.score = 0
            st.session_state.current_q_idx = 0
            st.session_state.quiz_id = str(random.randint(1000, 9999))
            
            new_questions = random.sample(raw_quiz_pool, 3)
            final_qs = []
            for q in new_questions:
                q_copy = q.copy()
                shuffled_opts = random.sample(q['options'], len(q['options']))
                q_copy['shuffled_options'] = shuffled_opts
                final_qs.append(q_copy)
            
            st.session_state.quiz_questions = final_qs
            safe_rerun()
