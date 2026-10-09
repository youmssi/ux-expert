import { useState } from 'react';
import { runAgent } from './agent';

type Message = { role: 'user' | 'assistant'; text: string };

export function Chat() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [busy, setBusy] = useState(false);

  const send = async () => {
    const question = input;
    setInput('');
    setBusy(true);
    try {
      const answer = await runAgent(question);
      setMessages(m => [...m, { role: 'user', text: question }, { role: 'assistant', text: answer }]);
    } catch {
      setMessages(m => [...m, { role: 'assistant', text: 'Error.' }]);
    } finally {
      setBusy(false);
    }
  };

  return (
    <section className="chat">
      {messages.length === 0 && <p>Ask me anything.</p>}
      {messages.map((m, i) => (
        <div key={i} className={m.role} dangerouslySetInnerHTML={{ __html: m.text }} />
      ))}
      {busy && <p>…</p>}
      <input value={input} onChange={e => setInput(e.target.value)} onKeyDown={e => e.key === 'Enter' && send()} />
      <button onClick={send} disabled={busy}>
        Send
      </button>
    </section>
  );
}
