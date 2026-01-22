# HQCB – Formalismo mínimo consistente (acción, ecuaciones, puente LQG/LQC, bootstrap)

Autor: Oscar Fuentes Fernández (2026)  
Licencia del repo: AGPL-3.0-or-later

## 1) Idea HQCB (enunciado técnico breve)

HQCB postula que el Higgs (v_eff) no es estrictamente constante a escala cosmológica: evoluciona lentamente por un proceso de *bootstrap* auto-consistente con la geometría cuántica discreta (grafo tipo LQG) a escala de Planck. Esa evolución induce un corrimiento efectivo en inferencias cosmológicas (CMB/BAO) y puede aliviar la Tensión de Hubble, generando predicciones falsables.

## 2) Acción efectiva (escalar–tensor, marco de Jordan)

Definimos un grado efectivo escalar \(h(x)\) que parametriza \(v_{\rm eff}\), con acoplo no mínimo a curvatura:

\[
F(h)=M_{\rm Pl}^2+\xi h^2,\qquad
S=\int d^4x\sqrt{-g}\left[\frac{1}{2}F(h)R-\frac{1}{2}(\nabla h)^2-V(h)-\Lambda_0\right]+S_m[g,\psi].
\]

Un potencial mínimo (modelo base):

\[
V(h)=\frac{\lambda}{4}(h^2-v_0^2)^2+\Delta V(h),
\]

donde \(\Delta V(h)\) representa correcciones efectivas (renormalización/sector cuántico/cierre HQCB).

## 3) Ecuaciones de campo (covariantes)

Variación en \(g_{\mu\nu}\):

\[
F(h)G_{\mu\nu}=T^{(m)}_{\mu\nu}+T^{(h)}_{\mu\nu}+\nabla_\mu\nabla_\nu F-g_{\mu\nu}\Box F-g_{\mu\nu}\big(V+\Lambda_0\big),
\]

con

\[
T^{(h)}_{\mu\nu}=\nabla_\mu h\nabla_\nu h-\frac{1}{2}g_{\mu\nu}(\nabla h)^2.
\]

Variación en \(h\):

\[
\Box h - V'(h) + \frac{1}{2}F'(h)R=0,\qquad F'(h)=2\xi h.
\]

## 4) Especialización FLRW (cosmología)

Para \(ds^2=-dt^2+a^2(t)d\vec{x}^2\), \(H=\dot a/a\), \(R=6(2H^2+\dot H)\). Un conjunto útil:

\[
3FH^2=\rho_m+\frac{1}{2}\dot h^2+V+\Lambda_0-3H\dot F,
\]

\[
-2F\dot H=(\rho_m+p_m)+\dot h^2+\ddot F-H\dot F,
\]

\[
\ddot h+3H\dot h+V'(h)-\xi h R=0.
\]

## 5) Puente con LQG (operadores, grafo, semiclasicalidad)

En LQG la geometría se cuantiza sobre un grafo (spin network) con operadores de área y volumen. En el sector homogéneo/isótropo, el límite efectivo estándar se implementa como LQC (holonomías):

\[
b \mapsto \frac{\sin(\lambda b)}{\lambda},
\]

donde \(\lambda\) proviene del *area gap* (discreción de LQG). El Friedmann efectivo típico queda:

\[
H^2=\frac{\rho_{\rm eff}}{3F(h)}\left(1-\frac{\rho_{\rm eff}}{\rho_c(h)}\right),
\qquad
\rho_c(h)=\frac{3F(h)}{8\pi G\,\gamma^2\,\lambda^2}.
\]

Así, la discreción (grafo) entra vía \(\lambda\) y el Higgs vía \(F(h)\).

## 6) Cierre “bootstrap” HQCB (auto-consistencia)

Se formula como condición de estacionariedad de un potencial efectivo dependiente de curvatura/discreción:

\[
V_{\rm eff}(h;R,\lambda)=V(h)+\frac{1}{2}\xi h^2 R+\Delta V_q(h,R)+\Delta V_{\rm LQG}(h;\lambda),
\]

\[
\frac{\partial V_{\rm eff}}{\partial h}=0.
\]

Como \(R\) depende de \(H,\dot H\) y éstos dependen de \(F(h)\) y \(\rho_{\rm eff}\), se obtiene el ciclo auto-consistente:

\[
h \rightarrow F(h)\rightarrow H(t)\rightarrow R(t)\rightarrow h.
\]

## 7) Predicciones falsables y pipeline de inferencia (resumen)

Observables típicos: \(H(z)\), \(D_M(z)/r_d\), \(D_H(z)/r_d\), \(D_V(z)/r_d\), parámetros comprimidos de CMB, y tensiones con \(H_0\) local.

Likelihood gaussiana estándar:

\[
\ln \mathcal{L}(\theta)= -\frac{1}{2}(d-m(\theta))^T C^{-1}(d-m(\theta))+\text{const}.
\]

Comparación con competidores vía evidencia (nested sampling) o criterios (AIC/BIC) contra \(\Lambda\)CDM, wCDM, EDE, escalar–tensor genérico.

---

Este documento define el “núcleo HQCB” que el repo debe reflejar: ecuaciones (acción), puente a discreción LQG/LQC y cierre bootstrap.