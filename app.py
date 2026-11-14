"""AstroCare AI Streamlit entry point."""

import pandas as pd
import streamlit as st

from astrocare.analysis import analyze_daily
from astrocare.charts import METRIC_LABELS, trend_chart
from astrocare.data import generate_demo_data, prepare_daily_data


def display_value(value, metric):
    if pd.isna(value):
        return "Veri yok"
    if metric == "sleep_minutes":
        minutes = round(value)
        return f"{minutes // 60} sa {minutes % 60:02d} dk"
    unit = "bpm" if metric == "resting_hr_bpm" else "dk"
    return f"{value:.1f} {unit}"


def main():
    st.set_page_config(page_title="AstroCare AI | AKYILDIZ", page_icon="✦", layout="wide")
    st.markdown("""<style>
    .stApp {background: radial-gradient(ellipse at top left, #152844, #080f1e 65%); color: #eef4ff;}
    [data-testid="stSidebar"] {background: #101c30;}
    [data-testid="stMetric"] {background: #14243b; border: 1px solid #344b68;
        border-radius: 12px; padding: 18px;}
    </style>""", unsafe_allow_html=True)
    st.caption("AKYILDIZ  /  GÖREV SAĞLIĞI İZLEME PROTOTİPİ  /  SPRINT 1")
    st.title("✦ AstroCare AI")
    st.write("Günlük ölçümleri incele, zaman içindeki değişimi takip et.")
    st.warning("DEMO — SIMULATED DATA · Tüm ölçümler kurmacadır; gerçek NASA veya astronot sağlık verisi değildir.")
    st.caption("Bu prototip teşhis, tıbbi risk puanı veya ilaç önerisi üretmez. NASA tarafından onaylanmış bir ürün değildir. Bu sürümde yapay zekâ modeli kullanılmaz.")
    try:
        daily, notices = prepare_daily_data(generate_demo_data())
        analyzed = analyze_daily(daily)
    except ValueError as exc:
        st.error(f"Veri hazırlanamadı: {exc}")
        st.stop()
    for notice in notices:
        st.warning(notice)

    with st.sidebar:
        st.header("Demo mürettebat profili")
        st.subheader("Deniz Yıldız")
        st.write("Kurmaca astronot · DEMO-001")
        st.caption("Simülasyon: AKYILDIZ-01\n\nKaynak: synthetic_demo\n\nProfil ve görev bilgileri kurmacadır.")
        selected = st.selectbox("İncelenecek gün", list(analyzed.index.date), index=len(analyzed) - 1)
        window = st.radio("Grafik aralığı", [7, 14, 21], index=2, format_func=lambda n: f"Son {n} gün")
        st.caption("Sabit demo dönemi: 25 Ekim – 14 Kasım 2026. Sayfa yenilendiğinde ölçümler değişmez.")

    endpoint = pd.Timestamp(selected)
    row = analyzed.loc[endpoint]
    shown = analyzed.loc[endpoint - pd.Timedelta(days=window - 1):endpoint]
    st.subheader(f"Günlük genel bakış · {endpoint:%d.%m.%Y}")
    for column, (metric, (label, unit, _)) in zip(st.columns(3), METRIC_LABELS.items()):
        with column:
            delta = row[f"{metric}_delta"]
            st.metric(label, display_value(row[metric], metric),
                      delta=f"{delta:+.1f} {unit}" if pd.notna(delta) else None,
                      delta_color="off")
            st.caption("Önceki takvim gününe göre fark" if pd.notna(delta) else "Önceki gün karşılaştırması için yeterli veri yok.")
            count = int(row[f"{metric}_count7"])
            st.write("7 günlük ortalama: " + display_value(row[f"{metric}_mean7"], metric))
            st.caption(f"Son 7 takvim gününde {count}/7 geçerli ölçüm")

    trends, records, research = st.tabs(["Günlük eğilimler", "Günlük kayıtlar", "Bilimsel bağlam ve yöntem"])
    with trends:
        st.caption("Kesikli çizgi: seçili gün dahil son 7 takvim günündeki mevcut ölçümlerin ortalaması. Eksikler doldurulmaz; grafik aralığından önceki günler ortalamaya katılabilir.")
        for metric in METRIC_LABELS:
            st.plotly_chart(trend_chart(shown, metric), width="stretch", key=f"chart_{metric}")
    with records:
        st.write("Grafiklerde görünen dönemin günlük ölçümleri")
        st.dataframe(shown[list(daily.columns)].reset_index(), hide_index=True, width="stretch")
        st.caption("Uyku ve aktivite dakika, dinlenme kalp atım hızı bpm cinsindedir. Tarihler UTC gününe göre işlenir.")
    with research:
        st.subheader("Araştırma başlangıç noktaları")
        st.markdown("""
        - [NASA Fatigue Countermeasures Laboratory](https://www.nasa.gov/human-systems-integration-division/human-performance/fatigue-countermeasures-laboratory/): uyku ve sirkadiyen ritim araştırmaları.
        - [NASA Wearable Tech for Space Station Research](https://www.nasa.gov/humans-in-space/wearable-tech-for-space-station-research/): uyku, egzersiz ve kalp sağlığının giyilebilir cihazlarla incelenmesine örnekler.
        """)
        st.info("Bu kaynaklar bilimsel bağlam içindir. Demo değerleri bu araştırmalardan alınmadı; klinik eşik veya kişisel öneri türetilmedi. Ayrıntılı literatür doğrulaması ekip tarafından yapılacak.")
        st.markdown("""**Yöntem:** Sabit tohum (2026) ile 21 günlük sentetik veri üretilir.
        Günlük fark, önceki takvim gününe göre hesaplanır. Yedi günlük ortalama mevcut
        değerleri kullanır; eksik değerler sıfır sayılmaz. İlk günlerdeki ortalama
        kısmi pencereye dayanır ve kartta ölçüm sayısı gösterilir.

        **Veri kalitesi:** Sayısal olmayan/sonsuz değerler ve negatif süreler dışlanır.
        Günlük süreler 0–1440 dakika, kalp atım hızı pozitif sonlu sayı olmalıdır.
        Bunlar yalnızca veri biçimi kontrolleridir, sağlıklı/sağlıksız sınırları değildir.
        Yinelenen günler reddedilir. Eksik günlerde grafik çizgisi kesilir.
        """)
    st.caption("AKYILDIZ · AstroCare AI · Sentetik veriyle açıklayıcı analiz")


if __name__ == "__main__":
    main()
