# -*- coding: utf-8 -*-
"""
Foras Khadra AI Suite Pro
Run:
    streamlit run app.py
"""

import streamlit as st
from search_engine import SearchEngine

st.set_page_config(
    page_title="Foras Khadra AI Suite Pro",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;500;700;800;900&display=swap');
html, body, [class*="css"] {
    font-family: 'Tajawal', sans-serif;
    direction: rtl;
    text-align: right;
}
.main {
    background:
        radial-gradient(circle at top right, rgba(16,185,129,0.18), transparent 32%),
        radial-gradient(circle at bottom left, rgba(245,158,11,0.12), transparent 34%),
        linear-gradient(135deg, #f8fffb 0%, #ecfdf5 55%, #fffdf5 100%);
}
.block-container { padding-top: 2rem; padding-bottom: 3rem; }
.hero {
    background: linear-gradient(135deg, #065f46, #10b981);
    padding: 42px;
    border-radius: 32px;
    color: white;
    box-shadow: 0 24px 60px rgba(6,95,70,0.28);
    margin-bottom: 28px;
    border: 1px solid rgba(255,255,255,0.28);
}
.hero h1 { font-size: 46px; font-weight: 900; margin-bottom: 12px; }
.hero p { font-size: 20px; line-height: 1.9; max-width: 920px; }
.glass-card {
    background: rgba(255,255,255,0.82);
    border: 1px solid rgba(16,185,129,0.22);
    border-radius: 26px;
    padding: 24px;
    box-shadow: 0 16px 38px rgba(15,23,42,0.08);
    margin-bottom: 18px;
}
.result-card {
    background: linear-gradient(180deg, #ffffff, #fbfffd);
    padding: 26px;
    border-radius: 28px;
    border: 1px solid #d1fae5;
    box-shadow: 0 18px 46px rgba(15,23,42,0.08);
    margin-bottom: 18px;
}
.badge {
    display: inline-block;
    padding: 7px 15px;
    border-radius: 999px;
    font-size: 14px;
    margin-left: 7px;
    margin-bottom: 9px;
    font-weight: 800;
}
.type-badge { background: #d1fae5; color: #065f46; }
.country-badge { background: #e0f2fe; color: #075985; }
.level-badge { background: #fef3c7; color: #92400e; }
.deadline-badge { background: #fce7f3; color: #9d174d; }
.ai-note {
    background: linear-gradient(135deg, #ecfdf5, #f0fdfa);
    border-right: 5px solid #10b981;
    padding: 16px 18px;
    border-radius: 18px;
    margin-top: 12px;
    color: #064e3b;
    font-weight: 600;
}
.footer { text-align: center; color: #64748b; margin-top: 42px; font-size: 14px; }
.stTextInput input, .stTextArea textarea { text-align: right; border-radius: 18px !important; }
.stButton button {
    border-radius: 18px;
    font-weight: 900;
    background: linear-gradient(135deg, #047857, #10b981);
    color: white;
    border: none;
}
</style>
""", unsafe_allow_html=True)


@st.cache_resource(show_spinner="🌱 جارٍ تحميل نموذج الذكاء الاصطناعي لأول مرة...")
def load_engine():
    return SearchEngine()


engine = load_engine()

if "query" not in st.session_state:
    st.session_state.query = ""


def render_header():
    st.markdown("""
    <div class="hero">
        <h1>🌱 Foras Khadra AI Suite Pro</h1>
        <p>
        منصة ذكاء اصطناعي مصغّرة تخدم فرص خضراء عبر البحث الدلالي، المساعد الذكي،
        التلخيص والتصنيف التلقائي، والتوصيات الذكية للشباب.
        </p>
    </div>
    """, unsafe_allow_html=True)


def render_opportunity_card(opp, show_reason=True):
    tags = opp.get("tags", [])
    tags_html = " ".join([f"<span class='badge type-badge'>#{tag}</span>" for tag in tags[:5]])

    st.markdown(f"""
    <div class="result-card">
        <h3>{opp.get('title', 'بدون عنوان')}</h3>
        <span class="badge type-badge">🏷️ {opp.get('type', 'غير محدد')}</span>
        <span class="badge country-badge">📍 {opp.get('country', 'غير محدد')}</span>
        <span class="badge level-badge">🎓 {opp.get('level', 'غير محدد')}</span>
        <span class="badge deadline-badge">⏳ {opp.get('deadline', 'مفتوح')}</span>
        <p>{opp.get('description', '')}</p>
        <div>{tags_html}</div>
    </div>
    """, unsafe_allow_html=True)

    match = int(opp.get("match_percent", 0))
    if match:
        st.progress(match / 100)
        st.caption(f"نسبة التطابق الدلالي: {match}%")

    if show_reason and opp.get("reason"):
        st.markdown(f"<div class='ai-note'>🧠 {opp.get('reason')}</div>", unsafe_allow_html=True)

    st.markdown(f"[🔗 فتح رابط الفرصة]({opp.get('url', '#')})")


with st.sidebar:
    st.markdown("## 🌱 فرص خضراء AI")
    page = st.radio(
        "القائمة",
        [
            "🏠 الرئيسية",
            "🔍 البحث الدلالي",
            "🤖 المساعد الذكي",
            "📝 تلخيص وتصنيف فرصة",
            "🎯 توصيات ذكية",
            "ℹ️ عن المشروع",
        ],
    )
    st.divider()
    top_k = st.slider("عدد النتائج", 1, 12, 6)
    st.caption("AI Model: paraphrase-multilingual-MiniLM-L12-v2")


countries = ["الكل"] + sorted(list(set([o["country"] for o in engine.opportunities])))
types = ["الكل"] + sorted(list(set([o["type"] for o in engine.opportunities])))
levels = ["الكل"] + sorted(list(set([o.get("level", "غير محدد") for o in engine.opportunities])))


if page == "🏠 الرئيسية":
    render_header()
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("إجمالي الفرص", len(engine.opportunities))
    c2.metric("أنواع الفرص", len(types) - 1)
    c3.metric("الدول", len(countries) - 1)
    c4.metric("ميزات AI", "4")

    st.markdown("### ✨ ماذا يقدّم المشروع؟")
    st.markdown("""
    <div class="glass-card">
    <b>هذا المشروع يجمع كل الأفكار المهمة في المهمة:</b><br>
    بحث دلالي، مساعد ذكي، تصنيف/تلخيص تلقائي، وتوصيات ذكية.
    </div>
    """, unsafe_allow_html=True)

    f1, f2 = st.columns(2)
    with f1:
        st.markdown("#### 🔍 بحث دلالي")
        st.write("يفهم المعنى ويقارن استفسار المستخدم مع الفرص باستخدام Embeddings وCosine Similarity.")
        st.markdown("#### 🤖 مساعد ذكي")
        st.write("يرد على أسئلة المستخدمين حول الفرص المتاحة بناءً على بيانات تجريبية.")
    with f2:
        st.markdown("#### 📝 تلخيص وتصنيف")
        st.write("يستقبل وصف فرصة طويل ويقترح ملخصاً وتصنيفاً ووسوماً مناسبة.")
        st.markdown("#### 🎯 توصيات")
        st.write("يقترح فرصاً تناسب اهتمامات المستخدم أو الفرص التي شاهدها.")


elif page == "🔍 البحث الدلالي":
    render_header()
    st.markdown("## 🔍 البحث الدلالي الذكي")

    examples = [
        "أريد منحة لدراسة الطاقة المتجددة في أوروبا",
        "فرص تطوع في البيئة وإعادة التدوير",
        "تدريب عن بعد في البرمجة وتحليل البيانات",
        "وظائف في الاستدامة والتقارير البيئية",
    ]

    e1, e2 = st.columns(2)
    for i, ex in enumerate(examples):
        with e1 if i % 2 == 0 else e2:
            if st.button(ex, key=f"ex_{i}"):
                st.session_state.query = ex

    query = st.text_input(
        "اكتبي طلبك بلغة طبيعية:",
        value=st.session_state.query,
        placeholder="مثال: أبحث عن فرصة تدريب في الطاقة الشمسية..."
    )

    f1, f2, f3 = st.columns(3)
    with f1:
        selected_country = st.selectbox("🌍 الدولة", countries)
    with f2:
        selected_type = st.selectbox("📂 نوع الفرصة", types)
    with f3:
        selected_level = st.selectbox("🎓 المستوى", levels)

    if st.button("بحث ذكي 🚀"):
        if not query.strip():
            st.warning("اكتبي جملة البحث أولاً.")
        else:
            with st.spinner("جارٍ تحويل النصوص إلى Embeddings وحساب التشابه الدلالي..."):
                results = engine.search(query, top_k=top_k)

            if selected_country != "الكل":
                results = [r for r in results if r["country"] == selected_country]
            if selected_type != "الكل":
                results = [r for r in results if r["type"] == selected_type]
            if selected_level != "الكل":
                results = [r for r in results if r.get("level", "غير محدد") == selected_level]

            if not results:
                st.error("لا توجد نتائج بعد تطبيق الفلاتر. جرّبي تقليل الفلاتر أو تغيير كلمات البحث.")
            else:
                st.success(f"تم العثور على {len(results)} نتيجة مناسبة.")
                for opp in results:
                    render_opportunity_card(opp)
                    with st.expander("🎯 فرص مشابهة لهذه الفرصة"):
                        recs = engine.get_recommendations_for_opportunity(opp, limit=3)
                        if recs:
                            for rec in recs:
                                st.write(f"• {rec['title']} — {rec['country']} — {rec['type']}")
                        else:
                            st.write("لا توجد توصيات مشابهة حالياً.")
                    st.divider()


elif page == "🤖 المساعد الذكي":
    render_header()
    st.markdown("## 🤖 مساعد فرص خضراء الذكي")

    question = st.text_input("اسألي المساعد عن الفرص:", placeholder="مثال: ما الفرص المتاحة للطلاب في مصر؟")

    if st.button("اسأل المساعد 💬"):
        if not question.strip():
            st.warning("اكتبي سؤالاً أولاً.")
        else:
            answer, related = engine.answer_question(question, top_k=5)
            st.markdown(f"<div class='glass-card'>{answer}</div>", unsafe_allow_html=True)
            if related:
                st.markdown("### فرص مرتبطة بسؤالك")
                for opp in related[:3]:
                    render_opportunity_card(opp, show_reason=False)
                    st.divider()


elif page == "📝 تلخيص وتصنيف فرصة":
    render_header()
    st.markdown("## 📝 تلخيص وتصنيف تلقائي للفرص")

    sample_text = (
        "برنامج دولي ممول جزئياً يهدف إلى تدريب الشباب على حلول الطاقة النظيفة "
        "والاستدامة وإدارة المشاريع البيئية، ويشمل ورش عمل وشهادة مشاركة."
    )

    opportunity_text = st.text_area("الصقي وصف فرصة طويل:", value=sample_text, height=190)

    if st.button("حلّل النص بالذكاء الاصطناعي 🧠"):
        if not opportunity_text.strip():
            st.warning("أدخلي وصف الفرصة أولاً.")
        else:
            analysis = engine.analyze_opportunity_text(opportunity_text)
            a1, a2 = st.columns(2)
            with a1:
                st.markdown("### الملخص")
                st.success(analysis["summary"])
                st.markdown("### التصنيف المقترح")
                st.info(analysis["category"])
            with a2:
                st.markdown("### الوسوم المقترحة")
                for tag in analysis["tags"]:
                    st.markdown(f"- #{tag}")
                st.markdown("### درجة الثقة")
                st.progress(analysis["confidence"] / 100)
                st.caption(f"{analysis['confidence']}%")


elif page == "🎯 توصيات ذكية":
    render_header()
    st.markdown("## 🎯 توصيات ذكية حسب الاهتمامات")

    interests = st.multiselect(
        "اختاري اهتماماتك:",
        [
            "طاقة متجددة", "استدامة", "تغير المناخ", "تطوع", "برمجة",
            "تحليل بيانات", "تمويل أخضر", "زراعة مستدامة", "مياه نظيفة", "ريادة أعمال"
        ],
        default=["طاقة متجددة", "استدامة"]
    )

    country_pref = st.selectbox("الدولة المفضلة", countries)
    type_pref = st.selectbox("نوع الفرصة المفضل", types)

    if st.button("اعرض التوصيات ✨"):
        profile_text = " ".join(interests)
        if country_pref != "الكل":
            profile_text += f" {country_pref}"
        if type_pref != "الكل":
            profile_text += f" {type_pref}"

        recs = engine.recommend_by_profile(profile_text, top_k=top_k, country=country_pref, opportunity_type=type_pref)

        if not recs:
            st.error("لا توجد توصيات مطابقة، جرّبي تغيير الاختيارات.")
        else:
            st.success("هذه فرص مناسبة لاهتماماتك:")
            for opp in recs:
                render_opportunity_card(opp)
                st.divider()


elif page == "ℹ️ عن المشروع":
    render_header()
    st.markdown("## ℹ️ عن المشروع والتقنيات")

    st.markdown("""
    <div class="glass-card">
    <b>الفكرة:</b> بناء ميزة AI مدمجة في تطبيق ويب تخدم منصة فرص خضراء.
    المشروع يستخدم نموذجاً مفتوح المصدر من Hugging Face لتحويل النصوص إلى Embeddings
    ثم يقارنها باستخدام Cosine Similarity.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### 🧠 الميزات الذكية")
    st.write("1. بحث دلالي يفهم المعنى وليس فقط الكلمات.")
    st.write("2. مساعد ذكي يجيب عن أسئلة المستخدمين من بيانات الفرص.")
    st.write("3. تلخيص وتصنيف تلقائي لوصف الفرص مع وسوم مناسبة.")
    st.write("4. توصيات ذكية بناءً على الاهتمامات والفلاتر.")

    st.markdown("### 🛠️ التقنيات")
    st.code("Python\nStreamlit\nSentence Transformers\nHugging Face\nNumPy\nMock Data", language="text")



st.markdown("""
<div class="footer">
© 2026 Foras Khadra AI Suite Pro — Built with Streamlit & Open-Source AI 🌱
</div>
""", unsafe_allow_html=True)
