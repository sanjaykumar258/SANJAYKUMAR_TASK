/* ========================================
   GroqChat — Application Logic
   ======================================== */

(() => {
  'use strict';

  // --- Constants ---
  const GROQ_API_URL = 'https://api.groq.com/openai/v1/chat/completions';
  const STORAGE_KEY_API = 'groqchat_api_key';
  const STORAGE_KEY_CHATS = 'groqchat_chats';
  const STORAGE_KEY_ACTIVE = 'groqchat_active_chat';

  const MODEL_NAMES = {
    'llama-3.3-70b-versatile': 'Llama 3.3 70B',
    'llama-3.1-8b-instant': 'Llama 3.1 8B',
    'mixtral-8x7b-32768': 'Mixtral 8x7B',
    'gemma2-9b-it': 'Gemma 2 9B',
  };

  const SYSTEM_PROMPT = `You are GroqChat, a helpful, friendly, and knowledgeable AI assistant. You provide clear, concise, and accurate answers. When writing code, use markdown code blocks with language identifiers. Format your responses with markdown for readability.`;

  // --- DOM Elements ---
  const $ = (sel) => document.querySelector(sel);
  const $$ = (sel) => document.querySelectorAll(sel);

  const els = {
    modal: $('#api-key-modal'),
    apiKeyInput: $('#api-key-input'),
    apiKeySubmit: $('#api-key-submit'),
    app: $('#app'),
    sidebar: $('#sidebar'),
    sidebarToggle: $('#sidebar-toggle'),
    newChatBtn: $('#new-chat-btn'),
    chatList: $('#chat-list'),
    modelSelect: $('#model-select'),
    headerModelName: $('#header-model-name'),
    clearKeyBtn: $('#clear-key-btn'),
    chatMessages: $('#chat-messages'),
    welcomeScreen: $('#welcome-screen'),
    chatForm: $('#chat-form'),
    chatInput: $('#chat-input'),
    sendBtn: $('#send-btn'),
    stopBtn: $('#stop-btn'),
  };

  // --- State ---
  let state = {
    apiKey: localStorage.getItem(STORAGE_KEY_API) || '',
    chats: [],
    activeChatId: null,
    isStreaming: false,
    abortController: null,
  };

  // --- Initialization ---
  function init() {
    loadChats();

    if (state.apiKey) {
      showApp();
    } else {
      showModal();
    }

    bindEvents();
  }

  // --- API Key Modal ---
  function showModal() {
    els.modal.classList.remove('hidden');
    els.app.classList.add('hidden');
    els.apiKeyInput.value = '';
    setTimeout(() => els.apiKeyInput.focus(), 300);
  }

  function showApp() {
    els.modal.classList.add('hidden');
    els.app.classList.remove('hidden');
    renderChatList();

    const activeId = localStorage.getItem(STORAGE_KEY_ACTIVE);
    if (activeId && state.chats.find(c => c.id === activeId)) {
      switchChat(activeId);
    } else if (state.chats.length > 0) {
      switchChat(state.chats[0].id);
    } else {
      createNewChat();
    }
  }

  function handleApiKeySubmit() {
    const key = els.apiKeyInput.value.trim();
    if (!key) {
      els.apiKeyInput.style.borderColor = '#ef4444';
      els.apiKeyInput.focus();
      return;
    }
    state.apiKey = key;
    localStorage.setItem(STORAGE_KEY_API, key);
    showApp();
  }

  // --- Chat Management ---
  function generateId() {
    return 'chat_' + Date.now() + '_' + Math.random().toString(36).substr(2, 6);
  }

  function createNewChat() {
    const chat = {
      id: generateId(),
      title: 'New Chat',
      messages: [],
      model: els.modelSelect.value,
      createdAt: Date.now(),
    };
    state.chats.unshift(chat);
    state.activeChatId = chat.id;
    saveChats();
    renderChatList();
    renderMessages();
    els.chatInput.focus();
  }

  function switchChat(id) {
    state.activeChatId = id;
    localStorage.setItem(STORAGE_KEY_ACTIVE, id);
    const chat = getActiveChat();
    if (chat) {
      els.modelSelect.value = chat.model;
      updateHeaderModel();
    }
    renderChatList();
    renderMessages();
  }

  function deleteChat(id) {
    state.chats = state.chats.filter(c => c.id !== id);
    if (state.activeChatId === id) {
      if (state.chats.length > 0) {
        switchChat(state.chats[0].id);
      } else {
        createNewChat();
      }
    }
    saveChats();
    renderChatList();
  }

  function getActiveChat() {
    return state.chats.find(c => c.id === state.activeChatId);
  }

  function saveChats() {
    localStorage.setItem(STORAGE_KEY_CHATS, JSON.stringify(state.chats));
    localStorage.setItem(STORAGE_KEY_ACTIVE, state.activeChatId);
  }

  function loadChats() {
    try {
      const data = localStorage.getItem(STORAGE_KEY_CHATS);
      state.chats = data ? JSON.parse(data) : [];
    } catch {
      state.chats = [];
    }
  }

  // --- Render ---
  function renderChatList() {
    els.chatList.innerHTML = '';
    state.chats.forEach(chat => {
      const item = document.createElement('div');
      item.className = 'chat-history-item' + (chat.id === state.activeChatId ? ' active' : '');
      item.innerHTML = `
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>
        <span>${escapeHtml(chat.title)}</span>
        <button class="delete-chat" data-id="${chat.id}" title="Delete chat">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
        </button>
      `;
      item.addEventListener('click', (e) => {
        if (e.target.closest('.delete-chat')) return;
        switchChat(chat.id);
        closeSidebar();
      });
      item.querySelector('.delete-chat').addEventListener('click', () => deleteChat(chat.id));
      els.chatList.appendChild(item);
    });
  }

  function renderMessages() {
    const chat = getActiveChat();
    els.chatMessages.innerHTML = '';

    if (!chat || chat.messages.length === 0) {
      els.chatMessages.appendChild(createWelcomeScreen());
      return;
    }

    chat.messages.forEach(msg => {
      els.chatMessages.appendChild(createMessageElement(msg.role, msg.content));
    });

    scrollToBottom();
  }

  function createWelcomeScreen() {
    const div = document.createElement('div');
    div.id = 'welcome-screen';
    div.className = 'welcome-screen';
    div.innerHTML = `
      <div class="welcome-glow"></div>
      <div class="welcome-icon">
        <svg width="56" height="56" viewBox="0 0 24 24" fill="none" stroke="url(#grad2)" stroke-width="1.2" stroke-linecap="round" stroke-linejoin="round">
          <defs><linearGradient id="grad2" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" style="stop-color:#f97316"/><stop offset="100%" style="stop-color:#ec4899"/></linearGradient></defs>
          <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>
        </svg>
      </div>
      <h1>How can I help you today?</h1>
      <p>Start a conversation with one of the fastest AI models available.</p>
      <div class="welcome-cards">
        <button class="welcome-card" data-prompt="Explain quantum computing in simple terms">
          <span class="card-icon">🧪</span><span>Explain quantum computing</span>
        </button>
        <button class="welcome-card" data-prompt="Write a Python function to find prime numbers">
          <span class="card-icon">💻</span><span>Write Python code</span>
        </button>
        <button class="welcome-card" data-prompt="What are the best practices for web security?">
          <span class="card-icon">🔒</span><span>Web security tips</span>
        </button>
        <button class="welcome-card" data-prompt="Help me plan a 7-day trip to Japan">
          <span class="card-icon">✈️</span><span>Plan a trip to Japan</span>
        </button>
      </div>
    `;
    div.querySelectorAll('.welcome-card').forEach(card => {
      card.addEventListener('click', () => {
        const prompt = card.dataset.prompt;
        els.chatInput.value = prompt;
        handleSend();
      });
    });
    return div;
  }

  function createMessageElement(role, content) {
    const div = document.createElement('div');
    div.className = `message ${role}`;
    const avatarLabel = role === 'user' ? 'U' : 'G';
    div.innerHTML = `
      <div class="message-inner">
        <div class="message-avatar">${avatarLabel}</div>
        <div class="message-content">${role === 'user' ? escapeHtml(content) : renderMarkdown(content)}</div>
      </div>
    `;
    return div;
  }

  // --- Markdown Rendering (lightweight) ---
  function renderMarkdown(text) {
    // Simple markdown renderer
    let html = text;

    // Code blocks: ```lang\n...\n```
    html = html.replace(/```(\w*)\n([\s\S]*?)```/g, (_, lang, code) => {
      return `<pre><code class="language-${lang || 'text'}">${escapeHtml(code.trim())}</code><button class="copy-btn" onclick="copyCode(this)">Copy</button></pre>`;
    });

    // Inline code: `...`
    html = html.replace(/`([^`]+)`/g, '<code>$1</code>');

    // Bold: **...**
    html = html.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>');

    // Italic: *...*
    html = html.replace(/(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)/g, '<em>$1</em>');

    // Headers: # ## ###
    html = html.replace(/^### (.+)$/gm, '<h3>$1</h3>');
    html = html.replace(/^## (.+)$/gm, '<h2>$1</h2>');
    html = html.replace(/^# (.+)$/gm, '<h1>$1</h1>');

    // Blockquotes: > ...
    html = html.replace(/^> (.+)$/gm, '<blockquote>$1</blockquote>');

    // Unordered lists: - item
    html = html.replace(/^[-*] (.+)$/gm, '<li>$1</li>');
    html = html.replace(/(<li>[\s\S]*?<\/li>)/g, '<ul>$1</ul>');
    // Clean up nested ul tags
    html = html.replace(/<\/ul>\s*<ul>/g, '');

    // Ordered lists: 1. item
    html = html.replace(/^\d+\. (.+)$/gm, '<li>$1</li>');

    // Links: [text](url)
    html = html.replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2" target="_blank" rel="noopener">$1</a>');

    // Paragraphs: double newline
    html = html.replace(/\n\n/g, '</p><p>');

    // Single newlines to <br> (except inside pre/code)
    html = html.replace(/(?<!<\/?\w[^>]*)\n(?!<\/?pre|<\/?code)/g, '<br>');

    // Wrap in <p> if not starting with block element
    if (!/^<(h[1-6]|pre|ul|ol|blockquote|div|table)/.test(html.trim())) {
      html = '<p>' + html + '</p>';
    }

    return html;
  }

  function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
  }

  // --- Copy Code ---
  window.copyCode = function(btn) {
    const code = btn.previousElementSibling.textContent;
    navigator.clipboard.writeText(code).then(() => {
      btn.textContent = 'Copied!';
      setTimeout(() => btn.textContent = 'Copy', 1500);
    });
  };

  // --- Streaming Chat ---
  async function handleSend() {
    const text = els.chatInput.value.trim();
    if (!text || state.isStreaming) return;

    const chat = getActiveChat();
    if (!chat) return;

    // Update chat model
    chat.model = els.modelSelect.value;

    // Add user message
    chat.messages.push({ role: 'user', content: text });

    // Update title from first message
    if (chat.messages.length === 1) {
      chat.title = text.length > 40 ? text.substring(0, 40) + '…' : text;
    }

    saveChats();
    renderChatList();

    // Clear input
    els.chatInput.value = '';
    els.chatInput.style.height = 'auto';
    els.sendBtn.disabled = true;

    // Remove welcome screen
    const welcome = els.chatMessages.querySelector('.welcome-screen');
    if (welcome) welcome.remove();

    // Render user message
    els.chatMessages.appendChild(createMessageElement('user', text));
    scrollToBottom();

    // Create assistant message placeholder
    const assistantDiv = document.createElement('div');
    assistantDiv.className = 'message assistant';
    assistantDiv.innerHTML = `
      <div class="message-inner">
        <div class="message-avatar">G</div>
        <div class="message-content stream-cursor">
          <div class="typing-indicator"><span></span><span></span><span></span></div>
        </div>
      </div>
    `;
    els.chatMessages.appendChild(assistantDiv);
    scrollToBottom();

    const contentDiv = assistantDiv.querySelector('.message-content');

    // Show stop button, hide send
    state.isStreaming = true;
    els.sendBtn.classList.add('hidden');
    els.stopBtn.classList.remove('hidden');

    state.abortController = new AbortController();

    try {
      const apiMessages = [
        { role: 'system', content: SYSTEM_PROMPT },
        ...chat.messages.map(m => ({ role: m.role, content: m.content })),
      ];

      const response = await fetch(GROQ_API_URL, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${state.apiKey}`,
        },
        body: JSON.stringify({
          model: chat.model,
          messages: apiMessages,
          stream: true,
          temperature: 0.7,
          max_tokens: 4096,
        }),
        signal: state.abortController.signal,
      });

      if (!response.ok) {
        const errData = await response.json().catch(() => ({}));
        throw new Error(errData.error?.message || `API Error: ${response.status}`);
      }

      const reader = response.body.getReader();
      const decoder = new TextDecoder();
      let fullContent = '';
      let buffer = '';

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        buffer += decoder.decode(value, { stream: true });
        const lines = buffer.split('\n');
        buffer = lines.pop() || '';

        for (const line of lines) {
          const trimmed = line.trim();
          if (!trimmed || !trimmed.startsWith('data: ')) continue;
          const data = trimmed.slice(6);
          if (data === '[DONE]') break;

          try {
            const json = JSON.parse(data);
            const delta = json.choices?.[0]?.delta?.content;
            if (delta) {
              fullContent += delta;
              contentDiv.innerHTML = renderMarkdown(fullContent);
              contentDiv.classList.add('stream-cursor');
              scrollToBottom();
            }
          } catch {}
        }
      }

      // Finalize
      contentDiv.classList.remove('stream-cursor');
      contentDiv.innerHTML = renderMarkdown(fullContent);

      // Save assistant message
      chat.messages.push({ role: 'assistant', content: fullContent });
      saveChats();

    } catch (err) {
      if (err.name === 'AbortError') {
        contentDiv.classList.remove('stream-cursor');
        const current = contentDiv.textContent;
        if (!current || current.trim() === '') {
          contentDiv.innerHTML = '<p style="color: var(--text-tertiary); font-style: italic;">Generation stopped.</p>';
        }
      } else {
        contentDiv.classList.remove('stream-cursor');
        contentDiv.innerHTML = `<p style="color: #ef4444;">⚠️ ${escapeHtml(err.message)}</p>`;

        if (err.message.includes('401') || err.message.includes('Invalid API')) {
          contentDiv.innerHTML += `<p style="color: var(--text-tertiary); font-size: 0.85rem;">Your API key may be invalid. <button onclick="document.getElementById('clear-key-btn').click()" style="color: var(--accent-orange); background: none; border: none; cursor: pointer; text-decoration: underline;">Change API Key</button></p>`;
        }
      }
    } finally {
      state.isStreaming = false;
      state.abortController = null;
      els.sendBtn.classList.remove('hidden');
      els.stopBtn.classList.add('hidden');
      updateSendButton();
      scrollToBottom();
    }
  }

  function stopStreaming() {
    if (state.abortController) {
      state.abortController.abort();
    }
  }

  // --- UI Helpers ---
  function scrollToBottom() {
    requestAnimationFrame(() => {
      els.chatMessages.scrollTop = els.chatMessages.scrollHeight;
    });
  }

  function updateSendButton() {
    els.sendBtn.disabled = !els.chatInput.value.trim();
  }

  function updateHeaderModel() {
    const name = MODEL_NAMES[els.modelSelect.value] || els.modelSelect.value;
    els.headerModelName.textContent = name;
  }

  function closeSidebar() {
    els.sidebar.classList.remove('open');
    const backdrop = document.querySelector('.sidebar-backdrop');
    if (backdrop) backdrop.remove();
  }

  function toggleSidebar() {
    const isOpen = els.sidebar.classList.toggle('open');
    if (isOpen) {
      const backdrop = document.createElement('div');
      backdrop.className = 'sidebar-backdrop';
      backdrop.addEventListener('click', closeSidebar);
      document.body.appendChild(backdrop);
    } else {
      closeSidebar();
    }
  }

  // --- Auto-resize textarea ---
  function autoResize() {
    els.chatInput.style.height = 'auto';
    els.chatInput.style.height = Math.min(els.chatInput.scrollHeight, 160) + 'px';
  }

  // --- Event Bindings ---
  function bindEvents() {
    // API Key
    els.apiKeySubmit.addEventListener('click', handleApiKeySubmit);
    els.apiKeyInput.addEventListener('keydown', (e) => {
      if (e.key === 'Enter') handleApiKeySubmit();
      els.apiKeyInput.style.borderColor = '';
    });

    // Clear API key
    els.clearKeyBtn.addEventListener('click', () => {
      localStorage.removeItem(STORAGE_KEY_API);
      state.apiKey = '';
      showModal();
    });

    // New chat
    els.newChatBtn.addEventListener('click', () => {
      createNewChat();
      closeSidebar();
    });

    // Send message
    els.chatForm.addEventListener('submit', (e) => {
      e.preventDefault();
      handleSend();
    });

    // Stop streaming
    els.stopBtn.addEventListener('click', stopStreaming);

    // Input handling
    els.chatInput.addEventListener('input', () => {
      updateSendButton();
      autoResize();
    });

    els.chatInput.addEventListener('keydown', (e) => {
      if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        handleSend();
      }
    });

    // Model select
    els.modelSelect.addEventListener('change', () => {
      updateHeaderModel();
      const chat = getActiveChat();
      if (chat) {
        chat.model = els.modelSelect.value;
        saveChats();
      }
    });

    // Sidebar toggle (mobile)
    els.sidebarToggle.addEventListener('click', toggleSidebar);

    // Keyboard shortcut: Ctrl+Shift+N for new chat
    document.addEventListener('keydown', (e) => {
      if ((e.ctrlKey || e.metaKey) && e.shiftKey && e.key === 'N') {
        e.preventDefault();
        createNewChat();
      }
    });
  }

  // --- Start ---
  init();
})();
