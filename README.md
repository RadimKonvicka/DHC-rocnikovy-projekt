# DHC Records Vault - Ročníkový projekt

Webová aplikace v Django pro správu a synchronizaci hudebního archivu se zaměřením na domácí undergroundovou a DHC scénu. Projekt kombinuje lokální databázi alb s real-time daty z externího Spotify API.

## Funkcionalita

* **Evidence interpretů a alb:** Kompletní CRUD správa interpretů, žánrů a konkrétních releasů (alb/singlů) přes administraci.
* **Propojení se Spotify API:** Možnost autentizace uživatele přes OAuth2.0 přímo na hlavním panelu. Po přihlášení aplikace porovnává hudební vkus uživatele s lokální databází a počítá shodu.
* **Real-time Global Releases:** Dynamické stahování nejnovějších globálních releasů ze serverů Spotify v reálném čase.
* **Responzivní UI:** Temný design přizpůsobený pro přehledné zobrazení statistik a hudebních žebříčků.

---

## Použité technologie
* **Backend:** Python 3.12+, Django Framework 6.0+
* **Databáze:** SQLite3
* **API:** Spotify Web API (Authorization Code Flow)
* **Frontend:** HTML5, CSS3 (Custom styling přímo v šablonách)

---

## Kompletní postup pro spuštění (Krok za krokem)

Pokud si projekt stahujete poprvé (např. jako ZIP z GitHubu), je potřeba inicializovat prostředí a připravit čistou databázi. Otevřete terminál ve složce projektu a postupujte podle těchto kroků:

### 1. Příprava virtuálního prostředí a závislostí
Nejdříve vytvořte a aktivujte virtuální prostředí, aby se balíčky neinstalovaly globálně do systému, a nainstalujte potřebné knihovny:

```powershell
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
