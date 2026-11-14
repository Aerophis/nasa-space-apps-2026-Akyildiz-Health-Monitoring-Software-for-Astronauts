# Sprint 1 kapanış raporu — AstroCare AI

## 1. Sprint bilgileri ve hedefleri

- Takım: AKYILDIZ · Sprint: 1 / 4 · Tarih: 14 Kasım 2026.
- Yarışma: NASA Space Apps Challenge 2026.
- Görev: Create Health Monitoring Software for Astronauts on Space Missions.
- Scrum Master / takım lideri / ana geliştirici: kullanıcı.
- Hedef: üç sağlık metriğini sentetik verilerle izleyen, tanı/tedavi üretmeyen ilk çalışan prototip.
- Durum: teknik kontroller başarılı; bilimsel karar DÜZELTME GEREKLİ; rapor ve GitHub teslimi Scrum Master onayını bekliyor.
- Kesin sprint saatleri kaydedilmedi. Rapor, Scrum Master'ın sağladığı 11 başlığa göre düzenlendi; Niğde organizasyonunun ayrı format yönergesi henüz sağlanmadı.

## 2. Planlanan görevler

- Tekrarlanabilir demo verisi; ayrı veri, analiz ve grafik modülleri; Streamlit paneli.
- Günlük fark, yedi günlük ortalama, geçerli kayıt sayısı ve eksik/geçersiz veri kontrolleri.
- Otomatik testler, uygulama açılışı, temel arayüz incelemesi ve bilimsel araştırma.
- Planlanan dağılım: liderde koordinasyon/entegrasyon; Muhammed Ali'de Python/test desteği; bilimsel araştırma sorumlusunda literatür ve değerlendirme. Planlanan görevler gerçekleşmiş katkı sayılmaz.

## 3. Gerçekten tamamlanan görevler

- AI destekli Streamlit/Pandas/Plotly prototipi: kurmaca profil, 21 günlük sabit tohumlu veri, üç özet kart, üç etkileşimli grafik, tarih/aralık seçimi ve günlük tablo.
- Önceki takvim gününe göre fark, yedi günlük ortalama ve geçerli ölçüm sayısı; eksikler sıfır sayılmıyor.
- DEMO — SIMULATED DATA etiketi, NASA onayı bulunmaması ve teşhis/ilaç önerisi üretmeme açıklamaları.
- Liderin yazdığını bildirdiği `analyze_daily()` içindeki `sleep_hours` dönüşümü ve iki testi dosyada doğrulandı. Dakika sütunu ve eksik değerler korunuyor.
- Kod/test yapısı ve yerel geliştirme rehberi hazır; 23 test bağımsız yeniden çalıştırıldı.
- Liderin bildirdiği temel arayüz incelemesi ve sohbet ekran görüntüsü mevcut; kapsamlı kullanıcı testi yapılmış sayılmadı.
- İki bilimsel belgenin varlığı ve içerikleri bu kapanışta doğrulandı; uygulamanın bilimsel kabulü tamamlanmış sayılmadı.

## 4. Tamamlanamayan veya ertelenen görevler

- Bilimsel düzeltmelerin yazılı kapanışı ve bilimsel sorumlunun ek uygulama kabul tutanağı.
- NASA resmî Resources listesinin kesin doğrulanması ve uygun gerçek veri entegrasyonu.
- Ölçüm koşulu/sensör kalitesi, kişisel başlangıç değeri ve planlanan–gerçekleşen egzersiz karşılaştırması.
- Ayrıntılı kullanılabilirlik testi ve arayüz iyileştirmeleri.
- Muhammed Ali'nin tamamladığı bireysel görevlerin teyidi; Sprint 1 commit/push onayı.

## 5. Karşılaşılan problemler ve engeller

- İlk arayüz testinde göreli uygulama yolu; kısıtlı terminalde yerel soket erişimi.
- Liderin terminalinde göreli Python yolu bulunamadı; terminalin o andaki klasörü kesin kaydedilmedi.
- Bilimsel PDF hazırlanırken kod/ekran/test çıktıları görülmemiş; bu sınırlama belgenin kendi içinde açıkça yazıyor.
- DOCX'teki bazı durum notları sentetik demoyu henüz oluşturulmamış gösteriyor; bunlar mevcut prototiple güncel değil.
- Yazılı ek bilimsel kabul, bağımsız Scrum format yönergesi ve resmî Resources teyidi yok. README yalnızca depo başlığını içeriyor.

## 6. Uygulanan çözümler

- Arayüz testinin dosya yolu düzeltildi; yerel bağlantı kontrolleri gerekli izinle çalıştırıldı; proje klasörüne geçiş komutu açıklandı.
- PDF, `pypdf`; DOCX, `python-docx` ile paketlenmiş belge araçları kullanılarak ayrıştırıldı. Dosyalar düz metin gibi okunmadı, kaynak belgeler değiştirilmedi, projeye paket kurulmadı.
- PDF'nin 1. ve 8. sayfaları ayrıca görüntülendi. DOCX içerik incelemesi yapıldı; sayfa düzeni/görsel kalite onayı verilmedi.
- Belge tarihindeki kanıt eksikliğiyle bugünkü teknik test sonucu ayrıldı; bilimsel karar değiştirilmedi.
- Bu kapanışta yalnızca bu rapor düzenlendi. Python kodları, testler, README, .gitignore ve requirements.txt değiştirilmedi; yeni özellik eklenmedi.

