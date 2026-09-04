export default function StatCard({ label, value, valueColor, trend }) {
    return (
        <div className="bg-[#fafafa] border border-[#ececec] rounded-[10px] px-3.5 py-3">
            <p className="text-xs text-[#71717a] mb-1">{label}</p>
            <div className="flex items-baseline gap-1.5">
                <p
                    className="text-xl font-medium"
                    style={{ color: valueColor || "#18181b" }}
                >
                    {value}
                </p>
                {trend && (
                    <span className="text-[11px] text-[#17b26a]">{trend}</span>
                )}
            </div>
        </div>
    );
}