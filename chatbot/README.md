# ⚡ GroqChat

A lightning-fast AI chatbot powered by the [Groq](https://groq.com/) LPU inference engine. Beautiful dark-mode UI with real-time streaming responses.

![GroqChat Screenshot](https://img.shields.io/badge/Status-Live-brightgreen) ![License](https://img.shields.io/badge/License-MIT-blue) ![Tech](https://img.shields.io/badge/Stack-HTML%20%7C%20CSS%20%7C%20JS-orange)

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🚀 **Real-time Streaming** | Token-by-token response streaming via Groq's SSE API |
| 🧠 **Multi-Model Support** | Llama 3.3 70B, Llama 3.1 8B, Mixtral 8x7B, Gemma 2 9B |
| 💬 **Chat History** | Create, switch, and delete multiple conversations |
| 📝 **Markdown Rendering** | Headers, bold, italic, code blocks, lists, tables, blockquotes |
| 📋 **Code Copy** | One-click copy button on all code blocks |
| ⏹️ **Stop Generation** | Abort streaming responses mid-generation |
| 🌙 **Dark Mode** | Premium dark UI with orange-pink gradient accents |
| 📱 **Responsive** | Full mobile support with sidebar toggle |
| 🔒 **Privacy First** | API key stored in localStorage, never sent anywhere except Groq |
| ⌨️ **Keyboard Shortcuts** | `Enter` to send, `Shift+Enter` for newline, `Ctrl+Shift+N` for new chat |

---

## 📁 Project Structure

```
chatbot/
├── index.html                 # Main HTML structure
├── style.css                  # Design system & styles
├── app.js                     # Application logic & Groq API integration
├── task-complete-email.html   # Task completion email template
└── README.md                  # This file
```

---

## 🚀 Getting Started

### Prerequisites

- A **Groq API key** (free) — get one at [console.groq.com/keys](https://console.groq.com/keys)
- A local web server (or simply open `index.html` in a browser)

### Run Locally

**Option 1 — Using `npx serve`:**
```bash
npx serve . -l 3000
```
Then open [http://localhost:3000](http://localhost:3000).

**Option 2 — Using Python:**
```bash
python -m http.server 3000
```

**Option 3 — Direct:**

Just double-click `index.html` to open it in your browser.

### Usage

1. Open the app in your browser
2. Paste your Groq API key in the welcome modal
3. Select a model from the sidebar dropdown
4. Start chatting!

---

## 🧩 Supported Models

| Model | Speed | Context | Best For |
|-------|-------|---------|----------|
| **Llama 3.3 70B** | Fast | 128K | General purpose, highest quality |
| **Llama 3.1 8B** | Fastest | 128K | Quick responses, simple tasks |
| **Mixtral 8x7B** | Fast | 32K | Code, reasoning, multilingual |
| **Gemma 2 9B** | Fast | 8K | Concise answers, instruction following |

---

## 📧 Email Template

The project includes a **task completion email template** (`task-complete-email.html`) featuring:

- Gradient header banner with success icon
- Structured task details grid (name, assignee, priority, status, duration)
- Summary section with bullet points
- CTA button with gradient styling
- Dark mode support via `prefers-color-scheme`
- Fully responsive, compatible with all major email clients

---

## 🛠️ Tech Stack

- **HTML5** — Semantic structure
- **CSS3** — Custom properties, gradients, animations, glassmorphism
- **Vanilla JavaScript** — No frameworks or dependencies
- **Groq API** — OpenAI-compatible chat completions with SSE streaming

---

## ⚙️ Configuration

All configuration is done through the UI:

- **API Key** — Entered on first launch, stored in `localStorage`
- **Model** — Selectable from sidebar dropdown
- **Chat History** — Automatically saved to `localStorage`

To reset everything, clear your browser's local storage for the site.

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

<p align="center">
  Built with ❤️ and powered by <a href="https://groq.com">Groq</a>
</p>
