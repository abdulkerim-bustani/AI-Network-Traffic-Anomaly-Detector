
from pathlib import Path

import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

from src.analyzer import REQUIRED_COLUMNS, LABEL_COLUMN, analyze_data
from src.generate_data import generate_dataset


ROOT = Path(__file__).resolve().parent
DEFAULT_DATA = ROOT / "data" / "network_traffic.csv"

LANGUAGES = {
    "العربية": "ar",
    "Türkçe": "tr",
    "English": "en",
}

TEXT = {
    "ar": {
        "page_title": "محلّل حركة الشبكة الذكي",
        "caption": "مشروع تعليمي لاكتشاف الأنماط غير المعتادة في حركة الشبكة باستخدام تعلم الآلة.",
        "language": "🌐 اللغة",
        "settings": "إعدادات التحليل",
        "contamination": "نسبة الشذوذ المقدّرة",
        "contamination_help": "النسبة المقدّرة للسجلات غير المعتادة، وليست احتمالًا لكون الاتصال خبيثًا.",
        "security_notice": "النتائج مؤشرات للمراجعة وليست حكمًا أمنيًا نهائيًا. استخدم بيانات مصرحًا لك بتحليلها.",
        "source": "1. مصدر البيانات",
        "upload": "ارفع ملف CSV لتحليله (اختياري)",
        "regenerate": "استخدم / أعد إنشاء البيانات التجريبية",
        "read_error": "تعذرت قراءة البيانات",
        "missing_columns": "الملف لا يحتوي على الأعمدة المطلوبة",
        "preview": "معاينة البيانات الأصلية",
        "analyze": "🔍 تحليل السجلات",
        "training": "تقسيم البيانات وتدريب نموذج اكتشاف الشذوذ...",
        "analysis_error": "حدث خطأ أثناء التحليل",
        "summary": "2. ملخص النتائج",
        "total": "إجمالي السجلات",
        "anomalies": "سجلات غير معتادة",
        "normal": "سجلات طبيعية",
        "distribution": "توزيع التصنيف",
        "by_protocol": "عدد السجلات حسب البروتوكول",
        "normal_chart": "طبيعي",
        "unusual_chart": "غير معتاد",
        "record_count": "عدد السجلات",
        "review": "3. السجلات التي تحتاج إلى مراجعة",
        "only_anomalies": "عرض السجلات غير المعتادة فقط",
        "protocol_filter": "تصفية حسب البروتوكول",
        "all": "الكل",
        "download": "⬇️ تنزيل النتائج المصنفة CSV",
        "download_name": "نتائج_تحليل_الشبكة.csv",
        "evaluation": "4. التقييم على مجموعة اختبار لم تدخل في التدريب",
        "train_rows": "عدد سجلات التدريب",
        "test_rows": "عدد سجلات الاختبار",
        "synthetic_note": "وسوم البيانات الاصطناعية لا تدخل في تدريب النموذج.",
        "precision": "Precision للشذوذ",
        "recall": "Recall للشذوذ",
        "f1": "F1 للشذوذ",
        "confusion": "مصفوفة الالتباس (الصفوف: الحقيقة، الأعمدة: توقع النموذج)",
        "actual_normal": "الحقيقة: طبيعي",
        "actual_unusual": "الحقيقة: غير معتاد",
        "pred_normal": "توقع: طبيعي",
        "pred_unusual": "توقع: غير معتاد",
        "no_labels": "الملف لا يحتوي على synthetic_label؛ لذلك نعرض نتائج اكتشاف الشذوذ فقط دون مقاييس تقييم مرجعية.",
        "warning": "تنبيه: السجل غير المعتاد ليس بالضرورة هجومًا. المقاييس الحالية تخص بيانات اصطناعية فقط.",
        "start_info": "اضغط «تحليل السجلات» لبدء التحليل.",
        "source_name": "مصدر البيانات",
        "all_protocols": "جميع البروتوكولات",
    },
    "tr": {
        "page_title": "Yapay Zekâ Destekli Ağ Trafiği Analizörü",
        "caption": "Makine öğrenmesi ile ağ trafiğindeki olağan dışı örüntüleri tespit etmeye yönelik eğitim projesi.",
        "language": "🌐 Dil",
        "settings": "Analiz Ayarları",
        "contamination": "Tahmini anormallik oranı",
        "contamination_help": "Olağan dışı kayıtların tahmini oranıdır; bağlantının kötü amaçlı olma olasılığı değildir.",
        "security_notice": "Sonuçlar inceleme amaçlı göstergelerdir, kesin bir güvenlik hükmü değildir. Yalnızca analiz izniniz olan verileri kullanın.",
        "source": "1. Veri Kaynağı",
        "upload": "Analiz etmek için CSV dosyası yükleyin (isteğe bağlı)",
        "regenerate": "Örnek verileri kullan / yeniden oluştur",
        "read_error": "Veriler okunamadı",
        "missing_columns": "Dosyada gerekli sütunlar bulunmuyor",
        "preview": "Ham Verileri Önizle",
        "analyze": "🔍 Kayıtları Analiz Et",
        "training": "Veriler bölünüyor ve anormallik tespit modeli eğitiliyor...",
        "analysis_error": "Analiz sırasında bir hata oluştu",
        "summary": "2. Sonuç Özeti",
        "total": "Toplam kayıt",
        "anomalies": "Anormal kayıtlar",
        "normal": "Normal kayıtlar",
        "distribution": "Sınıflandırma Dağılımı",
        "by_protocol": "Protokole Göre Kayıt Sayısı",
        "normal_chart": "Normal",
        "unusual_chart": "Anormal",
        "record_count": "Kayıt sayısı",
        "review": "3. İncelenmesi Gereken Kayıtlar",
        "only_anomalies": "Yalnızca anormal kayıtları göster",
        "protocol_filter": "Protokole göre filtrele",
        "all": "Tümü",
        "download": "⬇️ Sınıflandırılmış Sonuçları CSV Olarak İndir",
        "download_name": "ag_trafik_analiz_sonuclari.csv",
        "evaluation": "4. Eğitimde Kullanılmamış Test Kümesiyle Değerlendirme",
        "train_rows": "Eğitim kayıt sayısı",
        "test_rows": "Test kayıt sayısı",
        "synthetic_note": "Sentetik veri etiketleri model eğitiminde kullanılmaz.",
        "precision": "Anormallik Precision",
        "recall": "Anormallik Recall",
        "f1": "Anormallik F1",
        "confusion": "Karışıklık Matrisi (satırlar: gerçek, sütunlar: model tahmini)",
        "actual_normal": "Gerçek: Normal",
        "actual_unusual": "Gerçek: Anormal",
        "pred_normal": "Tahmin: Normal",
        "pred_unusual": "Tahmin: Anormal",
        "no_labels": "Dosyada synthetic_label bulunmuyor. Bu nedenle yalnızca anormallik tespit sonuçları gösteriliyor; referans değerlendirme metrikleri hesaplanamıyor.",
        "warning": "Uyarı: Anormal bir kayıt mutlaka saldırı anlamına gelmez. Mevcut değerlendirme metrikleri yalnızca sentetik veriler içindir.",
        "start_info": "Analizi başlatmak için «Kayıtları Analiz Et» düğmesine tıklayın.",
        "source_name": "Veri kaynağı",
        "all_protocols": "Tüm protokoller",
    },
    "en": {
        "page_title": "AI Network Traffic Analyzer",
        "caption": "An educational machine-learning project for detecting unusual patterns in network traffic.",
        "language": "🌐 Language",
        "settings": "Analysis Settings",
        "contamination": "Estimated anomaly proportion",
        "contamination_help": "Estimated share of unusual records, not the probability that a connection is malicious.",
        "security_notice": "Results are indicators for review, not a final security verdict. Analyze only data you are authorized to use.",
        "source": "1. Data Source",
        "upload": "Upload a CSV file to analyze (optional)",
        "regenerate": "Use / regenerate sample data",
        "read_error": "Could not read the data",
        "missing_columns": "The file is missing required columns",
        "preview": "Preview Original Data",
        "analyze": "🔍 Analyze Records",
        "training": "Splitting data and training the anomaly detection model...",
        "analysis_error": "An error occurred during analysis",
        "summary": "2. Results Summary",
        "total": "Total records",
        "anomalies": "Unusual records",
        "normal": "Normal records",
        "distribution": "Classification Distribution",
        "by_protocol": "Records by Protocol",
        "normal_chart": "Normal",
        "unusual_chart": "Unusual",
        "record_count": "Number of records",
        "review": "3. Records Requiring Review",
        "only_anomalies": "Show unusual records only",
        "protocol_filter": "Filter by protocol",
        "all": "All",
        "download": "⬇️ Download Classified Results as CSV",
        "download_name": "network_traffic_analysis.csv",
        "evaluation": "4. Evaluation on a Held-Out Test Set",
        "train_rows": "Training records",
        "test_rows": "Test records",
        "synthetic_note": "Synthetic data labels are not used to train the model.",
        "precision": "Anomaly Precision",
        "recall": "Anomaly Recall",
        "f1": "Anomaly F1",
        "confusion": "Confusion Matrix (rows: actual, columns: predicted)",
        "actual_normal": "Actual: Normal",
        "actual_unusual": "Actual: Unusual",
        "pred_normal": "Predicted: Normal",
        "pred_unusual": "Predicted: Unusual",
        "no_labels": "The file does not contain synthetic_label. Only anomaly detection results are shown; reference evaluation metrics are unavailable.",
        "warning": "Warning: an unusual record is not necessarily an attack. Current evaluation metrics apply to synthetic data only.",
        "start_info": "Click “Analyze Records” to begin.",
        "source_name": "Data source",
        "all_protocols": "All protocols",
    },
}


