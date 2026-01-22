# Paper HQCB (LaTeX)

Este directorio contiene un esqueleto de paper en formato LaTeX:

- `paper/main.tex`
- `paper/sections/*.tex`
- `paper/bib/references.bib`
- `paper/figures/` (figuras copiadas desde `docs/figures/`)

## Figuras reproducibles
Ejecuta:
- `python scripts/make_paper_figures.py`

Esto regenerará figuras en `docs/figures/` y copiará un subconjunto a `paper/figures/`.

## Compilación
Recomendado:
- Subir `paper/` a Overleaf, o
- Compilar localmente con una distribución TeX (latexmk)

Nota: el CI NO compila LaTeX para evitar dependencias pesadas en runners; valida que el paper y las figuras existan y se regeneren.