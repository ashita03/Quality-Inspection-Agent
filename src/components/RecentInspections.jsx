import { ImageIcon } from "lucide-react";

const VERDICT_TEXT_COLOR = {
    pass: "#17b26a",
    escalate: "#e0392f",
};

export default function RecentInspections({ history }) {
    return (
        <div className="bg-white border border-[#ececec] rounded-xl p-[1.1rem] flex-1">
            <p className="text-[13px] text-[#71717a] mb-2.5">Recent inspections</p>

            {history.length === 0 ? (
                <p className="text-xs text-[#a1a1aa]">Nothing inspected yet.</p>
            ) : (
                <div className="flex flex-col">
                    {history.map((item, i) => (
                        <div
                            key={item.id}
                            className={`flex items-center gap-2.5 py-1.5 ${i < history.length - 1 ? "border-b border-[#f4f4f5]" : ""
                                }`}
                        >
                            <div className="w-6.5 h-6.5 rounded-md bg-[#fafafa] flex items-center justify-center">
                                <ImageIcon size={13} color="#d4d4d4" />
                            </div>
                            <span className="text-[13px] flex-1 text-[#18181b]">
                                {item.part_id}
                            </span>
                            <span
                                className="text-xs capitalize"
                                style={{ color: VERDICT_TEXT_COLOR[item.verdict] || "#71717a" }}
                            >
                                {item.verdict}
                            </span>
                        </div>
                    ))}
                </div>
            )}
        </div>
    );
}