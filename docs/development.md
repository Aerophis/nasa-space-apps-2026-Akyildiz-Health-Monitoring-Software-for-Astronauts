# AstroCare AI — yerel geliştirme

Proje kökünde PowerShell ile:

```powershell
.\.venv\Scripts\python.exe -m streamlit run app.py
```

Tarayıcı: http://localhost:8501 · Durdurmak için terminalde Ctrl+C.
Sanal ortamı aktive etmek zorunlu değildir; bu komut doğrudan proje Python'unu kullanır.

Testler:

```powershell
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe -m pip check
```

`astrocare/data.py` sabit tohumla sentetik veri üretir ve günlük takvimi doğrular.
`astrocare/analysis.py` günlük farkları ve yedi günlük ortalamaları hesaplar.
`astrocare/charts.py` grafikleri, `app.py` arayüzü oluşturur.

Demo tarihleri sabittir: 25 Ekim – 14 Kasım 2026. Kaynak veriler diskten veya
internet üzerinden alınmaz. Hesaplamalar UTC takvim günü bazındadır; bu demo
uygulaması tek kurmaca astronotu kabul eder. Dosya yükleme/API entegrasyonu yoktur.

Boş/geçersiz tarihler dışlanır; tüm tarihler geçersizse hata gösterilir.
Eksik sayılar tahmin edilmez. Aynı gündeki birden fazla kayıt sessizce birleştirilmez.
Yedi günlük pencere seçili gün dahil takvim günlerini kapsar. İlk günlerde veya
eksik veride ortalama daha az gözleme dayanır; kartlarda sayı gösterilir.
Bu hesaplamalar klinik doğrulama veya sağlık önerisi anlamına gelmez.

Bilimsel bağlantılar bağlam içindir; sentetik veri bu kaynaklardan alınmamıştır.
Literatürün ayrıntılı doğrulanması ve ekip kabulü ayrıca yapılmalıdır.
