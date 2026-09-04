const BAR_COLORS = {
    crack: "#e0392f",
    scratch: "#e0a115",
    corrosion: "#e0a115",
    dent: "#e0a115",
    discoloration: "#e0a115",
    contamination: "#e0a115",
    thread_damage: "#e0a115",
};

export default function DefectBreakdown({ defectCounts }) {
    const entries = Object.entries(defectCounts || {});
    const maxCount = Math.max(...entries.map(([, count]) => count), 1);

    return (
        <div className="bg-white border border-[#ececec] rounded-xl p-[1.1rem]">
            <p className="text-[13px] text-[#71717a] mb-3">Defects by type</p>

            {entries.length === 0 ? (
                <p className="text-xs text-[#a1a1aa]">No defects logged yet.</p>
            ) : (
                <div className="flex flex-col gap-2.5">
                    {entries.map(([type, count]) => (
                        <div key={type}>
                            <div className="flex justify-between text-xs mb-1 text-[#18181b] capitalize">
                                <span>{type.replace("_", " ")}</span>
                                <span className="text-[#a1a1aa]">{count}</span>
                            </div>
                            <div className="h-1.5 rounded bg-[#f4f4f5]">
                                <div
                                    className="h-full rounded"
                                    style={{
                                        width: `${(count / maxCount) * 100}%`,
                                        background: BAR_COLORS[type] || "#a1a1aa",
                                    }}
                                />
                            </div>
                        </div>
                    ))}
                </div>
            )}
        </div>
    );
}