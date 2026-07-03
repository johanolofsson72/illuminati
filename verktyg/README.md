# Byggverktyg — PDF-export

Skript för att bygga hela kunskapsbasen till en enda PDF
([`../Illuminatiorden-kunskapsbas.pdf`](../Illuminatiorden-kunskapsbas.pdf)).

## Krav

- [`pandoc`](https://pandoc.org/)
- [`weasyprint`](https://weasyprint.org/) (Python-paket; ger unicode- och bildstöd utan LaTeX)

```sh
brew install pandoc
pipx install weasyprint      # eller: pip install weasyprint
```

## Kör

Från repo-roten:

```sh
python3 verktyg/build_pdf.py
```

Skriptet:

1. slår ihop alla dokument i läsordning (se `ORDER` i skriptet),
2. konverterar interna `[[wikilänkar]]` till läsbara `»referenser«`,
3. gör bildsökvägarna absoluta,
4. renderar via `pandoc → weasyprint` med stilmallen [`style.css`](style.css).

Resultatet hamnar i repo-roten som `Illuminatiorden-kunskapsbas.pdf`.

## Filer

| Fil | Roll |
|-----|------|
| `build_pdf.py` | Bygg­skriptet |
| `style.css` | Typografi, sidnummer, sidbrytning per dokument, citatblock |
| `combined.md` | *Genereras* av skriptet (ignoreras av git) |

> **Not:** `style.css` använder `weasyprint`-kompatibel CSS (`@page`-regler för sidnummer och sidhuvud). LaTeX behövs inte.
