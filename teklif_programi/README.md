# MEFE Makina - Teklif Programı

Windows tabanlı profesyonel teklif hazırlama programı.

## Özellikler

- **Firma Yönetimi**: Sisteme firmalar tanımlanabilir (Firma adı, vergi no, telefon, e-posta, adres)
- **Teklif Numaralandırma**: Otomatik C01-YYMMDD formatında teklif numarası oluşturma
- **Para Birimi Seçenekleri**: TL, USD, EUR desteği
- **Teslimat Tipleri**: Yurt İçi, Yurt Dışı, DAP, DDP, EXW, FOB, CIF seçenekleri
- **Kalem Yönetimi**: Teklife sınırsız kalem ekleme (Kod, açıklama, miktar, birim, birim fiyat)
- **Dışa Aktarma**: PDF ve Excel formatında teklif dışa aktarma
- **Teklif Geçmişi**: Tüm teklifleri görüntüleme ve geçmişten yükleme
- **Veritabanı**: SQLite veritabanı ile kalıcı veri saklama

## Kurulum

1. Python 3.7 veya üzeri sürümün yüklü olduğundan emin olun
2. Gerekli paketleri yükleyin:

```bash
pip install -r requirements.txt
```

## Kullanım

Programı başlatmak için:

```bash
python main.py
```

## Kullanım Kılavuzu

### Yeni Teklif Oluşturma

1. "Yeni Teklif" sekmesine tıklayın
2. Teklif numarası otomatik oluşturulur
3. Firma seçin veya "Yeni Firma" butonu ile yeni firma tanımlayın
4. Teslimat tipi ve para birimi seçin
5. Kalemleri ekleyin:
   - Kod, açıklama, miktar, birim ve birim fiyat girin
   - "Ekle" butonuna tıklayın
6. İsteğe bağlı notlar ekleyin
7. "Kaydet" butonu ile teklifi kaydedin
8. "PDF Dışa Aktar" veya "Excel Dışa Aktar" ile teklifi dışa aktarın

### Firma Yönetimi

1. "Firma Yönetimi" sekmesine tıklayın
2. "Yeni Firma" butonu ile yeni firma ekleyin
3. Firmaları düzenleyin veya silin
4. Listeyi yenilemek için "Yenile" butonunu kullanın

### Teklif Geçmişi

1. "Teklif Geçmişi" sekmesine tıklayın
2. Tüm kayıtlı teklifleri görüntüleyin
3. "Görüntüle" butonu ile eski teklifi formda açın

## Teklif Numarası Formatı

Teklif numaraları şu formatta oluşturulur: `C01-250529`

- `C`: Teklif kodu
- `01`: Günlük sıra numarası (01, 02, 03...)
- `250529`: Tarih (YYMMDD formatı)

## Dosya Yapısı

```
teklif_programi/
├── main.py              # Ana uygulama
├── company_manager.py   # Firma yönetimi modülü
├── quotation_manager.py # Teklif yönetimi modülü
├── export_manager.py    # Dışa aktarma modülü
├── requirements.txt     # Python bağımlılıkları
├── README.md           # Bu dosya
└── teklif.db           # SQLite veritabanı (otomatik oluşturulur)
```

## Sistem Gereksinimleri

- Windows 7 veya üzeri
- Python 3.7+
- 100 MB disk alanı

## Destek

Sorularınız için MEFE Makina ile iletişime geçin.
