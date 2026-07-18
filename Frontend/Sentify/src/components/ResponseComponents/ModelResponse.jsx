import { useState } from "react";
import { FiDownload, FiCheck, FiAlertCircle } from "react-icons/fi";
import { LuLoaderCircle } from "react-icons/lu";
import { downloadTrack } from "../../services/api";

function TrackItem({ track }) {
    const [dlState, setDlState] = useState("idle");

    const handleDownload = async () => {
        if (dlState === "loading") return;
        setDlState("loading");
        try {
            await downloadTrack(track.name, track.artists);
            setDlState("done");
            setTimeout(() => setDlState("idle"), 2500);
        } catch {
            setDlState("error");
            setTimeout(() => setDlState("idle"), 2500);
        }
    };

    const iconEl =
        dlState === "loading" ? <LuLoaderCircle size={16} className="animate-spin" /> :
            dlState === "done" ? <FiCheck size={16} className="text-green-500" /> :
                dlState === "error" ? <FiAlertCircle size={16} className="text-red-400" /> :
                    <FiDownload size={16} />;

    return (
        <div className="flex items-center gap-2">
            {/* Spotify iframe */}
            <div className="flex-1 min-w-0 rounded-xl overflow-hidden">
                <iframe
                    title={`${track.name} - ${track.artists}`}
                    style={{ borderRadius: "12px" }}
                    src={`https://open.spotify.com/embed/track/${track.id}`}
                    width="100%"
                    height="80"
                    frameBorder="0"
                    allowFullScreen
                    allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture"
                    loading="lazy"
                />
            </div>

            {/* Download button */}
            <button
                onClick={handleDownload}
                title={dlState === "error" ? "Thử lại" : "Tải MP3"}
                aria-label={`Tải ${track.name}`}
                className="shrink-0 w-12 h-12 rounded-xl border border-black/10 bg-white/60 backdrop-blur-sm flex items-center justify-center text-gray-500 hover:bg-orange-50 hover:text-[#f26639] hover:border-orange-200 hover:scale-105 active:scale-95 transition-all duration-150 cursor-pointer"
            >
                {iconEl}
            </button>
        </div>
    );
}

export default function ModelResponse({ data }) {
    if (!data) return null;
    const { recommendations = [] } = data;

    return (
        <div className="w-full rounded-2xl overflow-hidden bg-white/60 backdrop-blur-sm border border-black/[0.06] shadow-sm">
            {/* Greeting */}
            <div className="px-5 pt-4 pb-3">
                <p className="text-sm text-gray-600 leading-relaxed">
                    Xin chào! Đây là danh sách nhạc mình gợi ý cho bạn:
                </p>
            </div>

            {/* Track list */}
            <div className="px-4 pb-4 flex flex-col gap-2.5">
                {recommendations.length === 0 ? (
                    <p className="text-sm text-gray-400 text-center py-3">
                        Không tìm thấy gợi ý phù hợp.
                    </p>
                ) : (
                    recommendations.map((track, i) => (
                        <TrackItem key={track.id ?? i} track={track} />
                    ))
                )}
            </div>
        </div>
    );
}
