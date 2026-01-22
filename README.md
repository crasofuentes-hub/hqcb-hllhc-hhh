# HQCB-HL-LHC Higgs Self-Coupling Toolkit (κλ / λ_HHH)

**Autor:** Oscar Fuentes Fernández  
**Repositorio:** crasofuentes-hub/hqcb-hllhc-hhh  
**Licencia:** **GNU AGPL-3.0-or-later** (copyleft fuerte; uso en red requiere publicar modificaciones)  

Toolkit reproducible (código + config YAML + tests) para pronósticos tipo **Asimov** del acoplamiento propio del Higgs en **HL-LHC (14 TeV)**, usando un modelo minimalista y verificable:

- Parametrización cuadrática de la sección eficaz inclusiva **σ(gg→HH)** vs **κλ**
- Construcción de una **likelihood Gaussiana** sobre la tasa inclusiva (Asimov SM truth)
- Escaneo de **ΔNLL** y extracción de intervalos 68% y 95% en **κλ**
- Script de figuras para documentar el ajuste y el escaneo

> Nota: Este repositorio implementa un núcleo reproducible y explícito. No pretende reemplazar frameworks completos de HL-LHC; sirve como base verificable/extendible para estudios propios.

---

## 1. Motivación física (qué es κλ / λ_HHH)

La autointeracción trilineal del Higgs **λ_HHH** suele parametrizarse con:

`	ext
κλ ≡ λ_HHH / λ_HHH^SM

En este repo:
- Ajustamos (a,b,c) a partir de puntos tabulados en YAML (baseline HL-LHC).
- Definimos una likelihood Gaussiana sobre la tasa inclusiva, con **Asimov SM truth** (κλ=1).
- Extraemos intervalos resolviendo **ΔNLL ≤ ΔNLL_CL**.

---

## 2. Características

- Determinista y reproducible (YAML + código + tests)
- Instalación editable (src layout)
- CLI para correr el forecast
- Tests unitarios para verificar ajuste e intervalos
- Figuras: σ(κλ) y ΔNLL(κλ)

---

## 3. Estructura del repositorio

`	ext
src/hqcb_hhh/
  theory.py        # ajuste cuadrático σ(κλ)
  likelihood.py    # NLL Gaussiana + intervalos 1D
  io.py            # lectura de configuración YAML
  cli.py           # interfaz de línea de comandos
data/projections/
  hl_lhc_baseline.yaml
scripts/
  make_figures.py
tests/
  test_quadratic_fit.py
  test_asimov_interval.py

Verificación rápida:

`powershell
python -c "import hqcb_hhh; print('hqcb_hhh OK', hqcb_hhh.__version__)"
pytest

`powershell
python -m hqcb_hhh.cli asimov --config data/projections/hl_lhc_baseline.yaml

> Los números dependen del YAML baseline. Si cambias puntos o supuestos, cambian intervalos.

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
- sigma_points_fb: puntos (κλ, σ) en fb para ajustar la cuadrática
- scan: rango y granularidad del escaneo κλ
- intervals: umbrales de ΔNLL para 68% y 95% (1 parámetro)

Umbrales típicos (1 parámetro):
- 68%: ΔNLL = 0.5
- 95%: ΔNLL ≈ 1.92

---

## 9. Cómo extender (recomendado)

`	ext
1) Crear escenarios alternativos:
   - data/projections/hl_lhc_optimistic.yaml
   - data/projections/hl_lhc_conservative.yaml
2) Añadir más puntos y ajustar por mínimos cuadrados
3) Evolucionar a likelihood multi-bin y sistemáticos correlacionados
`"
& param([string]$s) $script:lines += $s  "
& param([string]$s) $script:lines += $s  

---

## 11. Citar

Ver CITATION.cff.

---

## 12. Licencia

Este proyecto está bajo **GNU Affero General Public License v3.0 or later (AGPL-3.0-or-later)**. Ver LICENSE.

---

## 13. Autoría

Copyright (c) 2026 **Oscar Fuentes Fernández**.
