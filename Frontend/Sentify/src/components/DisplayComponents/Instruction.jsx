import { IoChatbubbleEllipsesOutline } from 'react-icons/io5';
import { FiMic, FiMusic, FiDownload } from 'react-icons/fi';

const steps = [
    {
        icon: <FiMic size={22} className="text-[#f26639]" />,
        title: 'Chia sẻ cảm xúc của bạn',
        desc: (
            <>
                Nhập một câu mô tả cảm xúc bạn đang có. Ví dụ:{' '}
                <span className="font-semibold text-gray-800">
                    "Tôi cảm thấy buồn và cô đơn hôm nay."
                </span>
            </>
        ),
    },
    {
        icon: <IoChatbubbleEllipsesOutline size={22} className="text-[#f26639]" />,
        title: 'Sentify phân tích cảm xúc',
        desc: 'Hệ thống sẽ tự động dịch và nhận diện cảm xúc từ đoạn văn bạn nhập bằng mô hình AI.',
    },
    {
        icon: <FiMusic size={22} className="text-[#f26639]" />,
        title: 'Nhận danh sách nhạc gợi ý',
        desc: 'Dựa trên cảm xúc phát hiện được, Sentify sẽ đề xuất những bài nhạc phù hợp với tâm trạng của bạn.',
    },
    {
        icon: <FiDownload size={22} className="text-[#f26639]" />,
        title: 'Tải nhạc về máy',
        desc: 'Nhấn nút tải ở cạnh mỗi bài hát để download file MP3 về máy ngay lập tức.',
    },
];

const examples = [
    'Tôi cảm thấy rất vui vì hôm nay mọi thứ đều suôn sẻ.',
    'Tôi đang buồn và không muốn làm gì cả.',
    'Tôi cảm thấy lo lắng về bài thi ngày mai.',
    'Hôm nay tôi rất phấn khích, không thể ngồi yên được!',
    'Tôi tức giận vì bị hiểu lầm.',
];

export default function Instruction() {
    return (
        <div className="w-full max-w-2xl mx-4">
            {/* Header */}
            <div className="mb-8 text-center">
                <h1 className="text-2xl font-bold text-gray-900 tracking-tight mb-2">
                    Cách sử dụng Sentify
                </h1>
                <p className="text-sm text-gray-500">
                    Chia sẻ tâm trạng — nhận ngay danh sách nhạc phù hợp với bạn.
                </p>
            </div>

            {/* Steps */}
            <div className="flex flex-col gap-3 mb-8">
                {steps.map((step, i) => (
                    <div
                        key={i}
                        className="flex items-start gap-4 bg-white rounded-2xl px-5 py-4 shadow-sm border border-black/[0.05]"
                    >
                        {/* Step number + icon */}
                        <div className="flex flex-col items-center gap-1.5 flex-shrink-0 pt-0.5">
                            <div className="w-9 h-9 rounded-xl bg-orange-50 flex items-center justify-center">
                                {step.icon}
                            </div>
                            <span className="text-[10px] font-bold text-gray-300 uppercase tracking-widest">
                                {String(i + 1).padStart(2, '0')}
                            </span>
                        </div>

                        {/* Content */}
                        <div className="flex-1 pt-1">
                            <p className="text-sm font-semibold text-gray-800 mb-0.5">{step.title}</p>
                            <p className="text-sm text-gray-500 leading-relaxed">{step.desc}</p>
                        </div>
                    </div>
                ))}
            </div>

            {/* Examples */}
            <div className="bg-white rounded-2xl px-5 py-4 shadow-sm border border-black/[0.05]">
                <p className="text-xs font-semibold text-gray-400 uppercase tracking-widest mb-3">
                    Ví dụ bạn có thể nhập
                </p>
                <div className="flex flex-col gap-2">
                    {examples.map((ex, i) => (
                        <div
                            key={i}
                            className="flex items-center gap-2.5 bg-gray-50 rounded-xl px-4 py-2.5"
                        >
                            <span className="text-[#f26639] text-lg leading-none">›</span>
                            <span className="text-sm text-gray-700 italic">"{ex}"</span>
                        </div>
                    ))}
                </div>
            </div>
        </div>
    );
}