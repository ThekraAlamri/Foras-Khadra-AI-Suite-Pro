# -*- coding: utf-8 -*-
"""
AI backend logic for Foras Khadra AI Suite Pro.
"""

import re
import numpy as np
from sentence_transformers import SentenceTransformer
from data import OPPORTUNITIES

MODEL_NAME = "paraphrase-multilingual-MiniLM-L12-v2"


class SearchEngine:
    def __init__(self):
        self.opportunities = OPPORTUNITIES
        self.model = SentenceTransformer(MODEL_NAME)

        self.corpus = [self._build_text(opp) for opp in self.opportunities]
        self.corpus_embeddings = self.model.encode(
            self.corpus,
            normalize_embeddings=True,
            show_progress_bar=False
        )

    def _build_text(self, opp):
        tags = "، ".join(opp.get("tags", []))
        return (
            f"العنوان: {opp.get('title', '')}. "
            f"الوصف: {opp.get('description', '')}. "
            f"الدولة: {opp.get('country', '')}. "
            f"نوع الفرصة: {opp.get('type', '')}. "
            f"المستوى: {opp.get('level', '')}. "
            f"الموعد النهائي: {opp.get('deadline', '')}. "
            f"الكلمات المفتاحية: {tags}."
        )

    def search(self, query, top_k=5):
        if not query or not query.strip():
            return []

        query_embedding = self.model.encode(query, normalize_embeddings=True, show_progress_bar=False)
        scores = np.dot(self.corpus_embeddings, query_embedding)
        sorted_indices = np.argsort(scores)[::-1]

        results = []
        for idx in sorted_indices[:top_k]:
            opp = dict(self.opportunities[idx])
            score = float(scores[idx])
            opp["score"] = score
            opp["match_percent"] = max(0, min(100, int(score * 100)))
            opp["reason"] = self.explain_result(query, opp)
            results.append(opp)

        return results

    def explain_result(self, query, opp):
        tags = "، ".join(opp.get("tags", [])[:3])
        return (
            f"تم اقتراح هذه الفرصة لأنها قريبة دلالياً من طلبك «{query}». "
            f"الفرصة من نوع {opp.get('type', 'غير محدد')} في {opp.get('country', 'غير محدد')}، "
            f"وترتبط بوسوم مثل: {tags}."
        )

    def get_recommendations_for_opportunity(self, current_opp, limit=3):
        current_id = current_opp.get("id")
        current_type = current_opp.get("type")
        current_tags = set(current_opp.get("tags", []))

        scored = []
        for opp in self.opportunities:
            if opp.get("id") == current_id:
                continue

            score = 0
            if opp.get("type") == current_type:
                score += 2

            shared_tags = current_tags.intersection(set(opp.get("tags", [])))
            score += len(shared_tags)

            if score > 0:
                scored.append((score, opp))

        scored.sort(key=lambda x: x[0], reverse=True)
        return [item[1] for item in scored[:limit]]

    def recommend_by_profile(self, profile_text, top_k=5, country="الكل", opportunity_type="الكل"):
        results = self.search(profile_text, top_k=len(self.opportunities))

        if country != "الكل":
            results = [r for r in results if r.get("country") == country]

        if opportunity_type != "الكل":
            results = [r for r in results if r.get("type") == opportunity_type]

        for r in results:
            r["reason"] = (
                f"هذه التوصية مناسبة لأن ملف اهتماماتك يحتوي على: «{profile_text}»، "
                f"والفرصة مرتبطة بموضوعات قريبة مثل {', '.join(r.get('tags', [])[:3])}."
            )

        return results[:top_k]

    def answer_question(self, question, top_k=5):
        results = self.search(question, top_k=top_k)

        if not results:
            return "لم أجد فرصاً مرتبطة بسؤالك في البيانات التجريبية الحالية.", []

        countries = sorted(set([r["country"] for r in results]))
        types = sorted(set([r["type"] for r in results]))
        titles = "<br>".join([f"• {r['title']} — {r['country']} — {r['type']}" for r in results[:5]])

        answer = (
            "بناءً على سؤالك، وجدت لك فرصاً قريبة دلالياً من البيانات التجريبية المتاحة.<br><br>"
            f"<b>الدول المرتبطة:</b> {'، '.join(countries)}<br>"
            f"<b>أنواع الفرص:</b> {'، '.join(types)}<br><br>"
            f"<b>أقرب النتائج:</b><br>{titles}"
        )

        return answer, results

    def analyze_opportunity_text(self, text):
        clean_text = self._clean_text(text)
        summary = self._summarize(clean_text)
        category = self._classify(clean_text)
        tags = self._extract_tags(clean_text)
        confidence = self._estimate_confidence(clean_text, category, tags)

        return {
            "summary": summary,
            "category": category,
            "tags": tags,
            "confidence": confidence,
        }

    def _clean_text(self, text):
        return re.sub(r"\s+", " ", text).strip()

    def _summarize(self, text, max_words=28):
        words = text.split()
        if len(words) <= max_words:
            return text
        return " ".join(words[:max_words]) + "..."

    def _classify(self, text):
        text_lower = text.lower()

        category_keywords = {
            "منحة": ["منحة", "scholarship", "ممولة", "دراسة", "ماجستير", "بكالوريوس", "دكتوراه"],
            "تدريب": ["تدريب", "training", "ورشة", "مهارات", "دورة"],
            "وظيفة": ["وظيفة", "job", "عمل", "توظيف", "مهندس", "محلل", "أخصائي"],
            "تطوع": ["تطوع", "volunteer", "حملة", "مجتمعية"],
            "مسابقة": ["مسابقة", "competition", "جوائز", "ابتكار"],
            "زمالة": ["زمالة", "fellowship", "باحث", "بحث"],
            "برنامج تبادل": ["تبادل", "exchange", "ثقافي"],
            "برنامج قيادي": ["قيادة", "قادة", "leadership"],
        }

        best_category = "فرصة عامة"
        best_score = 0

        for category, keywords in category_keywords.items():
            score = sum(1 for kw in keywords if kw in text_lower)
            if score > best_score:
                best_score = score
                best_category = category

        return best_category

    def _extract_tags(self, text, limit=6):
        text_lower = text.lower()

        possible_tags = {
            "طاقة متجددة": ["طاقة متجددة", "renewable", "الطاقة النظيفة"],
            "طاقة شمسية": ["شمسية", "ألواح", "solar"],
            "طاقة رياح": ["رياح", "wind"],
            "تغير المناخ": ["مناخ", "climate", "كربون"],
            "استدامة": ["استدامة", "sustainability", "مستدام"],
            "إعادة تدوير": ["تدوير", "نفايات", "بلاستيك"],
            "مياه نظيفة": ["مياه", "water"],
            "زراعة مستدامة": ["زراعة", "عضوية", "agriculture"],
            "برمجة": ["برمجة", "ويب", "python", "بايثون"],
            "تحليل بيانات": ["بيانات", "تحليل", "data"],
            "تمويل أخضر": ["تمويل", "استثمار", "سندات"],
            "ريادة أعمال": ["ريادة", "مشاريع ناشئة", "startup"],
            "بحث علمي": ["بحث", "باحث", "research"],
            "قيادة": ["قيادة", "قادة", "leadership"],
        }

        tags = []
        for tag, keywords in possible_tags.items():
            if any(kw in text_lower for kw in keywords):
                tags.append(tag)

        if not tags:
            tags = ["فرص خضراء", "استدامة", "تطوير مهني"]

        return tags[:limit]

    def _estimate_confidence(self, text, category, tags):
        base = 55
        if category != "فرصة عامة":
            base += 20
        base += min(len(tags) * 4, 20)
        if len(text.split()) > 25:
            base += 5

        return max(50, min(98, base))
