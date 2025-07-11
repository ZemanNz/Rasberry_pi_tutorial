# Raspberry Pi 5 Wi-Fi Hotspot & SSH Access Setup

Tento návod popisuje krok za krokem, jak na Raspberry Pi 5 vytvořit automaticky spouštěný Wi-Fi hotspot pomocí NetworkManageru a jak se k němu připojit přes SSH.

Co to umí?

Raspberry Pi po startu automaticky vytvoří Wi-Fi Access Point (SSID Hostspot) a spustí DHCP/NAT.

Klient (notebook/telefon) se připojí k Hostspot a získá IP adresu z podsítě (10.42.0.x nebo 192.168.6.x).

SSH přístup do Pi přes ssh pi@<IP>, bez nutnosti přímého kabelového připojení.

Sdílení internetu: pokud je Pi připojeno k internetu přes Ethernet, nebo druhou Wi-Fi (např. USB dongle), klienti připojení na Hostspot mají internet.

Poznámka: Pi vestavěnou Wi-Fi (wlan0) nelze současně používat jako klient i AP – pro Wi-Fi uplink je nutný druhý adaptér.

## 1. Příprava systému

```bash
sudo apt update
sudo apt install -y network-manager openssh-server
```

* **NetworkManager** spravuje hotspot.
* **OpenSSH Server** umožní SSH přístup.

---

## 2. Vytvoření profilu hotspotu

```bash
sudo nmcli connection add \
  type wifi ifname wlan0 con-name Hostspot autoconnect yes ssid Hostspot
```

* `type wifi` – Wi-Fi připojení
* `ifname wlan0` – vestavěná Wi-Fi karta
* `con-name Hostspot` – interní název profilu
* `autoconnect yes` – spustí se po restartu
* `ssid Hostspot` – viditelné jméno sítě např: Pi_Bur_01
```bash
sudo nmcli connection add \
  type wifi ifname wlan0 con-name Pi_Bur_01 autoconnect yes ssid Pi_Bur_01
```
---

## 3. Přepnutí do režimu Access Point + NAT/DHCP

```bash
sudo nmcli connection modify Pi_Bur_01 \
  802-11-wireless.mode ap \
  802-11-wireless.band bg \
  ipv4.method shared
```

* `mode ap` – Access Point
* `band bg` – 2.4 GHz, režimy b/g
* `ipv4.method shared` – NAT + DHCP automaticky

---

## 4. Nastavení zabezpečení (WPA2‑PSK)

```bash
sudo nmcli connection modify Pi_Bur_01 wifi-sec.key-mgmt wpa-psk
sudo nmcli connection modify Pi_Bur_01 wifi-sec.psk "sokolska"
```

* `wifi-sec.key-mgmt wpa-psk` – WPA2‑Personal
* `wifi-sec.psk` – heslo (alespoň 8 znaků)

---

## 5. Aktivace hotspotu ihned

```bash
sudo nmcli connection up Hostspot
```

* AP začne vysílat a je připraven k použití.

---

## 7. Ověření a připojení klienta

1. Na zařízení (notebook/telefon) vyhledej síť **Pi_Bur_01**.
2. Připoj se heslem **sokolska**.
3. Na Linuxu ověř IP:

   ```bash
   ip addr show <tvé_wifi_iface> | grep inet
   ip route | grep default
   ```

   * Gateway je IP Raspberry Pi (např. `10.42.0.1` nebo `192.168.6.1`).

---

## 8. SSH přístup

```bash
 ssh pi@10.42.0.1
```

* Uživatel: `pi`
* Heslo: to, co máš pro `pi` (výchozí `raspberry` nebo své vlastní).

---

## 9. Autostart po rebootu

Díky `autoconnect yes` a `mode ap` se po každém restartu Raspberry Pi:

1. `wlan0` přepne do AP módu
2. spustí NAT a DHCP
3. začne vysílat **Hostspot**


## Tipy & rozšíření

* **Sdílení internetu**: připoj Pi k Ethernetu; NAT funguje automaticky.
* **Změna SSID/hesla**:

  ```bash
  sudo nmcli connection modify Hostspot 802-11-wireless.ssid "NewSSID"
  sudo nmcli connection modify Hostspot wifi-sec.psk "NewPassword123"
  sudo nmcli connection down Hostspot && sudo nmcli connection up Hostspot
  ```
