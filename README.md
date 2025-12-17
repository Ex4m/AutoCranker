# AppCranker (AppScheduler)

Jednoduchý nástroj pro automatizované spouštění aplikací v pravidelných intervalech s inteligentní kontrolou běžících procesů.

## Funkce

*   **Plánovač**: Spouští zvolenou aplikaci (EXE, skript) v nastavených intervalech (minuty/hodiny).
*   **Inteligentní blokování**: Před spuštěním zkontroluje, zda již neběží instance procesu.
    *   Pokud běží proces, který **obsahuje** definovaná klíčová slova (např. v argumentech příkazového řádku), spuštění se odloží.
*   **Podpora interpretů**: Možnost spouštět skripty (Perl, Python, atd.) specifikováním interpretu.
*   **GUI Konfigurace**: Uživatelsky přívětivé nastavení pomocí `CrankerSettings.py`.

## Instalace

1.  Ujistěte se, že máte nainstalovaný **Python 3**.
2.  Nainstalujte potřebné knihovny:
    ```bash
    pip install -r requirements.txt
    ```

## Použití

### 1. Konfigurace
Spusťte `CrankerSettings.py`.
*   **Cesta k aplikaci**: Vyberte soubor, který chcete spouštět.
*   **Interpret (nepovinné)**: Pokud spouštíte skript (např. `.pl`), zadejte `perl`. Pro `.py` zadejte `python`. Pro `.exe` nechte prázdné.
*   **Interval**: Jak často se má aplikace spouštět.
*   **Keywords**: Seznam klíčových slov. Pokud `runner` najde běžící proces, který má v názvu nebo argumentech některé z těchto slov, **nespustí** novou instanci.

### 2. Spuštění
Spusťte `autoCranker.bat`.
*   Otevře se okno příkazového řádku, které bude v smyčce kontrolovat čas a procesy.
*   Nechte toto okno otevřené (nebo minimalizované) pro běh na pozadí.

## Struktura projektu

*   `CrankerSettings.py` - Grafické rozhraní pro nastavení.
*   `autoCranker.bat` - Spouštěcí skript pro plánovač.
*   `dependencies/`
    *   `runner.py` - Hlavní logika smyčky a kontroly procesů.
    *   `settings.json` - Uložená konfigurace.
