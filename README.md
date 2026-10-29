# 🛡️ AI Network Traffic Anomaly Detector

**A multilingual network traffic analysis and anomaly detection project built with Python and Machine Learning.**

[English](#-english) | [Türkçe](#-türkçe) | [العربية](#-العربية)

---

## 🇬🇧 English

### About the Project

AI Network Traffic Anomaly Detector is an educational cybersecurity project that analyzes network traffic data and identifies potentially unusual patterns using machine learning.

It supports CSV datasets and converts PCAP/PCAPNG captures into flow-level features for analysis. An interactive Streamlit dashboard allows users to explore traffic statistics and anomaly detection results.

### Features

- Analyze network traffic data with Pandas.
- Convert PCAP/PCAPNG captures into CSV using Scapy.
- Detect potentially unusual traffic patterns using Isolation Forest.
- Visualize results through an interactive Streamlit dashboard.
- Generate synthetic network traffic datasets for testing.
- Switch between Arabic, Turkish, and English interfaces.

### Technologies

- Python
- Pandas
- Scikit-learn
- Scapy
- Streamlit
- Matplotlib

### Installation

**1. Clone the repository**

```bash
git clone https://github.com/abdulkerim-bustani/AI-Network-Traffic-Anomaly-Detector.git
cd AI-Network-Traffic-Anomaly-Detector
```

**2. Create a virtual environment**

```bash
python -m venv .venv
```

**3. Activate the environment on Windows PowerShell**

```powershell
.\.venv\Scripts\Activate.ps1
```

**4. Install dependencies**

```bash
python -m pip install -r requirements.txt
```

**5. Run the application**

```bash
python -m streamlit run app.py
```

### Limitations

An anomaly is not necessarily a cyberattack. Results depend on the dataset, selected features, and model configuration. This project is intended for learning and experimentation, not as a standalone intrusion detection system.

### Privacy and Security

Only analyze traffic you are authorized to inspect. Review captures before sharing them, and never publish private PCAP/PCAPNG files, sensitive IP information, credentials, or confidential network data.

---

## 🇹🇷 Türkçe

### Proje Hakkında

AI Network Traffic Anomaly Detector, ağ trafiğini analiz etmek ve makine öğrenmesi kullanarak olağan dışı olabilecek trafik örüntülerini belirlemek amacıyla geliştirilmiş eğitsel bir siber güvenlik projesidir.

Proje, CSV veri kümelerini analiz eder ve PCAP/PCAPNG dosyalarını akış seviyesindeki özelliklere dönüştürür. Streamlit tabanlı etkileşimli arayüz sayesinde trafik istatistikleri ve anomali tespit sonuçları incelenebilir.

### Özellikler

- Pandas ile ağ trafiği verilerini analiz etme.
- Scapy ile PCAP/PCAPNG dosyalarını CSV formatına dönüştürme.
- Isolation Forest ile olağan dışı olabilecek trafik örüntülerini tespit etme.
- Streamlit ile etkileşimli bir analiz paneli sunma.
- Test amacıyla sentetik ağ trafiği verileri oluşturma.
- Arapça, Türkçe ve İngilizce arayüz seçenekleri.

### Kullanılan Teknolojiler

- Python
- Pandas
- Scikit-learn
- Scapy
- Streamlit
- Matplotlib

### Kurulum

**1. Depoyu klonlayın**

```bash
git clone https://github.com/YOUR-USERNAME/AI-Network-Traffic-Anomaly-Detector.git
cd AI-Network-Traffic-Anomaly-Detector
```

**2. Sanal ortam oluşturun**

```bash
python -m venv .venv
```

**3. Windows PowerShell üzerinde sanal ortamı etkinleştirin**

```powershell
.\.venv\Scripts\Activate.ps1
```

**4. Bağımlılıkları yükleyin**

```bash
python -m pip install -r requirements.txt
```

**5. Uygulamayı çalıştırın**

```bash
python -m streamlit run app.py
```

### Sınırlamalar

Bir anomali mutlaka siber saldırı anlamına gelmez. Sonuçlar veri kümesine, kullanılan özelliklere ve model ayarlarına bağlıdır. Bu proje eğitim ve deneme amacıyla geliştirilmiştir; tek başına kapsamlı bir saldırı tespit sistemi değildir.

### Gizlilik ve Güvenlik

Yalnızca inceleme yetkiniz bulunan ağ trafiğini analiz edin. Dosyaları paylaşmadan önce kontrol edin; kişisel PCAP/PCAPNG kayıtlarını, hassas IP bilgilerini, parolaları veya gizli ağ verilerini herkese açık olarak yayımlamayın.

---

## 🇸🇾 العربية

### نبذة عن المشروع

**AI Network Traffic Anomaly Detector** هو مشروع تعليمي في الأمن السيبراني يستخدم Python وتعلّم الآلة لتحليل بيانات حركة الشبكة واكتشاف الأنماط التي قد تكون غير معتادة.

يدعم المشروع تحليل ملفات CSV وتحويل ملفات التقاط الشبكة PCAP/PCAPNG إلى خصائص على مستوى تدفقات الاتصال. كما يوفر لوحة تفاعلية باستخدام Streamlit لعرض إحصائيات الشبكة ونتائج اكتشاف الشذوذ.

### المميزات

- تحليل بيانات حركة الشبكة باستخدام Pandas.
- تحويل ملفات PCAP/PCAPNG إلى CSV باستخدام Scapy.
- اكتشاف الأنماط غير المعتادة باستخدام خوارزمية Isolation Forest.
- عرض النتائج من خلال لوحة تفاعلية باستخدام Streamlit.
- إنشاء بيانات شبكة اصطناعية لأغراض الاختبار.
- واجهة بثلاث لغات: العربية والتركية والإنجليزية.

### التقنيات المستخدمة

- Python
- Pandas
- Scikit-learn
- Scapy
- Streamlit
- Matplotlib

### التثبيت والتشغيل

**1. استنساخ المستودع**

```bash
git clone https://github.com/YOUR-USERNAME/AI-Network-Traffic-Anomaly-Detector.git
cd AI-Network-Traffic-Anomaly-Detector
```

**2. إنشاء بيئة افتراضية**

```bash
python -m venv .venv
```

**3. تفعيل البيئة على Windows PowerShell**

```powershell
.\.venv\Scripts\Activate.ps1
```

**4. تثبيت المكتبات المطلوبة**

```bash
python -m pip install -r requirements.txt
```

**5. تشغيل التطبيق**

```bash
python -m streamlit run app.py
```

### حدود المشروع

اكتشاف نمط غير معتاد لا يعني بالضرورة وجود هجوم إلكتروني. تعتمد النتائج على البيانات والخصائص المستخدمة وإعدادات النموذج. المشروع مخصص للتعلم والتجربة، ولا يُعد نظامًا مستقلًا ومتكاملًا لكشف الاختراقات.

### الخصوصية والأمان

حلّل فقط حركة الشبكة التي لديك صلاحية فحصها. راجع ملفات الالتقاط قبل مشاركتها، ولا تنشر ملفات PCAP/PCAPNG الشخصية أو عناوين IP الحساسة أو كلمات المرور أو بيانات الشبكة السرية.

---

## 📌 Project Status

Educational project under development.

## 📄 License

No license has been specified yet. Add a license before allowing others to reuse or distribute this project.