* **Skrytá síť**:

  ```bash
  sudo nmcli connection modify Hostspot 802-11-wireless.hidden yes
  sudo nmcli connection down Hostspot && sudo nmcli connection up Hostspot
  ```

---

*Hotovo! Teď máš spolehlivý SSH přístup přes vlastní Wi‑Fi hotspot, který se automaticky spustí při startu.*






### Pokusy:
* Kdyz pripojite nejakou kameru napr go pro pomoci usb do rasberry, potom pomoci prikazu:
  ```bash
  sudo dmesg -w
  lsusb
  ```
* zjistite, jestli rasberry zachytilo kameru
* spusteni streamu z kamery na monitor:
```bash
  ffplay /dev/video0
  ```

# SledovaniBarev na Raspberry Pi 5

Tento README popisuje, jak na Raspberry Pi 5 spustit projekt **SledovaniBarev**, který zpracovává obraz z USB kamery nebo statického obrázku v C++, pomocí OpenCV.

## 📦 Předpoklady

* Raspberry Pi 5 s Raspberry Pi OS (Desktop nebo Lite + X server)
* SSH přístup k Pi (např. `ssh pi@10.42.0.1`)
* USB kamera v UVC režimu (viditelná jako `/dev/video0`)
* Projekt **SledovaniBarev** přenesený do `~/Desktop/SledovaniBarev`

## 1. Přenos projektu na Pi


### ) SCP (alternativa)

Na vašem notebooku:

```bash
scp -r ~/Plocha/PROGRAMING/C++/SledovaniBarev pi@10.42.0.1:/home/pi/Desktop/
```

---

## 2. Instalace závislostí

```bash
sudo apt update
sudo apt install -y build-essential cmake libopencv-dev
```

* **build-essential**: GCC, make
* **cmake**: build system
* **libopencv-dev**: hlavičky a knihovny OpenCV

---
-----------------------------------------------------------------------------------------------

## 3. Jednorázová kompilace bez CMake

1. Přejdi do složky projektu:

   ```bash
   cd ~/Desktop/SledovaniBarev
   ```
2. Sestav program příkazem:

   ```bash
   g++ main.cpp -o sledovani `pkg-config --cflags --libs opencv4`
   ```

   * `-o sledovani` vytvoří binárku `sledovani`
   * back-ticks spustí `pkg-config` pro nastavení OpenCV

---

## 4. Spuštění programu

> **Poznámka**: Pro zobrazení GUI na HDMI monitoru je nutné nastavit `DISPLAY`

1. Přejdi do projektu:

   ```bash
   cd ~/Desktop/SledovaniBarev
   ```
2. Nastav X display:

   ```bash
   export DISPLAY=:0
   ```
3. Spus sledování z USB kamery:

   ```bash
   ./sledovani /dev/video0
   ```
4. (Alternativa) Zpracování statického obrázku:

   ```bash
   ./sledovani vstup.jpg
   ```

---

## 5. CMake varianta (volitelné)

1. Vytvoř build adresář a přejdi do něj:

   ```bash
   cd ~/Desktop/SledovaniBarev
   mkdir -p build && cd build
   ```
2. Generuj a sestav:

   ```bash
   cmake ..
   make -j4
   ```
3. Spus program:

   ```bash
   export DISPLAY=:0
   ./SledovaniBarev /dev/video0
   ```

---

## 6. Rychlé připojení a spuštění z notebooku

```bash
ssh pi@10.42.0.1 \
'cd ~/Desktop/SledovaniBarev && \
 g++ main.cpp -o sledovani `pkg-config --cflags --libs opencv4` && \
 export DISPLAY=:0 && \
 ./sledovani /dev/video0'
```

---

-----------------------------------------------------------------------------------------------

## 7. Automatické spouštění po bootu (volitelné)

Tato část ukazuje, jak zajistit, aby se SledovaniBarev spustil automaticky po startu Raspberry Pi.

### 7.1. Vytvoření systemd jednotky

1. Otevři nový soubor jednotky v editoru Nano (nebo jiném):

   ```bash
   sudo nano /etc/systemd/system/sledovani.service
   ```

