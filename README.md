# kindorf-bot-mvp
Modular Telegram bot MVP for the KINDORF international youth organization, featuring dynamic localization and user routing pipelines.
# KINDORF Bot MVP 🌍

A production-ready, modular Telegram automation tool developed for the **KINDORF International Youth Organization**. The system automates member onboarding, project proposals submission, and partnership routing using a dynamic JSON-driven localization architecture.

## ⚙️ Core Engineering Features
* **Modular Infrastructure:** Code architecture is separated into isolated semantic handling layers (`team`, `partner`, `project`, `common`) for scalable state management.
* **Dynamic JSON Localization Engine:** Interface text, onboarding flows, and multi-step question diagnostics are programmatically detached from the core backend logic into an independent `locales.json` pipeline, enabling instant multi-language remapping.
* **Persistent Cloud Infrastructure:** The codebase is fully deployed and hosted asynchronously under persistent runtime monitors on cloud infrastructure (**PythonAnywhere**), maintaining continuous 24/7 availability.

## 🛠️ System Architecture & Tech Stack
* **Language:** Python 3.10+
* **Framework:** PyTelegramBotAPI (Asynchronous Long Polling workflow)
* **Data Storage:** Structured JSON localization matrix
