const BASE_URL = 'http://localhost:8000';

/**
 * Trả về session_id của tab hiện tại.
 * Tạo mới nếu chưa có, lưu trong sessionStorage (riêng biệt mỗi tab).
 */
function getOrCreateSessionId() {
    const KEY = 'sentify_session_id';
    let id = sessionStorage.getItem(KEY);
    if (!id) {
        id = crypto.randomUUID();
        sessionStorage.setItem(KEY, id);
    }
    return id;
}

/**
 * Gọi API để phân tích cảm xúc và lấy gợi ý nhạc
 * @param {string} inputText - Đoạn chat người dùng nhập vào
 * @returns {Promise<Object>} - Object chứa status, emotion, và mảng recommendations
 */
export const analyzeText = async (inputText) => {
    try {
        const res = await fetch(`${BASE_URL}/api/analyze`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                text: inputText,
                session_id: getOrCreateSessionId()
            })
        })

        if (!res.ok) {
            const errorData = await res.json()
            throw new Error(errorData.detail || "Đã xảy ra lỗi khi gọi API");
        }

        const data = await res.json()
        return data;

    } catch (error) {
        console.error('Error calling API', error);
        throw error;
    }
}

/**
 * Tải bài hát dưới dạng MP3 qua YouTube
 * @param {string} songName - Tên bài hát
 * @param {string} artistName - Tên nghệ sĩ
 */
export const downloadTrack = async (songName, artistName) => {
    const params = new URLSearchParams({ song_name: songName, artist_name: artistName });
    const res = await fetch(`${BASE_URL}/api/download?${params.toString()}`);

    if (!res.ok) {
        const errorData = await res.json().catch(() => ({}));
        throw new Error(errorData.detail || "Lỗi khi tải nhạc");
    }

    // Tạo blob và trigger download trình duyệt
    const blob = await res.blob();
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `${songName} - ${artistName}.mp3`;
    document.body.appendChild(a);
    a.click();
    a.remove();
    window.URL.revokeObjectURL(url);
}
