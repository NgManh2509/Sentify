import { useState, useRef, useEffect } from "react";
import { FaRegPaperPlane } from "react-icons/fa6";
import { FiLoader } from "react-icons/fi";
import { analyzeText } from "../../services/api";
import ModelResponse from "../ResponseComponents/ModelResponse";

export default function MainChat() {
    const [messages, setMessages] = useState([]);
    const [inputValue, setInputValue] = useState("");
    const [isLoading, setIsLoading] = useState(false);
    const [isFocused, setIsFocused] = useState(false);
    const messagesEndRef = useRef(null);

    const hasSent = messages.length > 0;

    const handleSend = async () => {
        const text = inputValue.trim();
        if (!text || isLoading) return;

        const userMsg = { id: Date.now(), type: "user", text };
        setMessages((prev) => [...prev, userMsg]);
        setInputValue("");
        setIsLoading(true);

        try {
            const data = await analyzeText(text);
            const botMsg = { id: Date.now() + 1, type: "bot", data };
            setMessages((prev) => [...prev, botMsg]);
        } catch (err) {
            const errMsg = {
                id: Date.now() + 1,
                type: "error",
                text: err.message || "Đã xảy ra lỗi. Vui lòng thử lại.",
            };
            setMessages((prev) => [...prev, errMsg]);
        } finally {
            setIsLoading(false);
        }
    };

    const handleKeyDown = (e) => {
        if (e.key === "Enter" && !e.shiftKey) handleSend();
    };

    useEffect(() => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    }, [messages, isLoading]);

    return (
        <div
            className={`
                flex flex-col bg-white text-[#333] overflow-hidden
                transition-all duration-300
                ${isFocused || isLoading ? 'animate-aura-active' : 'animate-aura-pulse'}
                ${hasSent
                    ? "w-full max-w-[65rem] mx-4 rounded-2xl shadow-[0_0.5rem_2rem_rgba(0,0,0,0.05)] h-[85vh]"
                    : "w-full max-w-[65rem] mx-4 rounded-2xl shadow-[0_0.5rem_2rem_rgba(0,0,0,0.05)]"
                }
            `}
        >
            {/* Messages area */}
            {hasSent && (
                <div className="flex-1 overflow-y-auto px-6 py-4 flex flex-col gap-4">
                    {messages.map((msg) => {
                        if (msg.type === "user") {
                            return (
                                <div key={msg.id} className="flex justify-end">
                                    <div
                                        className="max-w-[70%] px-4 py-2.5 rounded-2xl rounded-br-sm text-sm text-[#333] leading-relaxed"
                                        style={{ backgroundColor: "#f2f0f0" }}
                                    >
                                        {msg.text}
                                    </div>
                                </div>
                            );
                        }

                        if (msg.type === "bot") {
                            return (
                                <div key={msg.id} className="flex justify-start">
                                    <div className="w-full max-w-[90%]">
                                        <ModelResponse data={msg.data} />
                                    </div>
                                </div>
                            );
                        }

                        if (msg.type === "error") {
                            return (
                                <div key={msg.id} className="flex justify-start">
                                    <div className="max-w-[70%] px-4 py-2.5 rounded-2xl rounded-bl-sm text-sm text-red-600 bg-red-50 leading-relaxed">
                                        ⚠️ {msg.text}
                                    </div>
                                </div>
                            );
                        }

                        return null;
                    })}

                    {/* Loading indicator */}
                    {isLoading && (
                        <div className="flex justify-start">
                            <div className="px-4 py-3 rounded-2xl rounded-bl-sm bg-[#f2f0f0] flex items-center gap-2 text-sm text-gray-500">
                                <FiLoader className="animate-spin" size={15} />
                                <span>Đang phân tích cảm xúc...</span>
                            </div>
                        </div>
                    )}

                    <div ref={messagesEndRef} />
                </div>
            )}

            {/* Input bar */}
            <div className={`p-4 ${hasSent ? "border-t border-gray-100" : ""}`}>
                <div className="flex items-center gap-2 bg-white p-2 rounded-xl shadow-[0_0.125rem_0.5rem_rgba(0,0,0,0.05)]">
                    <input
                        type="text"
                        value={inputValue}
                        onChange={(e) => setInputValue(e.target.value)}
                        onKeyDown={handleKeyDown}
                        placeholder="Tell me how you feel..."
                        disabled={isLoading}
                        onFocus={() => setIsFocused(true)}
                        onBlur={() => setIsFocused(false)}
                        className="flex-1 border-none outline-none text-sm p-2 bg-transparent text-[#333] placeholder:text-gray-400 disabled:opacity-60"
                    />
                    <button
                        onClick={handleSend}
                        disabled={isLoading || !inputValue.trim()}
                        className="bg-[#f26639] border-none text-white w-8 h-8 rounded-lg flex items-center justify-center cursor-pointer hover:bg-[#d95b33] transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                    >
                        {isLoading ? <FiLoader className="animate-spin" size={15} /> : <FaRegPaperPlane />}
                    </button>
                </div>
            </div>
        </div>
    );
}