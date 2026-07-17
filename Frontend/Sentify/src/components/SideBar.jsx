import { useState } from 'react';
import { IoChatbubbleEllipsesOutline, IoDocumentTextOutline, IoChevronBackOutline, IoChevronForwardOutline } from 'react-icons/io5';

export default function SideBar({ activePage, onNavigate }) {
    const [isOpen, setIsOpen] = useState(true);

    const navItems = [
        { id: 'chat', label: 'Chat', icon: <IoChatbubbleEllipsesOutline size={20} /> },
        { id: 'instruction', label: 'Instruction', icon: <IoDocumentTextOutline size={20} /> },
    ];

    return (
        <aside
            className={`
                flex flex-col min-h-screen bg-white 
                transition-all duration-300 ease-in-out overflow-hidden flex-shrink-0
                ${isOpen ? 'w-[220px]' : 'w-16'}
            `}
        >
            {/* Logo + App name */}
            <div className="flex items-center gap-3 px-4 py-5 min-h-[72px] overflow-hidden">
                <img
                    src="/appIcon.png"
                    alt="Sentify Logo"
                    className="w-8 h-8 rounded-lg flex-shrink-0"
                />
                <span
                    className={`font-bold text-lg text-gray-900 tracking-tight whitespace-nowrap transition-opacity duration-200 ${isOpen ? 'opacity-100' : 'opacity-0'}`}
                >
                    Sentify
                </span>
            </div>

            {/* Nav items */}
            <nav className="flex flex-col gap-1 flex-1 p-2">
                {navItems.map((item) => {
                    const isActive = activePage === item.id;
                    return (
                        <button
                            key={item.id}
                            onClick={() => onNavigate(item.id)}
                            title={!isOpen ? item.label : ''}
                            className={`
                                flex items-center gap-3 w-full px-3 py-2.5 rounded-xl
                                text-sm text-left whitespace-nowrap overflow-hidden
                                transition-all duration-200 cursor-pointer border-none
                                ${isActive
                                    ? 'bg-[#f26639] text-white font-semibold'
                                    : 'text-gray-500 hover:bg-gray-100 hover:text-gray-900 font-medium'
                                }
                            `}
                        >
                            <span className="flex-shrink-0">{item.icon}</span>
                            <span className={`transition-opacity duration-200 ${isOpen ? 'opacity-100' : 'opacity-0'}`}>
                                {item.label}
                            </span>
                        </button>
                    );
                })}
            </nav>

            {/* Toggle button */}
            <button
                onClick={() => setIsOpen(!isOpen)}
                title={isOpen ? 'Thu gọn' : 'Mở rộng'}
                className="flex items-center justify-center m-2 p-2.5 rounded-xl border-none cursor-pointer
                           bg-gray-100 text-gray-500 hover:bg-gray-200 hover:text-gray-900 transition-all duration-200"
            >
                {isOpen ? <IoChevronBackOutline size={18} /> : <IoChevronForwardOutline size={18} />}
            </button>
        </aside>
    );
}