2. Vlož do něj následující obsah:

   ```ini
   [Unit]
   Description=SledovaniBarev service
   After=multi-user.target

   [Service]
   Environment=DISPLAY=:0
   StandardOutput=inherit
   StandardError=inherit
   ExecStartPre=/bin/sleep 30
   ExecStart=/home/pi/Desktop/SledovaniBarev/sledovani /dev/video0
   WorkingDirectory=/home/pi/Desktop/SledovaniBarev
   Restart=always
   User=pi

   [Install]
   WantedBy=multi-user.target
   ```

   * **Environment=DISPLAY=:0**: zajistí zobrazení okna OpenCV na připojeném monitoru
   * **ExecStartPre=/bin/sleep 30**: počká, až se grafické prostředí načte
   * **ExecStart**: cesta ke spustitelnému souboru `sledovani` a argument `/dev/video0`
   * **WorkingDirectory**: adresář, kde služba poběží
   * **Restart=always**: služba se restartuje, pokud spadne
   * **User=pi**: služba poběží pod uživatelem `pi`

3. Ulož změny:

   * Stiskni `Ctrl+O`, poté `Enter` pro potvrzení
   * Ukonči Nano s `Ctrl+X`

### 7.2. Aktivace a spuštění služby

1. Načti nové jednotky a aktualizuj systemd:

   ```bash
   sudo systemctl daemon-reload
   ```
2. Povolení automatického spouštění služby při bootu:

   ```bash
   sudo systemctl enable sledovani.service
   ```
   deaktivace :
  ```bash
   sudo systemctl disable sledovani.service
   ```
4. Okamžité spuštění služby bez restartu:

   ```bash
   sudo systemctl start sledovani.service
   ```
5. Ověř stav služby:

   ```bash
   sudo systemctl status sledovani.service
   ```

   * Měl bys vidět **Active: active (running)**

### 7.3. Zobrazení logů služby

Pro sledování výstupu služby (např. debug zpráv) použij:

```bash
sudo journalctl -u sledovani.service -f
```

* `-f` sleduje log v reálném čase
-------------------------------------------------------------

## 8. Opakovaný přenos a spuštění po úpravách

Když upravíš kód na **notebooku**, stačí spustit tyto příkazy, které přenesou nejnovější změny, přeloží program pro ARM architekturu na Pi a okamžitě ho spustí:

1. **Přenos souborů na Raspberry Pi**

   ```bash
   # Ze složky projektu na notebooku
   scp -r ~/Plocha/PROGRAMING/C++/SledovaniBarev/* \
     pi@10.42.0.1:/home/pi/Desktop/SledovaniBarev/
   ```

   * `-r` kopíruje celý obsah včetně podadresářů

2. **SSH do Pi a kompilace**

   ```bash
   ssh pi@10.42.0.1
   cd ~/Desktop/SledovaniBarev
   g++ main.cpp -o sledovani `pkg-config --cflags --libs opencv4`
   ```

   * Přihlásíš se do Pi a přeložíš `main.cpp` pro ARM64

3. **Spuštění programu s kamerou**

   ```bash
   export DISPLAY=:0
   ./sledovani /dev/video0
   ```

Hotovo! Po těchto krocích poběží nejnovější verze SledovaniBarev na Raspberry Pi 5 bez nutnosti manuálního mazání starých binárek.


## UART komunikace mezi Raspberry Pi 5 a ESP32

Tato sekce popisuje, jak propojit Raspberry Pi 5 a ESP32 pomocí UART (seriové linky), ukázku kódu na obou zařízeních a vysvětlení, co je potřeba nakonfigurovat.

---

### 1. Požadavky

* Raspberry Pi 5 s nainstalovaným Raspberry Pi OS
* ESP32 (Arduino Core nebo vestavěné UART2/Serial2 dostupné)
* Propojovací kabely (dupont)
* Společná zem (**GND**)

---

### 2. Hardwarové zapojení

```
Raspberry Pi 5 (40pin)       ESP32
------------------------       ----------------
GND (pin 6, 9, 14, ...)   →    GND
TX  (GPIO14, pin 8)       →    RX2 (např. GPIO16)
RX  (GPIO15, pin 10)      ←    TX2 (např. GPIO17)
```

