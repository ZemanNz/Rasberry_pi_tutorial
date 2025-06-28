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
