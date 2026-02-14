# Teleport
**Minimalist, Smart Directory Jumper for Linux.**

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Platform](https://img.shields.io/badge/platform-linux-green)
![Language](https://img.shields.io/badge/language-python3-yellow)

[English](#english) | [Türkçe](#türkçe)

---

<div id="english"></div>

## English

Stop typing `cd ../../../var/www/html`. Just **teleport** there.
Teleport learns your frequently visited directories and lets you jump to them instantly with fuzzy search.

### ✨ Features
- **Smart Jump:** `tp <query>` finds the best match.
- **Auto Scan:** `tp scan` automatically adds all subdirectories.
- **Interactive:** Select from a list if multiple matches found.
- **Aliases:** Save long commands (`tp save "npm run dev" -n start`).
- **Clean:** No background processes, just a simple database.
- **Bilingual:** Fully supports English and Turkish (`tp config --lang tr`).

### 📦 Installation (Universal Linux)

Works on Debian, Ubuntu, Arch, Fedora, etc.

```bash
chmod +x install.sh
./install.sh
```
*Restart your terminal after installation.*

### ⚡ Usage

| Command | Action | Example |
|---------|--------|---------|
| `tp` | Interactive Menu | `tp` |
| `tp <query>` | Jump to directory | `tp pro` -> `~/Projects` |
| `tp scan` | Auto-discover folders | `tp scan ~/Projects` |
| `tp add` | Add current directory | `tp add` |
| `tp save` | Save command alias | `tp save "ls -la" -n ll` |
| `tp list` | Show stats | `tp list` |
| `tp clean` | Clean history | `tp clean --all` |
| `tp config` | Change language | `tp config --lang tr` |

### ❌ Uninstall
```bash
# Debian/Ubuntu
sudo apt remove teleport-cli

# Other Distros (Arch/Fedora)
sudo rm -rf /opt/teleport-cli /usr/local/bin/tp
```

---

<div id="türkçe"></div>

## Türkçe

Uzun uzun `cd` yazmaya son. Sadece **ışınlanın**.
Teleport, sık kullandığınız klasörleri öğrenir ve sizi onlara en kısa yoldan ulaştırır.

### ✨ Özellikler
- **Akıllı Geçiş:** `tp <sorgu>` en iyi eşleşmeyi bulur.
- **Otomatik Tarama:** `tp scan` ile tüm alt klasörleri otomatik ekleyin.
- **Etkileşimli Menü:** Birden fazla sonuç varsa listeden seçtirir.
- **Takma Adlar:** Uzun komutları kaydedin (`tp save "npm run dev" -n baslat`).
- **Temiz:** Arka plan işlemi yok, sadece basit ve hızlı.
- **Çift Dil:** İngilizce ve Türkçe tam destek (`tp config --lang tr`).

### 📦 Kurulum (Tüm Linux Dağıtımları)

Debian, Ubuntu, Arch, Fedora vb. hepsinde çalışır.

```bash
chmod +x install.sh
./install.sh
```
*Kurulumdan sonra terminalinizi yeniden başlatın.*

### ⚡ Kullanım

| Komut | İşlev | Örnek |
|-------|-------|-------|
| `tp` | Etkileşimli Menü | `tp` |
| `tp <sorgu>` | Dizine Git | `tp bel` -> `~/Belgeler` |
| `tp scan` | Klasörleri Keşfet | `tp scan ~/Projelerim` |
| `tp add` | Dizini Ekle | `tp add` |
| `tp save` | Komut Kaydet | `tp save "ls -la" -n ll` |
| `tp list` | İstatistikler | `tp list` |
| `tp clean` | Temizlik Yap | `tp clean --all` |
| `tp config` | Dili Değiştir | `tp config --lang tr` |

### ❌ Kaldırma
```bash
# Debian/Ubuntu
sudo apt remove teleport-cli

# Diğer Dağıtımlar (Arch/Fedora)
sudo rm -rf /opt/teleport-cli /usr/local/bin/tp
```
