export const BASE_URL = "http://localhost:8000";

export async function inspectImage(file, partId) {
    const formData = new FormData();
    formData.append("file", file);

    const response = await fetch(
        `${BASE_URL}/inspect?part_id=${encodeURIComponent(partId)}`,
        {
            method: "POST",
            body: formData,
        }
    );

    if (!response.ok) {
        throw new Error(`Inspection failed: ${response.status}`);
    }

    return response.json();
}

export async function getHistory(limit = 20) {
    const response = await fetch(`${BASE_URL}/history?limit=${limit}`);
    if (!response.ok) {
        throw new Error(`Failed to load history: ${response.status}`);
    }
    return response.json();
}

export async function getStats() {
    const response = await fetch(`${BASE_URL}/stats`);
    if (!response.ok) {
        throw new Error(`Failed to load stats: ${response.status}`);
    }
    return response.json();
}