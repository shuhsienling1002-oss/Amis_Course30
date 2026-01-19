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
st.set_page_config(page_title="Unit 30: O Maamaanan", page_icon="🌿", layout="centered")

# --- CSS 美化 (大地綠色調) ---
st.markdown("""
    <style>
    body { font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; }
    .source-tag { font-size: 12px; color: #aaa; text-align: right; font-style: italic; }
    
    /* 單字卡 */
    .word-card {
        background: linear-gradient(135deg, #DCEDC8 0%, #ffffff 100%);
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        text-align: center;
        margin-bottom: 15px;
        border-bottom: 4px solid #689F38;
    }
    .emoji-icon { font-size: 48px; margin-bottom: 10px; }
    .amis-text { font-size: 22px; font-weight: bold; color: #33691E; }
    .chinese-text { font-size: 16px; color: #7f8c8d; }
    
    /* 句子框 */
    .sentence-box {
        background-color: #F1F8E9;
        border-left: 5px solid #AED581;
        padding: 15px;
        margin: 10px 0;
        border-radius: 0 10px 10px 0;
    }

    /* 按鈕 */
    .stButton>button {
        width: 100%; border-radius: 12px; font-size: 20px; font-weight: 600;
        background-color: #DCEDC8; color: #33691E; border: 2px solid #689F38; padding: 12px;
    }
    .stButton>button:hover { background-color: #C5E1A5; border-color: #558B2F; }
    .stProgress > div > div > div > div { background-color: #689F38; }
    </style>
""", unsafe_allow_html=True)

# --- 2. 資料庫 (Unit 30: 14個單字 - 農牧自然篇) ---
vocab_data = [
    {"amis": "Tefos", "chi": "甘蔗", "icon": "🎋", "source": "Row 1261"},
    {"amis": "'Oway", "chi": "藤 / 黃藤", "icon": "🌿", "source": "Row 1175"},
    {"amis": "Kolong", "chi": "牛", "icon": "🐂", "source": "Row 490"},
    {"amis": "Ayam", "chi": "鳥", "icon": "🐦", "source": "Row 1029"},
    {"amis": "Konga", "chi": "地瓜 / 蕃薯", "icon": "🍠", "source": "Row 1717"},
    {"amis": "Dongec", "chi": "藤心", "icon": "🌱", "source": "Row 2181"},
    {"amis": "Icep", "chi": "檳榔", "icon": "🌰", "source": "Row 273"},
    {"amis": "Fonos", "chi": "刀 / 番刀", "icon": "🔪", "source": "Row 1146"},
    {"amis": "Kangkang", "chi": "鋤頭 / 犁", "icon": "⛏️", "source": "Row 1157"},
    {"amis": "Talod", "chi": "草 / 雜草", "icon": "🌾", "source": "Row 969"},
    {"amis": "Militolak", "chi": "削皮", "icon": "🔪", "source": "Row 1261"},
    {"amis": "Ma'engid", "chi": "被蛀 / 被咬", "icon": "🐛", "source": "Row 1028"},
    {"amis": "Lomengaw", "chi": "生長 / 發芽", "icon": "🌱", "source": "Row 969"},
    {"amis": "Pawli", "chi": "香蕉", "icon": "🍌", "source": "Row 4654"},
]

# --- 句子庫 (7句: 嚴格源自 CSV 並移除連字號) ---
sentences = [
    {"amis": "Militolak to tefos.", "chi": "削甘蔗皮。", "icon": "🎋", "source": "Row 1261"},
    {"amis": "O kalimelaan no maomahay ko kolong.", "chi": "牛是農民所珍惜的。", "icon": "🐂", "source": "Row 490"},
    {"amis": "Wata! Tata'ang koni a konga!", "chi": "哇！這塊地瓜很大！", "icon": "🍠", "source": "Row 1717"},
    {"amis": "Halo tapatapang no tefos a ma'engid.", "chi": "連甘蔗的根部都被蛀了。", "icon": "🐛", "source": "Row 1028"},
    {"amis": "Midongec kako i lotok.", "chi": "我在山上採藤心。", "icon": "⛰️", "source": "Row 2181"},
    {"amis": "Ci'orong ci wama to kangkang a minokay.", "chi": "父親扛著犁回家。", "icon": "⛏️", "source": "Row 1157"},
    {"amis": "Lomengawto ko talod i papotal.", "chi": "在屋外雜草生長了。", "icon": "🌾", "source": "Row 969"},
]

# --- 3. 隨機題庫 (Synced) ---
raw_quiz_pool = [
    {
        "q": "Militolak to tefos.",
        "audio": "Militolak to tefos",
        "options": ["削甘蔗皮", "吃甘蔗", "種甘蔗"],
        "ans": "削甘蔗皮",
        "hint": "Militolak (削皮), Tefos (甘蔗) (Row 1261)"
    },
    {
        "q": "Wata! Tata'ang koni a konga!",
        "audio": "Wata! Tata'ang koni a konga",
        "options": ["這塊地瓜很大", "這顆檳榔很大", "這把刀很大"],
        "ans": "這塊地瓜很大",
        "hint": "Konga (地瓜) (Row 1717)"
    },
    {
        "q": "單字測驗：Kolong",
        "audio": "Kolong",
        "options": ["牛", "羊", "豬"],
        "ans": "牛",
        "hint": "農夫珍惜的動物 (Row 490)"
    },
    {
        "q": "單字測驗：Dongec",
        "audio": "Dongec",
        "options": ["藤心", "竹筍", "地瓜"],
        "ans": "藤心",
        "hint": "山上採的 Dongec (Row 2181)"
    },
    {
        "q": "Lomengawto ko talod i papotal.",
        "audio": "Lomengawto ko talod i papotal",
        "options": ["雜草生長了", "花開了", "樹倒了"],
        "ans": "雜草生長了",
        "hint": "Talod (雜草), Lomengaw (生長) (Row 969)"
    },
    {
        "q": "單字測驗：Fonos",
        "audio": "Fonos",
        "options": ["刀/番刀", "槍", "弓箭"],
        "ans": "刀/番刀",
        "hint": "Row 1146: Cifonos... (帶刀)"
    },
    {
        "q": "單字測驗：Icep",
        "audio": "Icep",
        "options": ["檳榔", "香菸", "酒"],
        "ans": "檳榔",
        "hint": "Row 273: Mi'icep (嚼檳榔)"
    },
    {
        "q": "單字測驗：Ma'engid",
        "audio": "Ma'engid",
        "options": ["被蛀/咬", "被打", "被吃"],
        "ans": "被蛀/咬",
        "hint": "Row 1028: 甘蔗被 Ma'engid"
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
st.markdown("<h1 style='text-align: center; color: #33691E;'>Unit 30: O Maamaanan</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #666;'>各式各樣的事物 (Plants, Animals & Tools)</p>", unsafe_allow_html=True)

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
            <div style="font-size: 20px; font-weight: bold; color: #33691E;">{s['icon']} {s['amis']}</div>
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
        <div style='text-align: center; padding: 30px; background-color: #DCEDC8; border-radius: 20px; margin-top: 20px;'>
            <h1 style='color: #33691E;'>🏆 挑戰成功！</h1>
            <h3 style='color: #333;'>本次得分：{st.session_state.score}</h3>
            <p>你已經學會這些特殊的動植物詞彙了！</p>
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
