# HQCB-HL-LHC Higgs Self-Coupling Toolkit (ÎºÎ» / Î»_HHH)

## Formalismo HQCB (acciï¿½n + ecuaciones + puente LQG/LQC + bootstrap)

El formalismo mï¿½nimo consistente de la hipï¿½tesis HQCB (acciï¿½n, ecuaciones de campo, conexiï¿½n efectiva con LQG/LQC y cierre bootstrap) estï¿½ documentado aquÃ©:

- docs/HQCB_Formalism.md

[![CI](https://github.com/crasofuentes-hub/hqcb-hllhc-hhh/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/crasofuentes-hub/hqcb-hllhc-hhh/actions/workflows/ci.yml)

**Autor:** Oscar Fuentes FernÃ¡ndez  
**Repositorio:** crasofuentes-hub/hqcb-hllhc-hhh  
**Licencia:** **GNU AGPL-3.0-or-later** (copyleft fuerte; uso en red requiere publicar modificaciones)  

Toolkit reproducible (cÃ³digo + config YAML + tests) para pronÃ³sticos tipo **Asimov** del acoplamiento propio del Higgs en **HL-LHC (14 TeV)**, usando un modelo minimalista y verificable:

- ParametrizaciÃ³n cuadrÃ¡tica de la secciÃ³n eficaz inclusiva **Ïƒ(ggâ†’HH)** vs **ÎºÎ»**
- ConstrucciÃ³n de una **likelihood Gaussiana** sobre la tasa inclusiva (Asimov SM truth)
- Escaneo de **Î”NLL** y extracciÃ³n de intervalos 68% y 95% en **ÎºÎ»**
- Script de figuras para documentar el ajuste y el escaneo

> Nota: Este repositorio implementa un nÃºcleo reproducible y explÃ­cito. No pretende reemplazar frameworks completos de HL-LHC; sirve como base verificable/extendible para estudios propios.

---

## 1. MotivaciÃ³n fÃ­sica (quÃ© es ÎºÎ» / Î»_HHH)

La autointeracciÃ³n trilineal del Higgs **Î»_HHH** suele parametrizarse con:

`	ext
ÎºÎ» â‰¡ Î»_HHH / Î»_HHH^SM

En este repo:
- Ajustamos (a,b,c) a partir de puntos tabulados en YAML (baseline HL-LHC).
- Definimos una likelihood Gaussiana sobre la tasa inclusiva, con **Asimov SM truth** (ÎºÎ»=1).
- Extraemos intervalos resolviendo **Î”NLL â‰¤ Î”NLL_CL**.

---

## 2. CaracterÃ­sticas

- Determinista y reproducible (YAML + cÃ³digo + tests)
- InstalaciÃ³n editable (src layout)
- CLI para correr el forecast
- Tests unitarios para verificar ajuste e intervalos
- Figuras: Ïƒ(ÎºÎ») y Î”NLL(ÎºÎ»)

---

## 3. Estructura del repositorio

`	ext
src/hqcb_hhh/
  theory.py        # ajuste cuadrÃ¡tico Ïƒ(ÎºÎ»)
  likelihood.py    # NLL Gaussiana + intervalos 1D
  io.py            # lectura de configuraciÃ³n YAML
  cli.py           # interfaz de lÃ­nea de comandos
data/projections/
  hl_lhc_baseline.yaml
scripts/
  make_figures.py
tests/
  test_quadratic_fit.py
  test_asimov_interval.py

VerificaciÃ³n rÃ¡pida:

`powershell
python -c "import hqcb_hhh; print('hqcb_hhh OK', hqcb_hhh.__version__)"
pytest

`powershell
python -m hqcb_hhh.cli asimov --config data/projections/hl_lhc_baseline.yaml

> Los nÃºmeros dependen del YAML baseline. Si cambias puntos o supuestos, cambian intervalos.

---

## 7. Figuras (PowerShell)

Genera dos figuras:
- docs/figures/sigma_vs_kappa.png"
& param([string]$s) $script:lines += $s  

`powershell
python scripts/make_figures.py --config data/projections/hl_lhc_baseline.yaml
dir .\docs\figures
`"
& param([string]$s) $script:lines += $s  "
& param([string]$s) $script:lines += $s  

Campos clave:
- ssumptions.rel_uncert_rate: incertidumbre relativa (gaussiana) sobre la tasa inclusiva
- sigma_points_fb: puntos (ÎºÎ», Ïƒ) en fb para ajustar la cuadrÃ¡tica
- scan: rango y granularidad del escaneo ÎºÎ»
- intervals: umbrales de Î”NLL para 68% y 95% (1 parÃ¡metro)

Umbrales tÃ­picos (1 parÃ¡metro):
- 68%: Î”NLL = 0.5
- 95%: Î”NLL â‰ˆ 1.92

---

## 9. CÃ³mo extender (recomendado)

`	ext
1) Crear escenarios alternativos:
   - data/projections/hl_lhc_optimistic.yaml
   - data/projections/hl_lhc_conservative.yaml
2) AÃ±adir mÃ¡s puntos y ajustar por mÃ­nimos cuadrados
3) Evolucionar a likelihood multi-bin y sistemÃ¡ticos correlacionados
`"
& param([string]$s) $script:lines += $s  "
& param([string]$s) $script:lines += $s  

---

## 11. Citar

Ver CITATION.cff.

---

## 12. Licencia

Este proyecto estÃ¡ bajo **GNU Affero General Public License v3.0 or later (AGPL-3.0-or-later)**. Ver LICENSE.

---

## 13. AutorÃ­a

Copyright (c) 2026 **Oscar Fuentes FernÃ¡ndez**.
