# DAB Timer App

A Python-based precision timer application for Android (via Pydroid3) designed to guide herbal extraction (“dabbing”) sessions through customizable preheat, heat-soak, and cool-down phases with audio and vibration alerts.

---

## Table of Contents

1. [Features](#features)  
2. [Demo](#demo)  
3. [Requirements](#requirements)  
4. [Installation](#installation)  
5. [Usage](#usage)  
6. [Project Structure](#project-structure)  
7. [Configuration](#configuration)  
8. [Roadmap](#roadmap)  
9. [Contributing](#contributing)  
10. [License](#license)  
11. [Contact](#contact)  

---

## Features

- **Phase Control:** Three distinct timers for Preheat, Heat-Soak, and Cool-Down.  
- **Custom Durations:** Adjust each phase from 0–60 s (Preheat), 0–30 s (Heat-Soak), and custom Cool-Down interval.  
- **Audio & Vibration Alerts:** Choose sound, vibration, or both at the end of each phase.  
- **Session Logging:** Automatically logs each session’s parameters and timestamps to a local JSON file.  
- **Dark Mode UI:** High-contrast interface optimized for low-light use.  

---

## Requirements

- **Android** device with Pydroid3 installed  
- **Python** 3.8+ (bundled with Pydroid3)  
- **pip** (for optional libraries)  

---

## Installation

1. **Clone the repo**  
   
   git clone https://github.com/YourUsername/dab-timer-app.git
   cd dab-timer-app
