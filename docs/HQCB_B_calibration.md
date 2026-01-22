# HQCB-B: La tensión de Hubble como “cambio de regla de medir” (no como nueva fuerza)

Autor: Oscar Fuentes Fernández (2026)  
Licencia: AGPL-3.0-or-later

## Idea (versión corta)
En HQCB-B el universo es una red (tipo LEGO) de grados de libertad de espacio-tiempo.  
El Higgs está acoplado a esa red, por lo que el valor efectivo del vacío del Higgs, v_eff, puede reajustarse muy lentamente con la expansión.

Eso NO se interpreta como “energía oscura que cambia”, sino como un efecto de *calibración*: si v_eff afecta escalas físicas tempranas (por ejemplo el “ruler” estándar r_d asociado a BAO/CMB), entonces las inferencias cosmológicas que asumen un ruler constante pueden sesgar H0.

Resultado: el H0 inferido desde el universo temprano (CMB/BAO) puede salir menor que el H0 local, aun si ambos son correctos dentro de su propia calibración.

## Modelo toy (mínimo)
- v_eff(z) = v0 * (1+z)^alpha, con alpha pequeño.
- r_d,true = r_d,0 * (v_eff(z_rec)/v0)^p
  (p controla “sensibilidad” de la escala estándar al Higgs efectivo).
- Si el análisis asume r_d,0 constante, el H0 inferido temprano queda sesgado:
  H0_inferido ≈ H0_local * (r_d,true / r_d,0)

Si r_d,true < r_d,0, entonces H0_inferido < H0_local, reproduciendo el patrón de la tensión de Hubble.

Este repo incluye:
- Script reproducible que ajusta alpha para igualar un objetivo H0 temprano.
- Figuras en docs/figures/
- Tests que validan coherencia básica (alpha=0 => no tensión).