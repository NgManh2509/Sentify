const BASE_URL = 'http://localhost:8000';

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
            body: JSON.stringify({ text: inputText })
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