## 7. Takım üyelerinin bireysel katkıları

| Kişi / destek | Kaydedilen katkı ve kanıt sınırı |
| --- | --- |
| Takım lideri / Scrum Master / ana geliştirici | Planlama, Codex yönlendirmesi, bilimsel koordinasyon ve arayüz incelemesi kendi beyanına dayanıyor. Kendi yazdığını belirttiği sleep_hours hesabı ile iki test dosyada mevcut ve yeniden çalıştırıldı; yazarlık beyanı kullanıcıya ait. |
| Muhammed Ali | Python/test destek rolü mevcut; tamamlanmış bireysel görevler hakkında ayrıntılı doğrulanmış kayıt yok. Katkılar teyit bekliyor. |
| Bilimsel araştırma sorumlusu — eczacılık öğrencisi, liderin kuzeni | Liderin atfına göre araştırma/rapor hazırlama, ölçüm ve kaynak/lisans incelemesi, ortak değerlendirme ve Sprint 2 önerileri. İki belge ve bilimsel içerikleri görüldü; kişisel yazarlık ve ortak toplantı ayrıntıları bağımsız doğrulanmadı. |
| Codex — AI desteği | İlk prototip ve başlangıçtaki 21 test, teknik doğrulama, belge incelemesi ve raporlama desteği. Tüm prototip liderin elle yazdığı kod olarak sunulmaz. |

## 8. Test ve doğrulama sonuçları

- Son bağımsız çalıştırma: `.\.venv\Scripts\python.exe -m pytest -q` → **23 passed in 1.47s**.
- Önceki kapanış çalıştırması 1.52s; liderin bildirdiği önceki çalıştırma 1.44s idi. Süre farkı ayrı çalıştırmalardan kaynaklanır.
- `test_sleep_minutes_to_hours`: 450 dakika → 7.5 saat; `test_missing_sleep_data`: None → NaN, sıfıra dönüştürülmüyor.
- Diğer testler veri üretimi, takvim boşlukları, geçersiz/yinelenen kayıtlar, fark/ortalama, grafik serileri ve arayüz tarih/aralık kontrollerini kapsıyor. Test kapsam yüzdesi ölçülmedi.
- Uygulama importları ve `pip check` başarılı. Önceki denetimde requirements.txt ile kurulu sürümlerin eşleşmesi doğrulandı.
- Python 3.11.9; Streamlit 1.67.0; Pandas 3.1.1; Plotly 7.1.0; pytest 9.2.0.
- Geçici 127.0.0.1:8502 sunucusu yeniden başlatıldı: sağlık 200 / ok, ana sayfa 200. Kontrol sonrası durduruldu; mevcut 8501 oturumuna dokunulmadı.
- .gitignore sanal ortamı, önbellekleri, yerel sırları ve geçici dosyaları dışlıyor. Teslim listesi bilimsel belgeleri kapsamıyor. Temel gizli bilgi/büyük dosya kontrolü mutlak güvence değildir.
- Teknik test başarısı klinik doğrulama veya bilimsel kabul yerine geçmez.

## 9. Bilimsel incelemenin sonucu ve açık maddeler

İncelenen yerel belgeler (GitHub teslimine dahil değil):

- `docs/research/AKYILDIZ_Sprint1_Bilimsel_Dogrulama_Raporu.pdf`: 8 sayfa; karar 1. ve 8. sayfalarda **DÜZELTME GEREKLİ**.
- `docs/research/AstroCare_Bilimsel_Arastirma_Duzeltilmis.docx`: bilimsel araştırma, ölçüm sınırlamaları, kaynak/lisans matrisi ve NASA veri kaynakları değerlendirmesi.

Ayrı `AstroCare_Bilimsel_Arastirma_Duzeltilmis.pdf` dosyası bu klasörde yok; incelenmiş sayılmadı.

PDF, bilimsel eğilim tasarımını koşullu uygun buluyor; hazırlanırken uygulama kodu, ekranlar ve testlerin incelenmediğini belirtiyor. Bugünkü teknik denetimde bu unsurlar kısmen bağımsız doğrulandı; bu durum bilimsel sorumlunun yeni kabul tutanağı değildir. Ortak ek inceleme lider tarafından bildirildi, yazılı kapanış yok. **DÜZELTME GEREKLİ kararı korunuyor.**

