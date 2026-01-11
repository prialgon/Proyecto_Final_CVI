<div align="center">

# Proyecto Final de Visión por Ordenador I

Este repositorio contiene el **Proyecto Final de Visión por Ordenador I**.  


[![Python](https://img.shields.io/badge/Python-3.x-blue.svg)](https://www.python.org/)
[![OpenCV](https://img.shields.io/badge/OpenCV-4.x-green.svg)](https://opencv.org/)
[![Status](https://img.shields.io/badge/Status-Completed-success.svg)](https://github.com/prialgon/Proyecto_Final_CVI)

## 👥 Autores

**Álvaro Pérez Ortega** - [@Coolgolf1](https://github.com/Coolgolf1)  
**Alberto Prieto González** - [@prialgon](https://github.com/prialgon)

</div>

---

## 🚀 Descripción del Proyecto

### 1. 🔐 Sistema de Seguridad

Antes de acceder al juego, el usuario debe validar su identidad mediante una secuencia de figuras geométricas coloreadas.

* **Detección:** Basada en segmentación de color y aproximación de polígonos.
* **Secuencia:** Cuadrado -> Triángulo -> Hexágono -> Pentágono.

### 2. 🖐️ Selección de Jugadores

Interfaz gestual para elegir el modo de juego sin necesidad de teclado o ratón.

* **Técnica:** Sustracción de fondo (MOG2) y detección de centroides para rastrear la posición de la mano.

### 3. 🏓 Pong

* **Modo 1 PvE:** Juega contra un sistema automático. La plataforma del jugador se controla mediante **KCF Tracking**.
* **Modo 2 PvP:** Juego entre dos sistemas con el mismo sistema de tracking.

---

## 📂 Estructura del Repositorio

```text
Proyecto_Final_CVI/
├── 📁 data/                              # Recursos generales
│   ├── 📷 calibration/                   # Imágenes del tablero de ajedrez
│   └── 🖼️ security_system_patterns/      # Assets de figuras
└── 📁 src/                               
    ├── ⚡ main.py
    ├── 🛡️ security_system/               # Sistema de seguridad
    ├── 🕹️ pong/                          # Código del juego
    ├── 🛠️ calibration/                   # Herramientas de calibración de cámara
    └── 📜 player_selection.py            # Selección del modo de juego
```

## 🛠️ Requisitos e Instalación

1. **Clonar el repositorio:**

   ```bash
   git clone https://github.com/prialgon/Proyecto_Final_CVI.git
   ```

2. **Instalar dependencias:**

   ```bash
   conda env create -f environment.yml
    conda activate <env-name>
   ```

3. **Ejecutar:**

   ```bash
   python src/main.py
   ```

---
<div align="center">

Universidad Pontificia Comillas - ICAI

3º de Grado en Ingeniería Matemática e Inteligencia Artificial
</div>