st.set_page_config(
    page_title="AI Network Traffic Analyzer",
    page_icon="🛡️",
    layout="wide",
)

# Language selector at the top of the page.
language_col, title_col = st.columns([1, 3])

with language_col:
    language_name = st.selectbox(
        "🌐 Language",
        options=list(LANGUAGES.keys()),
        index=0,
        key="language_choice",
    )

lang = LANGUAGES[language_name]
T = TEXT[lang]

# Basic right-to-left support for Arabic.
if lang == "ar":
    st.markdown(
        """
        <style>
        .stApp, [data-testid="stSidebar"] {
            direction: rtl;
            text-align: right;
        }
        [data-testid="stMarkdownContainer"],
        [data-testid="stWidgetLabel"] {
            text-align: right;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
else:
    st.markdown(
        """
        <style>
        .stApp, [data-testid="stSidebar"] {
            direction: ltr;
            text-align: left;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

with title_col:
    st.title(f"🛡️ {T['page_title']}")

st.caption(T["caption"])

with st.sidebar:
    st.header(T["settings"])
    contamination = st.slider(
        T["contamination"],
        min_value=0.02,
        max_value=0.20,
        value=0.10,
        step=0.01,
        help=T["contamination_help"],
    )
    st.info(T["security_notice"])

st.subheader(T["source"])
uploaded = st.file_uploader(T["upload"], type=["csv"])

if st.button(T["regenerate"]):
    DEFAULT_DATA.parent.mkdir(parents=True, exist_ok=True)
    generate_dataset().to_csv(DEFAULT_DATA, index=False)
    for key in ("scored_data", "evaluation", "train_rows", "test_rows"):
        st.session_state.pop(key, None)
    st.rerun()

if not DEFAULT_DATA.exists():
    DEFAULT_DATA.parent.mkdir(parents=True, exist_ok=True)
    generate_dataset().to_csv(DEFAULT_DATA, index=False)

try:
    raw_df = (
        pd.read_csv(uploaded)
        if uploaded is not None
        else pd.read_csv(DEFAULT_DATA)
    )
    source_name = (
        uploaded.name
        if uploaded is not None
        else "data/network_traffic.csv"
    )
except Exception as exc:
    st.error(f"{T['read_error']}: {exc}")
    st.stop()

missing = [col for col in REQUIRED_COLUMNS if col not in raw_df.columns]
if missing:
    st.error(f"{T['missing_columns']}: " + ", ".join(missing))
    st.stop()

st.caption(f"{T['source_name']}: `{source_name}`")

with st.expander(T["preview"]):
    st.dataframe(raw_df.head(30), use_container_width=True)

if st.button(T["analyze"], type="primary"):
    try:
        with st.spinner(T["training"]):
            result = analyze_data(raw_df, contamination=contamination)

        st.session_state["scored_data"] = result.scored_data
        st.session_state["evaluation"] = result.evaluation
        st.session_state["train_rows"] = result.train_rows
        st.session_state["test_rows"] = result.test_rows
        st.session_state["source_name"] = source_name

    except Exception as exc:
        st.error(f"{T['analysis_error']}: {exc}")

scored = st.session_state.get("scored_data")

if scored is not None:
    st.subheader(T["summary"])

    total = len(scored)
    anomalies = int(scored["anomaly"].sum())

    c1, c2, c3 = st.columns(3)
    c1.metric(T["total"], f"{total:,}")
    c2.metric(T["anomalies"], f"{anomalies:,}")
    c3.metric(T["normal"], f"{total - anomalies:,}")

    left, right = st.columns(2)

    with left:
        st.markdown(f"**{T['distribution']}**")
        fig, ax = plt.subplots()
        ax.bar(
            [T["normal_chart"], T["unusual_chart"]],
            [total - anomalies, anomalies],
        )
        ax.set_ylabel(T["record_count"])
        st.pyplot(fig)
        plt.close(fig)

    with right:
        st.markdown(f"**{T['by_protocol']}**")
        counts = scored["protocol"].value_counts()
        fig, ax = plt.subplots()
        ax.bar(counts.index.astype(str), counts.values)
        ax.set_ylabel(T["record_count"])
        st.pyplot(fig)
        plt.close(fig)

    st.subheader(T["review"])

    filter_anomalies = st.checkbox(T["only_anomalies"], value=True)

    protocol_values = sorted(scored["protocol"].astype(str).unique().tolist())
    protocol_options = [T["all"]] + protocol_values

    selected_protocol = st.selectbox(
        T["protocol_filter"],
        protocol_options,
    )

    view = (
        scored[scored["anomaly"]].copy()
        if filter_anomalies
        else scored.copy()
    )

    if selected_protocol != T["all"]:
        view = view[view["protocol"].astype(str) == selected_protocol]

    view = view.sort_values("anomaly_score", ascending=True)
    st.dataframe(view, use_container_width=True, hide_index=True)

    st.download_button(
        T["download"],
        data=scored.to_csv(index=False).encode("utf-8-sig"),
        file_name=T["download_name"],
        mime="text/csv",
    )

    evaluation = st.session_state.get("evaluation")

    if evaluation:
        st.subheader(T["evaluation"])

        st.caption(
            f"{T['train_rows']}: "
            f"{st.session_state.get('train_rows', 0):,} | "
            f"{T['test_rows']}: "
            f"{st.session_state.get('test_rows', 0):,}. "
            f"{T['synthetic_note']}"
        )

        report = evaluation["classification_report"]
        metrics = st.columns(3)

        metrics[0].metric(
            T["precision"],
            f"{report['Unusual (1)']['precision']:.3f}",
        )
        metrics[1].metric(
            T["recall"],
            f"{report['Unusual (1)']['recall']:.3f}",
        )
        metrics[2].metric(
            T["f1"],
            f"{report['Unusual (1)']['f1-score']:.3f}",
        )

        st.write(T["confusion"])

        st.dataframe(
            pd.DataFrame(
                evaluation["confusion_matrix"],
                index=[T["actual_normal"], T["actual_unusual"]],
                columns=[T["pred_normal"], T["pred_unusual"]],
            ),
            use_container_width=True,
        )

    elif LABEL_COLUMN not in scored.columns:
        st.info(T["no_labels"])

    st.warning(T["warning"])

else:
    st.info(T["start_info"])
