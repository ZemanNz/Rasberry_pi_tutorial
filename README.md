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

Tato část ukazuje, jak zajistit, aby se SledovaniBarev spustil automaticky po startu Raspberry Pi.

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
   ExecStart=/home/pi/Desktop/SledovaniBarev/build/SledovaniBarev /dev/video0
   WorkingDirectory=/home/pi/Desktop/SledovaniBarev/build
   Restart=always
   User=pi

   [Install]
   WantedBy=multi-user.target
   ```

   * **ExecStart**: cesta ke spustitelnému souboru a argument (/dev/video0)
   * **WorkingDirectory**: adresář, kde služba běží
   * **Restart=always**: znovu spustí, pokud program spadne
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
3. Okamžité spuštění služby bez restartu:

   ```bash
   sudo systemctl start sledovani.service
   ```
4. Ověř stav služby:

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

---

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