| Bilimsel öneri | Mevcut teknik kanıt / açık iş |
| --- | --- |
| Eksik ölçümü sıfır saymama, geçerli kayıt sayısı | Kod ve testlerde doğrulandı; düşük kapsama için açıklayıcı bildirim geliştirmesi açık. |
| Sentetik köken ve klinik iddia sınırı | Genel demo etiketi ve kaynak alanları mevcut; her grafik/istatistik için ayrıntılı köken/kalite izi kısmi. |
| Gün ve yedi günlük pencere | UTC takvim günü, ortalama ve sayım mevcut; başlangıç/bitiş saatlerinden gece yarısını aşan uyku hesabı yok. |
| Dinlenme nabzında karşılaştırılabilir koşullar | Yalnızca sentetik seri var; dinlenme durumu/sensör kalitesi ve kişisel baz çizgisi yok. |
| Egzersizde plan, gerçekleşme ve tür | Yalnızca süre var; plan/tür karşılaştırması yok. Süreden kas/kemik teşhisi üretilmiyor. |
| NASA verisi ve lisans izi | Gerçek veri indirme/işleme/entegrasyonu yok; kaynak ve dosya bazlı uygunluk açık. |

Belgelerdeki uyku önerisi, nabız koşulları ve egzersiz sınırlamaları klinik alarm/teşhis kuralına dönüştürülmedi. DOCX'teki henüz üretilmemiş demo notları, belgenin kanıt anını yansıtır; güncel prototip durumu bölüm 3 ve 8'de kayıtlıdır.

Belgeler OSD-575'i üç metriğin günlük serisi yerine serum biyokimyası kaynağı olarak değerlendiriyor. Resmî Resources listesinin tam doğrulanamadığını, ikincil listenin kesin uygunluk kanıtı olmadığını belirtiyorlar. Bu kapanışta dış kaynakların tümü veya lisans iddiaları yeniden doğrulanmadı. **NASA veri entegrasyonu ve Resources şartının karşılandığı iddia edilmez.** Bilimsel belgelerin paylaşım hakları onaylanmadı; GitHub'a eklenmeyecekler.

## 10. Sprint 2'ye aktarılan işler

Scrum Master'ın öncelik sırası; bu kapanışta geliştirme başlatılmadı:

1. Veri kaynağı ve ölçüm kalitesinin daha iyi gösterilmesi.
2. Eksik, tekrarlı ve geçersiz ölçüm kontrollerinin genişletilmesi.
3. Kullanıcı tarafından yeni sağlık kaydı girilmesi.
4. Kişisel başlangıç değerleriyle karşılaştırma.
5. Kaynaklara dayalı, tanı koymayan açıklayıcı bildirimler ve bilimsel düzeltmelerin yazılı takibi.
6. Planlanan–gerçekleşen egzersiz ve egzersiz türü karşılaştırması.
7. NASA resmî Resources listesinin kesin doğrulanması — açık, yüksek öncelikli araştırma işi.
8. Uygun NASA veri kaynağının gerçekten kullanılması — kaynak/lisans/alan uygunluğu doğrulandıktan sonra, açık ve yüksek öncelikli entegrasyon işi.
9. Arayüz iyileştirmeleri; yöntem alanındaki Markdown/görünüm sorununun değerlendirilmesi.

Ollama yalnızca zaman ve teknik uygunluk varsa ileride değerlendirilecek. Gelecek Python görevlerinde dosya adı, tam yol, fonksiyon, konum, görev, beklenen sonuç, test ve VS Code Explorer yolu belirtilecek; önce ipucu verilip liderin kodu yazması beklenecek.

## 11. GitHub commit ve kanıt bağlantıları

- [Depo](https://github.com/Aerophis/nasa-space-apps-2026-Akyildiz-Health-Monitoring-Software-for-Astronauts).
- [13feb3b ortam hazırlığı](https://github.com/Aerophis/nasa-space-apps-2026-Akyildiz-Health-Monitoring-Software-for-Astronauts/commit/13feb3bf71c91892d48266dd3293cf1915533f9c): yarışma öncesi ortam hazırlığı; Sprint 1 uygulama geliştirme commit'i değildir.
- Yerel kanıtlar: [analiz](../astrocare/analysis.py), [liderin testleri](../tests/test_sleep_hours.py), [veri/grafik testleri](../tests/test_analysis.py), [arayüz testi](../tests/test_app.py), [çalıştırma rehberi](development.md). Henüz uzak Sprint 1 kanıtı değiller.
- Sprint 1 commit/push yapılmadı; yeni commit bağlantısı ancak onay ve teslim sonrası kaydedilecek. Test terminal çıktıları bu sohbet içinde, ayrı dosya olarak oluşturulmadı.
- Teslim adayları: `app.py`, `astrocare/__init__.py`, `astrocare/data.py`, `astrocare/analysis.py`, `astrocare/charts.py`, `tests/test_analysis.py`, `tests/test_app.py`, `tests/test_sleep_hours.py`, `docs/development.md`, `docs/sprint-1.md`.
- Bu 10 dosya dışında ekleme yapılmayacak. Bilimsel PDF/DOCX, .venv, önbellekler, sırlar ve geçici dosyalar hariç. `docs/research/` yerelde izlenmeyen dosyalar olarak kalacak; toplu `git add .` kullanılmayacak.
- Git indeksi boş; commit/push için Scrum Master onayı bekleniyor. README, .gitignore ve requirements.txt değiştirilmedi. README'ye kısa kurulum özeti eklenmesi yalnızca öneridir.
