import { useState, useRef, useEffect } from "react";
import { FaRegPaperPlane } from "react-icons/fa6";

export default function MainChat() {
    const [messages, setMessages] = useState([]);
    const [inputValue, setInputValue] = useState("");
    const messagesEndRef = useRef(null);

    const hasSent = messages.length > 0;

    const handleSend = () => {
        const text = inputValue.trim();
        if (!text) return;
        setMessages((prev) => [...prev, { id: Date.now(), text }]);
        setInputValue("");
    };

    const handleKeyDown = (e) => {
        if (e.key === "Enter") handleSend();
    };

    // Auto scroll xuống khi có tin nhắn mới
    useEffect(() => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    }, [messages]);

    return (
        <div
            className={`
                flex flex-col bg-white text-[#333] overflow-hidden
                transition-all duration-300
                ${hasSent
                    ? "w-full max-w-[65rem] mx-4 rounded-2xl shadow-[0_0.5rem_2rem_rgba(0,0,0,0.05)] h-[80vh]"
                    : "w-full max-w-[65rem] mx-4 rounded-2xl shadow-[0_0.5rem_2rem_rgba(0,0,0,0.05)]"
                }
            `}
        >
            {hasSent && (
                <div className="flex-1 overflow-y-auto px-6 py-4 flex flex-col gap-3">
                    {messages.map((msg) => (
                        <div key={msg.id} className="flex justify-end">
                            <div
                                className="max-w-[70%] px-4 py-2.5 rounded-2xl rounded-br-sm text-sm text-[#333] leading-relaxed"
                                style={{ backgroundColor: "#f2f0f0" }}
                            >
                                {msg.text}
                            </div>
                        </div>
                    ))}
                    <div ref={messagesEndRef} />
                </div>
            )}

            <div className={`p-4 ${hasSent ? "" : ""}`}>
                <div className="flex items-center gap-2 bg-white p-2 rounded-xl shadow-[0_0.125rem_0.5rem_rgba(0,0,0,0.05)]">
                    <input
                        type="text"
                        value={inputValue}
                        onChange={(e) => setInputValue(e.target.value)}
                        onKeyDown={handleKeyDown}
                        placeholder="Tell me how you feel..."
                        className="flex-1 border-none outline-none text-sm p-2 bg-transparent text-[#333] placeholder:text-gray-400"
                    />
                    <button
                        onClick={handleSend}
                        className="bg-[#f26639] border-none text-white w-8 h-8 rounded-lg flex items-center justify-center cursor-pointer hover:bg-[#d95b33] transition-colors"
                    >
                        <FaRegPaperPlane />
                    </button>
                </div>
            </div>
        </div>
    );
}