> **Poznámka:** Obě zařízení používají logické úrovně 3.3 V, takže není potřeba žádný převodník napětí.

---

### 3. Konfigurace Raspberry Pi

1. Vypnutí sériové konzole (serial console), aby bylo UART čistě pro vaši aplikaci:

   ```bash
   sudo raspi-config
   # Interface Options → Serial Port
   # „Would you like a login shell over serial?“ → No
   # „Enable UART hardware?“ → Yes
   sudo reboot
   ```

2. Ověření dostupnosti UART:

   ```bash
   ls -l /dev/serial0
   # nebo
   dmesg | grep ttyAMA0
   ```

3. Příklad použití v Pythonu (pomocí pyserial):

   ```python
   import serial

   # Otevřeme UART (/dev/serial0 alias /dev/ttyAMA0) na 115200 baud
   ser = serial.Serial('/dev/serial0', 115200, timeout=1)
   ser.write(b'Ahoj ze Raspberry Pi!')
   data = ser.readline().decode('utf-8').strip()
   print(f"Přijaté: {data}")
   ser.close()
   ```

---

### 4. Konfigurace ESP32 (Arduino)

```cpp
#include <HardwareSerial.h>

// Použijeme Serial2: RX na GPIO16, TX na GPIO17
HardwareSerial Serial2(2);

void setup() {
  // Debug přes USB
  Serial.begin(115200);
  // UART2 na zvolených pinech
  Serial2.begin(115200, SERIAL_8N1, 16, 17);
  Serial.println("ESP32 UART2 připraven...");
}

void loop() {
  // Čteme ze sériové linky od Raspberry Pi
  if (Serial2.available()) {
    String msg = Serial2.readStringUntil('\n');
    Serial.print("Dostáno z Pi: ");
    Serial.println(msg);
    // Odeslání odpovědi: echo
    Serial2.println("Echo: " + msg);
  }
}
```

> **Poznámka:** Vyberte si volné piny pro RX2/TX2, v příkladu používáme GPIO16 a GPIO17.

---

### 5. Princip fungování

1. **Křížové propojení**: TX ↔ RX + společná GND.
2. **Logické úrovně**: obě strany 3.3 V → bezpečné propojení bez převodníků.
3. **Serial console** na Raspberry Pi se vypne, jinak by se UART používal systémem pro přihlášení a výpis bootovacích zpráv.
4. **Komunikační rychlost** (baudrate) musí být stejná na obou stranách (např. 115200 bd).
5. Aplikace si mohou vzájemně posílat data – viz ukázky kódu.

---

### 6. Tipy a doporučení

* Použijte `minicom` nebo `screen` pro rychlý test UART na Raspberry Pi:

  ```bash
  sudo apt install minicom
  minicom -b 115200 -D /dev/serial0
  ```
* Pro stabilnější linku se hodí zkombinovat **RC filtr** nebo **odporový dělič** při delších kabelech.

---

*Hotovo!* Teď už můžeš používat UART mezi Raspberry Pi 5 a ESP32 v libovolné vlastní aplikaci.


-------

### Kompletní průvodce tréninkem AI modelu

Tento README tě provede od úplného začátku až po nasazení vlastního YOLOv5 modelu na detekci červených, zelených, modrých kostek a červeného čtverce.

---

## 📁 Struktura projektu

```
projekt/
├── dataset/
│   ├── raw_images/           ← surové snímky z kamery (capture.py)
│   ├── images/
│   │   ├── train/            ← 80% obrázků (po splitu)
│   │   └── val/              ← 20% obrázků (po splitu)
│   └── labels/
│       ├── train/            ← YOLO anotace pro train
│       └── val/              ← YOLO anotace pro val
├── yolov5/                   ← klon YOLOv5 repozitáře
│   ├── data/
│   │   └── cubes.yaml        ← konfigurační YAML se cestami a třídami
│   ├── models/
│   ├── train.py
│   ├── detect.py
│   └── requirements.txt
├── capture.py                ← skript pro sběr snímků (F = uložení, Q = konec)
├── split.py                  ← skript na rozdělení raw_images → images/train, images/val
├── annotate.py               ← vlastní annotátor v OpenCV pro kreslení boxů
└── test.py                   ← ukázkový inference skript
```

---

## 🔧 1. Sběr snímků

