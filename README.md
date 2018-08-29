# varmilik

Mal varlıklarınızı kontrol etmek için bir betik.

## Yükleme

* Kodu bilgisayarınıza indirin
```bash
git clone https://github.com/molcay/varmilik.git
```

* Yeni bir sanal ortam(virtual environment, `venv`) oluşturun
```bash
python3 -m venv myvenv
```

* Sanal ortamı aktifleştirin
```bash
source myvenv/bin/activate
```

* Bağımlılıkları(dependencies) yükleyiniz
```bash
pip install -r requirements.txt
```

* `data.json` isimli bir dosya oluşturun.
Bu dosya mal varlıklarını içermeli ve aşağıdaki gibi bir yapıya sahip olmalıdır.
```json
{
    "USD": {
      "amount": 22.55,
      "price": 100,
      "unit_price": 4.43
    }
}
```
> amount => Alınan ya da satılan döviz miktarı

> price =>
- `amount` kısmında belirtiğiniz miktarda dövizi alabilmek için ödenen miktar(TL olarak)
- `amount` kısmında belirtiğiniz miktarda dövizi satınca elde ettiğiniz miktar(TL olarak)

> unit_price => işlem kuru

> Satınalma işlemlerini negatif sayılarla ifade edebilirsiniz. `amount` ve `price` olarak negatif sayı grimeniz gereklidir.

  - Sample:
  ```json
  {
      "GOLD": [
        {
          "amount": 0.75,
          "price": 139.42,
          "unit_price": 185.89
        }
      ],
      "USD": [
        {
          "amount": 22.55,
          "price": 100,
          "unit_price": 4.43
        }
      ],
      "EUR": [
        {
          "amount": 150,
          "price": 815.5,
          "unit_price": 5.44
        },
        {
          "amount": -100,
          "price": -688.79,
          "unit_price": 6.887858
        }
      ]
  }
  ```

## Kullanım:

```
varmilik run [-f <file_path>]
varmilik watch [-f <file_path>] -t SECONDS [-s|-m|-h|-d]

Options:
  -f, --file <file_path>   Mal varlıklarınızı içeren dosyayı belirtmek için kullanılır [default: data.json].
  -t, --time SECONDS       Bekleme periyodu belirtmek için kullanılır.
  -s, --second             Bekleme periyodu zaman birimini saniye olarak seçer [default: True].
  -m, --minute             Bekleme periyodu zaman birimini dakika olarak seçer.
  -h, --hour               Bekleme periyodu zaman birimini saat olarak seçer.
  -d, --day                Bekleme periyodu zaman birimini gün olarak seçer.
```

### Örnekler

* Tek seferlik sonuç görmek için
```bash
./varmilik.py run
```

* 150 saniyelik aralıklarla mal varlıklarınızı kontrol etmek için
```bash
./varmilik.py watch -t 150
```

* 10 dakikalık aralıklarla mal varlıklarınızı kontrol etmek için
```bash
./varmilik.py watch -t 10 -m
```
