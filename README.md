# 👩‍🔬 Gerçek Zamanlı Cilt Problemi Tespiti – YOLOv8n Tabanlı AI Destekli Görüntü İşleme Sistemi

## 🧬 Proje Hakkında
Bu proje, derin öğrenme ve bilgisayarla görme tekniklerini kullanarak insan yüzünde çeşitli cilt problemlerinin tespitini amaçlayan, gerçek zamanlı çalışan bir web uygulamasıdır. Sistem, kullanıcıdan alınan yüz fotoğrafı üzerinde dört farklı cilt problemini tespit ederek, görsel çıktılar ve detaylı tahminler sunar.

---

## 🚀 Temel Özellikler
- ⚡ **Gerçek zamanlı tahmin**: Yüklenen fotoğraflar anında analiz edilir.
- 🧠 **Çoklu model desteği**: Akne, kızarıklık, göz altı torbası ve kırışıklık için ayrı YOLOv8 modelleri.
- 💡 **Hafif ve hızlı**: YOLOv8n mimarisi sayesinde düşük donanımlı cihazlarda bile yüksek hızda çalışır.
- 🧪 **Klinik öncesi değerlendirme**: Dermatologlar ve cilt bakım uzmanları için ön analiz sağlar.
- 🔌 **Kolay entegrasyon**: Flask tabanlı backend ve REST API ile farklı platformlara entegre edilebilir.

---

## 🧠 Tespit Edilen Cilt Problemleri

| Problem Türü          | Açıklama                                                        | Sınıf Sayısı |
|-----------------------|------------------------------------------------------------------|--------------|
| Kırışıklık (Wrinkle)  | Alın, kazayağı, ağız kenarı vb. bölgelerdeki farklı kırışıklıklar| 9            |
| Kızarıklık (Redness)  | Ciltte lokal ya da yaygın şekilde oluşan kızarık alanlar        | 1            |
| Göz Altı Torbası      | Alt göz kapağında sarkma veya şişkinlik oluşumu                 | 1            |
| Akne (Acne)           | Siyah nokta, beyaz nokta, iltihaplı sivilceler dahil çeşitli türler| 1         |

---

## 🏗️ Proje Mimarisi
- Flask tabanlı bir backend servisi üzerinden REST API sağlanır.
- Her model ayrı bir .pt dosyası olarak yüklenir ve paralel çalıştırılır.
- Tahmin sonuçları base64 formatında frontend’e gönderilir.

---

## ⚙️ Kullanılan Teknolojiler

- **YOLOv8n / YOLOv8n-seg** – Ultralytics tarafından sağlanan nesne tespit modeli.
- **PyTorch** – Derin öğrenme için temel framework.
- **Flask** – REST API ve web arayüzü için mikro framework.
- **OpenCV & Pillow** – Görüntü işleme ve format dönüşümleri için.

---

## 🧑‍💻 Yöntemler

- **Bounding Box Tespiti**: Cilt problemleri nesne tespiti ile kutucuk içine alınır.
- **Veri Çeşitliliği**: Farklı yaş, cinsiyet ve cilt tonuna sahip bireylerden veri sağlanmıştır.
- **Augmentasyon Teknikleri**: 
  - Flip (Yansıma)
  - HSV varyasyonları
  - Mosaic
- **Paralel Model Çalıştırma**: `ThreadPoolExecutor` kullanılarak birden fazla model eşzamanlı çalıştırılır.

---

## 📦 Veri Setleri

| Problem | Veri Seti Kaynağı | Etiketleme Türü         |
|--------|--------------------|--------------------------|
| Kırışıklık | Özel veri seti, makesense.ai | Manuel bounding box (9 sınıf) |
| Kızarıklık | Roboflow Redness Dataset | Otomatik etiketleme        |
| Göz Altı Torbası | Puffy Eyes Dataset (Roboflow) | Hazır etiketli               |
| Akne | Özel oluşturulmuş yüz verisi | makesense.ai ile manuel     |

---

## 🏋️‍♂️ Model Eğitimi

| Parametre              | Değer              |
|------------------------|--------------------|
| Model                  | YOLOv8n / YOLOv8n-seg |
| Epoch                  | 50                 |
| Batch Size             | 16                 |
| Görüntü Boyutu         | 640x640            |
| Optimizer              | SGD                |
| Augmentasyon           | Flip, HSV, Mosaic  |
| Eğitim/Doğrulama Oranı | %80 / %20          |