Použij `capture.py`, které seskriptuje kameru a při stisku **F** uloží snímek do `dataset/raw_images/`.

```bash
# Ujisti se, že máš instalované OpenCV:
# pip install opencv-python

python3 capture.py --output dataset/raw_images
```

* **F**: uloží aktuální snímek jako `timestamp.jpg`
* **Q**: ukončí snímání

Nasnímej \~800–1000 snímků, kombinuj scény s více objekty (červená, zelená, modrá kostka + červený čtverec).

---

## 🔀 2. Rozdělení na train / val

Po nasbírání spusť `split.py`, který náhodně provede 80/20 rozdělení.

```bash
python3 split.py
```

Po úspěchu budeš mít:

```
dataset/images/train/ ─ 80% všech .jpg
dataset/images/val/   ─ 20% všech .jpg
```

---

## ✍️ 3. Anotace obrázků

Spusť `annotate.py` pro offline kreslení bounding boxů a uložení YOLO `.txt` anotací.

```bash
python3 annotate.py
```

**Ovládání:**

* **R/G/B/Z**: volba třídy (`cube_red`, `cube_green`, `cube_blue`, `zone_red`)
* **Levý tlačítko**: začít a táhnout box
* **S**: uložit `.txt` a přejít na další obrázek
* **N**: přejít na další bez uložení
* **P**: předchozí obrázek
* **Q**: ukončit

Výsledkem budou soubory:

```
dataset/labels/train/img_XXX.txt
dataset/labels/val/img_YYY.txt
```

Každý `.txt` může obsahovat více řádků: `<class_id> <x_c> <y_c> <w> <h>` (yolo-normalizované).

---

## 📦 4. Příprava YOLOv5

### A) Klon repozitáře

```bash
git clone https://github.com/ultralytics/yolov5.git
cd yolov5
```

### B) Instalace závislostí (obejdi "externally-managed")

```bash
pip install --break-system-packages -r requirements.txt
```

> **Poznámka:** Pokud nechceš riskovat, můžeš použít:
>
> ```bash
> python3 -m venv venv
> source venv/bin/activate
> pip install -r requirements.txt
> ```

---

## ⚙️ 5. Konfigurace datasetu

Vytvoř `yolov5/data/cubes.yaml` s obsahem:

```yaml
train: ../dataset/images/train
val:   ../dataset/images/val

nc: 4
names: ['cube_red','cube_green','cube_blue','zone_red']
```

---

## 🚀 6. Trénink modelu

Spusť trénink YOLOv5n (nano) s předtrénovanými váhami:

```bash
python3 train.py \
  --img 640 \
  --batch 16 \
  --epochs 100 \
  --data data/cubes.yaml \
  --cfg models/yolov5n.yaml \
  --weights yolov5n.pt \
  --name cubes-exp1
```

Po skončení najdeš výsledky v:

```
yolov5/runs/train/cubes-exp1/
  ├─ weights/best.pt
  ├─ weights/last.pt
  └─ results.png
```

### Pokračování tréninku (resume)

```bash
python3 train.py --resume runs/train/cubes-exp1 --exist-ok
```

---

## 🎯 7. Inference / Detekce

### A) Test na validačních obrázcích

```bash
python3 detect.py \
  --weights runs/train/cubes-exp1/weights/best.pt \
  --source ../dataset/images/val \
  --conf 0.4 \
  --save-txt \
  --project detect-test
```

### B) Real-time z kamery

```bash
python3 detect.py \
  --weights runs/train/cubes-exp1/weights/best.pt \
  --source 0 \
  --conf 0.4 \
  --view-img
```

Pro vlastní skript `test.py` s importem přes `torch.hub`:

```python
model = torch.hub.load('ultralytics/yolov5', 'custom', path='runs/train/cubes-exp1/weights/best.pt')
```

---

## 💡 8. Tipy a doporučení

* **Augmentace**: v `hyp.scratch-low.yaml` povol rotace, změnu jasu a ořezy
* **Vyšší rozlišení**: pro malé objekty zvaž `--img 800` nebo `1024`
* **Early stopping**: přidej `--patience 30` pro automatické ukončení při stagnaci
* **Test na různé scény**: nasbírej více validačních obrázků z různých úhlů a světelných podmínek

---



