# 🌱 Foras Khadra AI Suite Pro

مشروع ويب فخم ومتكامل لمهمة فريق الذكاء الاصطناعي في فرص خضراء.

## الفكرة

المشروع يبني ميزة AI مدمجة في تطبيق ويب تخدم منصة فرص خضراء.  
بدلاً من اختيار فكرة واحدة فقط، يجمع المشروع أربع ميزات ذكية:

1. بحث دلالي ذكي Semantic Search
2. مساعد ذكي AI Assistant
3. تلخيص وتصنيف تلقائي
4. توصيات ذكية Smart Recommendations

## التقنيات المستخدمة

- Python
- Streamlit
- Sentence Transformers
- Hugging Face
- NumPy
- Mock Data

## كيف يعمل البحث الدلالي؟

1. يحوّل النظام كل فرصة إلى متجه رقمي Embedding.
2. يحوّل سؤال المستخدم إلى Embedding أيضاً.
3. يقيس التشابه باستخدام Cosine Similarity.
4. يرتب الفرص حسب الأقرب في المعنى.

## تشغيل المشروع محلياً

```bash
pip install -r requirements.txt
streamlit run app.py
```

أول تشغيل قد يستغرق عدة دقائق لأن النموذج يتم تحميله من Hugging Face.

## هيكل المشروع

```text
foras_khadra_ai_suite_pro/
├── app.py
├── search_engine.py
├── data.py
├── requirements.txt
├── README.md
├── .gitignore
└── .streamlit/
    └── config.toml
```

## لماذا المشروع قوي للمهمة؟

- يدمج AI فعلياً باستخدام نموذج مفتوح المصدر.
- يحتوي على Frontend وBackend.
- يستخدم بيانات تجريبية مناسبة لسياق فرص خضراء.
- يغطي البحث الذكي والمساعد والتلخيص والتوصيات.
- يشرح سبب اقتراح كل فرصة.
- جاهز للرفع على GitHub والنشر على Streamlit Cloud.
