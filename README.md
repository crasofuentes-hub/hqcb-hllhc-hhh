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

κλ ≡ λ_HHH / λ_HHH^SM

En muchos estudios se modela el impacto de κλ en la producción **gg→HH** mediante una aproximación cuadrática:

σ(κλ) ≈ a·κλ² + b·κλ + c

En este repo:
- Ajustamos (a,b,c) a partir de 3 puntos tabulados en YAML (baseline HL-LHC).
- Definimos una likelihood Gaussiana sobre la tasa inclusiva, con Asimov SM truth (κλ=1).
- Extraemos intervalos resolviendo ΔNLL ≤ ΔNLL_CL.

---

## 2. Características

- Determinista y reproducible (YAML + código + tests)
- Instalación editable (src layout)
- CLI para correr el forecast
- Tests unitarios para verificar ajuste e intervalos
- Figuras: σ(κλ) y ΔNLL(κλ)

---

## 3. Estructura del repositorio

- src/hqcb_hhh/
  - theory.py — ajuste cuadrático σ(κλ)
  - likelihood.py — NLL Gaussiana + intervalos 1D
  - io.py — lectura de configuración YAML
  - cli.py — interfaz de línea de comandos
- data/projections/
  - hl_lhc_baseline.yaml — escenario baseline (puntos de σ y supuestos)
- scripts/
  - make_figures.py — genera figuras en docs/figures/
- tests/
  - pruebas unitarias reproducibles
- .github/workflows/ (opcional)
  - CI en Windows para pytest + smoke test del CLI

---

## 4. Requisitos

- Python ≥ 3.10

---

## 5. Instalación (PowerShell)

Desde el directorio del repo:

python -m pip install -U pip  
python -m pip install -e .  
python -m pip install -e ".[dev]"

Verificación rápida:

python -c "import hqcb_hhh; print('hqcb_hhh OK', hqcb_hhh.__version__)"  
pytest

---

## 6. Uso (PowerShell)

### 6.1 Forecast Asimov (SM truth)

python -m hqcb_hhh.cli asimov --config data/projections/hl_lhc_baseline.yaml

Salida esperada (ejemplo):

=== HQCB-HL-LHC κλ forecast (Asimov, SM truth) ===  
Author: Oscar Fuentes Fernández  
Config: data/projections/hl_lhc_baseline.yaml  
Quadratic fit: a=0.43, b=-28.44, c=71.01  
sigma_SM(k=1): 43.0000 fb  
rel_uncert_rate: 0.300 -> sigma_err=12.9000 fb  
68% interval (ΔNLL=0.5): [0.540, 1.470]  
95% interval (ΔNLL=1.92): [0.100, 1.930]

> Los números dependen del YAML baseline. Si cambias puntos o supuestos, cambian intervalos.

---

## 7. Figuras (PowerShell)

Genera:
- docs/figures/sigma_vs_kappa.png
- docs/figures/deltaNLL_scan.png

python scripts/make_figures.py --config data/projections/hl_lhc_baseline.yaml  
dir .\docs\figures

---

## 8. Configuración: data/projections/hl_lhc_baseline.yaml

Campos clave:
- assumptions.rel_uncert_rate: incertidumbre relativa (gaussiana) sobre la tasa inclusiva (baseline: 0.30)
- sigma_points_fb: puntos (κλ, σ) en fb para ajustar la cuadrática
- scan: rango y granularidad del escaneo κλ
- intervals: umbrales de ΔNLL para 68% y 95% (1 parámetro)

Umbrales típicos (1 parámetro):
- 68%: ΔNLL = 0.5
- 95%: ΔNLL ≈ 1.92

---

## 9. Cómo extender (recomendado)

- Crear escenarios alternativos:
  - hl_lhc_optimistic.yaml (menor incertidumbre)
  - hl_lhc_conservative.yaml (mayor incertidumbre)
- Añadir más puntos y ajustar por mínimos cuadrados (ya soportado por el fitter con >3 puntos)
- Evolucionar a likelihood multi-bin y sistemáticos correlacionados

---

## 10. Reproducibilidad y calidad

pytest asegura:
- el ajuste reproduce exactamente los puntos de entrada
- el intervalo 95% se reduce cuando disminuye la incertidumbre

---

## 11. Citar

Ver CITATION.cff.

---

## 12. Licencia

GNU Affero General Public License v3.0 or later (AGPL-3.0-or-later). Ver LICENSE.

---

## 13. Autoría

Copyright (c) 2026 Oscar Fuentes Fernández.