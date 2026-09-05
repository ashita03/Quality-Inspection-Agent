import { ImageIcon } from "lucide-react";
import { BASE_URL } from "../api";

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
                            className={`flex items-center gap-2.5 py-2 ${i < history.length - 1 ? "border-b border-[#f4f4f5]" : ""
                                }`}
                        >
                            <div className="w-[34px] h-[34px] rounded-md bg-[#fafafa] flex-shrink-0 overflow-hidden flex items-center justify-center">
                                {item.image_url ? (
                                    <img
                                        src={`${BASE_URL}${item.image_url}`}
                                        alt={item.equipment_type || "part"}
                                        className="w-full h-full object-cover"
                                    />
                                ) : (
                                    <ImageIcon size={13} color="#d4d4d4" />
                                )}
                            </div>
                            <div className="flex-1 min-w-0">
                                <p className="text-[12.5px] font-medium text-[#18181b] truncate">
                                    {item.part_id}
                                </p>
                                <p className="text-[11px] text-[#a1a1aa] capitalize truncate">
                                    {item.equipment_type || "Unknown"}
                                </p>
                            </div>
                            <span
                                className="text-xs capitalize flex-shrink-0"
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