# Teleport

**Minimalist, Smart Directory Jumper for Linux.**  
**Linux için Minimalist ve Akıllı Dizin Gezgini.**

[![Version](https://img.shields.io/badge/version-v1.0.0-blue?style=flat-square)](https://github.com/huseyinacikgoz/teleport-cli/releases)
[![Platform](https://img.shields.io/badge/platform-linux-green?style=flat-square)](https://www.linux.org/)
[![Language](https://img.shields.io/badge/language-python3-yellow?style=flat-square)](https://www.python.org/)

<!-- Language Selection -->
<p align="center">
  <a href="#english">
    <img src="https://img.shields.io/badge/Lang-English-blue?style=for-the-badge" alt="English">
  </a>
  <a href="#türkçe">
    <img src="https://img.shields.io/badge/Dil-Türkçe-red?style=for-the-badge" alt="Türkçe">
  </a>
</p>

---

<div id="english"></div>

## 🇬🇧 English

Stop typing `cd ../../../var/www/html`. Just **teleport** there.  
Teleport learns your frequently visited directories and lets you jump to them instantly with fuzzy search.

### ✨ Features
- **Smart Jump:** `tp <query>` finds the best match instantly.
- **Auto Scan:** `tp scan` automatically discovers subdirectories.
- **Interactive Menu:** Navigate through matches with arrow keys.
- **Aliases:** Save long commands (`tp save "npm run dev" -n start`).
- **Clean:** No background monitoring, just a simple SQLite database.
- **Bilingual:** Fully supports English and Turkish (`tp config --lang tr`).

### 📦 Installation

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
| `tp backup` | Backup Database | `tp backup ~/tp.bak` |
| `tp restore` | Restore Database | `tp restore ~/tp.bak` |
| `tp config` | Change language | `tp config --lang tr` |

### ❌ Uninstall
```bash
# Debian/Ubuntu
sudo apt remove teleport-cli

# Other Distros
sudo rm -rf /opt/teleport-cli /usr/local/bin/tp
```

---

<div id="türkçe"></div>

## 🇹🇷 Türkçe

Uzun uzun `cd` yazmaya son. Sadece **ışınlanın**.  
Teleport, sık kullandığınız klasörleri öğrenir ve sizi onlara en kısa yoldan, akıllıca ulaştırır.

### ✨ Özellikler
- **Akıllı Geçiş:** `tp <sorgu>` en iyi eşleşmeyi anında bulur.
- **Otomatik Tarama:** `tp scan` ile tüm alt klasörleri tek komutla ekleyin.
- **Etkileşimli Menü:** Birden fazla sonuç varsa ok tuşlarıyla seçin.
- **Takma Adlar:** Uzun komutları kaydedin (`tp save "npm run dev" -n baslat`).
- **Temiz:** Arka plan işlemi yok, sadece basit ve hızlı.
- **Çift Dil:** İngilizce ve Türkçe tam destek (`tp config --lang tr`).

### 📦 Kurulum

Debian, Ubuntu, Arch, Fedora vb. tüm Linux dağıtımlarında çalışır.

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
| `tp backup` | Yedekle | `tp backup ~/tp.bak` |
| `tp restore` | Geri Yükle | `tp restore ~/tp.bak` |
| `tp config` | Dili Değiştir | `tp config --lang en` |

### ❌ Kaldırma
```bash
# Debian/Ubuntu
sudo apt remove teleport-cli

# Diğer Dağıtımlar
sudo rm -rf /opt/teleport-cli /usr/local/bin/tp
```
