👩‍🔬 Gerçek Zamanlı Cilt Problemi Tespiti – YOLOv8n Tabanlı AI Destekli Görüntü İşleme Sistemi
🧬 Proje Hakkında
Bu proje, derin öğrenme ve bilgisayarla görme tekniklerini kullanarak insan yüzünde çeşitli cilt problemlerinin tespitini amaçlayan, gerçek zamanlı çalışan bir web uygulamasıdır. Sistem, kullanıcıdan alınan yüz fotoğrafı üzerinde dört farklı cilt problemini tespit ederek, görsel çıktılar ve detaylı tahminler sunar.
🚀 Projenin Temel Özellikleri
Gerçek zamanlı tahmin: Yüklenen fotoğraflar anında analiz edilir.
Çoklu model desteği: Akne, kızarıklık, göz altı torbası ve kırışıklık için ayrı modeller.
Hafif ve hızlı: YOLOv8n mimarisi sayesinde düşük donanımlı cihazlarda bile hızlı çalışır.
Klinik öncesi değerlendirme: Dermatologlar ve cilt bakım uzmanları için ön analiz sağlar.
Kolay entegrasyon: Flask tabanlı backend ve REST API ile farklı platformlara kolayca entegre edilebilir.
🧠 Tespit Edilen Cilt Problemleri
| Problem Türü | Açıklama | Sınıf Sayısı |
|--------------|----------|--------------|
| Kırışıklık (Wrinkle) | Alın, kazayağı, ağız kenarı vb. bölgelerdeki farklı kırışıklıklar | 9 |
| Kızarıklık (Redness) | Ciltte lokal ya da yaygın şekilde oluşan kızarık alanlar | 1 |
| Göz Altı Torbası (Eyebag) | Alt göz kapağında sarkma veya şişkinlik oluşumu | 1 |
| Akne (Acne) | Siyah nokta, beyaz nokta, iltihaplı sivilceler dahil çeşitli türler | 1 |
🏗️ Proje Mimarisi
Apply to yolov8_custo...
⚙️ Kullanılan Teknolojiler ve Yöntemler
📚 AI Framework ve Algoritma Seçimi
Ultralytics YOLOv8:
Hızlı, hafif ve gerçek zamanlı nesne tespiti için endüstri standardı.
yolov8n.pt (nano) modeli, düşük donanımda dahi yüksek performans sunar.
Segmentasyon için yolov8n-seg.pt kullanılmıştır.
PyTorch: YOLOv8’in temel aldığı derin öğrenme framework’ü.
Flask: REST API ve web arayüzü için hafif ve esnek bir Python framework’ü.
OpenCV & Pillow: Görüntü işleme ve renk düzeltmeleri için.
🧑‍💻 Yöntemler
Bounding Box Tespiti: Her cilt problemi için nesne tespiti (object detection) yaklaşımı.
Veri Çeşitliliği: Farklı yaş, cinsiyet ve ten rengine sahip örnekler.
Augmentasyon: Modelin genelleme kabiliyetini artırmak için flip, HSV varyasyonları, mosaic gibi teknikler.
Çoklu Model Paralel Çalıştırma: Flask backend’de ThreadPoolExecutor ile aynı anda birden fazla modelin tahmin yapması sağlanır.
📦 Veri Setleri ve Kaynaklar
Her bir cilt problemi için bağımsız ve özenle etiketlenmiş veri setleri kullanılmıştır:
Kırışıklık:
Özel toplanmış, yüksek çözünürlüklü yüz fotoğrafları
makesense.ai ile manuel bounding-box etiketleme
9 farklı kırışıklık bölgesi
Kızarıklık:
Redness Dataset – Roboflow
Otomatik etiketleme, dengeli veri
Göz Altı Torbası:
Puffy Eyes Dataset – Roboflow
Hazır etiketli, odaklı görüntüler
Akne:
Gerçek yüz örneklerinden oluşturulan özel dataset
makesense.ai ile manuel etiketleme
🏋️‍♂️ Model Eğitimi
Eğitim Parametreleri
| Parametre | Değer |
|-----------|-------|
| Model | YOLOv8n / YOLOv8n-seg |
| Epoch | 50 |
| Batch Size | 16 |
| Image Size | 640x640 |
| Optimizer | SGD |
| Augmentasyon | Flip, HSV varyasyonları, Mosaic |
| Eğitim/Doğrulama Oranı | %80 / %20 |
Eğitim Komutu
Apply to yolov8_custo...
Run
🖥️ Kurulum ve Çalıştırma
1. Gereksinimler
Python 3.8+
pip
2. Bağımlılıkların Kurulumu
Apply to yolov8_custo...
Run
3. Modellerin Yüklenmesi
models/ klasörüne eğitilmiş YOLOv8 modellerinizi yerleştirin:
acne_best_250epochs.pt
redness_model.pt
eyebag_new_best.pt
wrinkle_best.pt
4. Uygulamayı Başlatma
Apply to yolov8_custo...
Run
5. Web Arayüzü
Tarayıcınızda http://localhost:5000 adresine giderek uygulamayı kullanabilirsiniz.
📝 Kod Açıklamaları
app.py:
Flask ile API ve web arayüzü sunar.
Yüklenen fotoğrafı geçici olarak kaydeder, tüm modelleri paralel çalıştırır.
Her modelin çıktısını base64 formatında frontend’e iletir.
Renk bozulmasını önlemek için OpenCV ile BGR→RGB dönüşümü yapılır.
Kodda her fonksiyon ve önemli bloklar açıklama satırları ile detaylandırılmıştır.
