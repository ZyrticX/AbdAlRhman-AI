import { useState, useRef, useEffect } from "react";
import "./App.css";

const translations = {
  en: {
    title: "Abd AlRahman Assistant 🤖",
    placeholder: "Type your message here...",
    loading: "⏳ Loading...",
    error: "⚠️ Error connecting to the server.",
    send: "Send",
  },
  ar: {
    title: "المساعد عبد الرحمن 🤖",
    placeholder: "اكتب رسالتك هنا...",
    loading: "⏳ جاري التحميل...",
    error: "⚠️ حدث خطأ في الاتصال بالخادم.",
    send: "إرسال",
  },
  he: {
    title: "העוזר עבד אלרחמן 🤖",
    placeholder: "כתוב את ההודעה שלך כאן...",
    loading: "⏳ טוען...",
    error: "⚠️ שגיאה בחיבור לשרת.",
    send: "שלח",
  },
};

function App() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [lang, setLang] = useState("en");
  const messagesEndRef = useRef(null);

  const t = translations[lang];
  const dir = lang === "ar" || lang === "he" ? "rtl" : "ltr";

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(scrollToBottom, [messages]);

  const sendMessage = async () => {
    if (!input.trim()) return;

    const userMessage = { type: "user", text: input };
    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setLoading(true);

    try {
      const res = await fetch("https://abdalrhman.duckdns.org/api", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
      },
      body: JSON.stringify({ message: input }),
    });


      const data = await res.json();
      const botMessage = { type: "assistant", text: data.response };
      setMessages((prev) => [...prev, botMessage]);
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        { type: "assistant", text: t.error },
      ]);
    }

    setLoading(false);
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  const toggleLang = () => {
    const order = ["en", "ar", "he"];
    const nextIndex = (order.indexOf(lang) + 1) % order.length;
    setLang(order[nextIndex]);
  };

  return (
    <div className="main-content" dir={dir}>
      <header className="header">
        <h1>{t.title}</h1>
        <button className="lang-button" onClick={toggleLang}>
          🌐 {lang.toUpperCase()}
        </button>
      </header>

      <div className="chat-container">
        {messages.map((msg, index) => (
          <div key={index} className={`message ${msg.type}`}>
            <div className="message-bubble">{msg.text}</div>
          </div>
        ))}

        {loading && (
          <div className="message assistant">
            <div className="message-bubble">{t.loading}</div>
          </div>
        )}
        <div ref={messagesEndRef}></div>
      </div>

      <div className="input-area">
        <div className="input-container">
          <div className="input-wrapper">
            <textarea
              className="message-input"
              placeholder={t.placeholder}
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={handleKeyDown}
              rows={1}
            />
          </div>
          <button className="send-button" onClick={sendMessage}>
            ➤
          </button>
        </div>
      </div>
    </div>
  );
}

export default App;
