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


# Eğitim Kodunun Açıklaması
Kullanılan YOLOv8 Versiyonu: yolov8n

yolov8n.pt, YOLOv8 ailesinin en hafif modelidir (nano versiyon).

Düşük hesaplama gücü isteyen cihazlarda (ör. CPU) çalıştırmak için uygundur.

Eğitim süresi daha kısadır.

Küçük veri setleriyle hızlı prototipleme ve test için idealdir.

Bu projede cilt verileri sınırlı olduğu için fazla parametreli modellere (s, m, l, x) gerek duyulmamıştır.

🏗️ Model Özelleştirme – Katman Katman Açıklama
CustomYOLOv8 Sınıfı
YOLO sınıfı kalıtılarak özelleştirilmiş bir versiyon oluşturulmuştur. Bu sınıf aşağıdaki modifikasyonları yapar:

🔧 Değiştirilen Ana Katmanlar:
🔁 C2f Katmanları (Derinlik Artırımı):
self.model.model[4] ve self.model.model[6]:

C2f bloklarının tekrar sayısı (n=2) artırılarak daha derin özellik öğrenimi sağlanır.

Kanal sayısı da 256 ve 512 gibi daha geniş tutulmuştur.

Daha karmaşık örüntüler (ör. kırışıklık, akne şekilleri) bu sayede daha iyi temsil edilir.

🧠 AttentionModule (Uzamsal ve Kanal Dikkat Mekanizması):
self.model.model.insert(8, AttentionModule(512))

Spatial (uzamsal) ve Channel (kanal) attention birlikte uygulanır.

Önemli bölgeler (ör. kırışıklık yoğunluğu olan alanlar) vurgulanarak modelin odaklanması sağlanır.

Sigmoid aktivasyon ile dikkat maskeleri oluşturulur.

🌀 SPPF (Spatial Pyramid Pooling Fast):
self.model.model[9]:

k=5 kullanılarak daha geniş alanlardan bilgi toplanır.

Farklı ölçekte bağlam (context) bilgisi öğrenilir.

🧩 Başlık (Head) Katmanı:
self.model.model[15]:

Tahmin öncesi bir C2f bloğu ile son özelliklerin işlenme kapasitesi artırılır.

Daha hassas kutu/sınıf tahminleri yapılır.
Dikkat Katmanı (AttentionModule)

class AttentionModule(nn.Module):

İki parçalı bir dikkat mekanizması içerir;

Spatial Attention: Görsel alanın hangi bölgelerinin daha önemli olduğunu öğrenir.

Channel Attention: Hangi filtrelerin (feature maps) daha anlamlı olduğunu öğrenir.

Her ikisinin çıktısı giriş ile çarpılarak "önemli alanlar" güçlendirilmiş olur.

🧪 Eğitim Fonksiyonu – train()
Model eğitimi için çeşitli hiperparametreler özelleştirilmiştir:

📌 Eğitim Ayarları:
Parametre	Açıklama
epochs=100	Uzun süreli eğitim, istikrarlı öğrenme sağlar.
batch=16	Düşük batch size, RAM kullanımını azaltır.
device='cpu'	Eğitim CPU’da yapılır; GPU varsa cuda olarak değiştirilebilir.
optimizer='SGD'	Daha stabil, kontrollü öğrenme sağlar.

🔧 Optimizasyon Ayarları:
Parametre	Açıklama
lr0=0.01	Başlangıç öğrenme oranı
momentum=0.937	Öğrenme yönünü korumaya yardımcı olur.
weight_decay=0.0005	Ağırlıkların aşırı büyümesini engeller.

🌈 Görüntü Veri Artırma:
Parametre	Açıklama
fliplr=0.5	Yatay çevirme: yüz simetrisi için anlamlı
scale=0.5	Farklı yüz boyutlarına karşı dayanıklılık sağlar
mosaic=1.0	Mozaik birleştirme: veri çeşitliliği ve genelleme gücünü artırır
mixup=0.0	Cilt verisi için uygun görülmemiştir

🧬 Çoklu Model Eğitimi – train_all_models()
Bu fonksiyon dört farklı cilt koşulu için ayrı ayrı model eğitir:

python
Copy
Edit
data_paths = {
    'wrinkles': '.../wrinkles.yaml',
    'eyebags': '.../eyebags.yaml',
    'acne': '.../acne.yaml',
    'redness': '.../redness.yaml'
}
Her veri kümesi için:

Model create_custom_model() ile oluşturulur ve eğitilir.

Eğitilen model models/ dizinine .pt formatında kaydedilir.

Eğitim süresi izlenir ve raporlanır.

🛠️ Model Kaydetme
Eğitim sonrası her model ayrı ayrı şu şekilde kaydedilir:

models[condition].save(f'models/{condition}_model.pt')


