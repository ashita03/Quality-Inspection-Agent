import { Scan, LayoutDashboard, ScanEye, History, Settings } from "lucide-react";

export default function Sidebar() {
    return (
        <div className="w-14 flex flex-col items-center gap-5 py-4 bg-[#161615]">
            <div className="w-8 h-8 rounded-lg bg-[#2a2a28] flex items-center justify-center">
                <Scan size={18} color="#ffffff" />
            </div>
            <div className="w-8 h-8 rounded-lg bg-[#2a2a28] flex items-center justify-center">
                <LayoutDashboard size={18} color="#ffffff" />
            </div>
            <ScanEye size={19} color="#7a7a76" />
            <History size={19} color="#7a7a76" />
            <Settings size={19} color="#7a7a76" className="mt-auto" />
        </div>
    );
}