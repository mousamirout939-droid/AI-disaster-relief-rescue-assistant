import { useRef, useState } from 'react';
import { MessageCircle, Send, X, Bot } from 'lucide-react';
import { aiApi } from '../../api/endpoints';
import './aichat.css';

/** Floating emergency chatbot widget, backed by the Gemini-powered /ai/chat endpoint. */
export default function AIChat() {
  const [open, setOpen] = useState(false);
  const [messages, setMessages] = useState([
    { role: 'assistant', text: "Hi, I'm your emergency assistant. Describe your situation and I'll help." },
  ]);
  const [input, setInput] = useState('');
  const [sending, setSending] = useState(false);
  const scrollRef = useRef(null);

  const send = async () => {
    const text = input.trim();
    if (!text || sending) return;

    const history = messages.map((m) => ({ role: m.role === 'assistant' ? 'model' : 'user', text: m.text }));
    setMessages((prev) => [...prev, { role: 'user', text }]);
    setInput('');
    setSending(true);

    try {
      const { data } = await aiApi.chat(text, history);
      setMessages((prev) => [...prev, { role: 'assistant', text: data.data.reply }]);
    } catch {
      setMessages((prev) => [...prev, { role: 'assistant', text: 'Sorry, I could not reach the assistant right now.' }]);
    } finally {
      setSending(false);
      setTimeout(() => scrollRef.current?.scrollTo(0, scrollRef.current.scrollHeight), 50);
    }
  };

  if (!open) {
    return (
      <button className="aichat__fab" onClick={() => setOpen(true)} aria-label="Open emergency assistant">
        <MessageCircle size={24} />
      </button>
    );
  }

  return (
    <div className="aichat">
      <div className="aichat__header">
        <span className="flex items-center gap-2 font-semibold"><Bot size={18} /> Emergency Assistant</span>
        <button onClick={() => setOpen(false)} aria-label="Close chat"><X size={18} /></button>
      </div>

      <div ref={scrollRef} className="aichat__messages">
        {messages.map((m, i) => (
          <div key={i} className={`aichat__bubble ${m.role === 'user' ? 'aichat__bubble--user' : 'aichat__bubble--bot'}`}>
            {m.text}
          </div>
        ))}
        {sending && <div className="aichat__bubble aichat__bubble--bot">Typing…</div>}
      </div>

      <div className="aichat__input-row">
        <input
          className="input !py-2"
          placeholder="Describe your emergency…"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && send()}
        />
        <button className="btn-primary !px-3 !py-2" onClick={send} disabled={sending} aria-label="Send message">
          <Send size={16} />
        </button>
      </div>
    </div>
  );
}
