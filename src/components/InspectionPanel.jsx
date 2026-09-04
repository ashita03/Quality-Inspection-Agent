import { useState } from "react";
import { Eye, History, Flag, Sparkles, Upload, ImageIcon, ChevronDown, ChevronUp } from "lucide-react";
import { inspectImage } from "../api";

const VERDICT_STYLES = {
    pass: { bg: "#ecfdf3", text: "#067647" },
    escalate: { bg: "#fef2f2", text: "#e0392f" },
};

// Maps each reasoning-trace line to an icon based on which node produced it.
// Our backend prefixes every line with the node name (e.g. "inspect_image: ...")
// so we can pattern-match on that prefix to pick a relevant icon.
function iconForTraceLine(line) {
    if (line.startsWith("inspect_image")) return { Icon: Eye, bg: "#eff6ff", color: "#1d6ee0" };
    if (line.startsWith("check_history")) return { Icon: History, bg: "#f5f3ff", color: "#6d4ee0" };
    return { Icon: Flag, bg: "#fef2f2", color: "#e0392f" };
}

export default function InspectionPanel({ latestResult, onNewResult }) {
    const [uploading, setUploading] = useState(false);
    const [error, setError] = useState(null);
    const [showDetails, setShowDetails] = useState(false);

    async function handleFileChange(event) {
        const file = event.target.files[0];
        if (!file) return;

        setUploading(true);
        setError(null);

        try {
            const partId = `PART-${Date.now().toString().slice(-4)}`;
            const result = await inspectImage(file, partId);
            onNewResult(result);
        } catch (err) {
            setError("Inspection failed. Is the backend running on localhost:8000?");
        } finally {
            setUploading(false);
            event.target.value = ""; // reset so re-selecting the same file re-triggers onChange
        }
    }

    return (
        <div>
            <label className="flex items-center gap-2 justify-center border border-dashed border-[#d4d4d4] rounded-[10px] px-4 py-3.5 mb-3 bg-[#fafafa] cursor-pointer hover:bg-[#f4f4f4] transition-colors">
                <Upload size={18} color="#a1a1aa" />
                <span className="text-xs text-[#a1a1aa]">
                    {uploading
                        ? "Running agent inspection..."
                        : "Drag an image here or click to upload a part for the agent to inspect"}
                </span>
                <input
                    type="file"
                    accept="image/*"
                    className="hidden"
                    onChange={handleFileChange}
                    disabled={uploading}
                />
            </label>

            {error && (
                <p className="text-xs text-[#e0392f] mb-3">{error}</p>
            )}

            <div className="bg-white border border-[#ececec] rounded-xl p-[1.1rem]">
                {!latestResult ? (
                    <p className="text-xs text-[#a1a1aa] text-center py-8">
                        No inspections yet — upload an image to see the agent's verdict here.
                    </p>
                ) : (
                    <>
                        <div className="flex items-center justify-between mb-3">
                            <p className="text-[13px] text-[#71717a]">Latest inspection</p>
                            <span
                                className="text-xs px-2.5 py-[3px] rounded-md capitalize"
                                style={{
                                    background: VERDICT_STYLES[latestResult.verdict]?.bg,
                                    color: VERDICT_STYLES[latestResult.verdict]?.text,
                                }}
                            >
                                {latestResult.verdict}
                            </span>
                        </div>

                        <div className="flex gap-3 mb-3.5">
                            <div className="w-24 h-24 rounded-[10px] bg-[#fafafa] flex-shrink-0 flex items-center justify-center">
                                <ImageIcon size={26} color="#d4d4d4" />
                            </div>
                            <div className="flex-1">
                                <p className="text-[15px] font-medium text-[#18181b] mb-0.5">
                                    {latestResult.part_id}
                                </p>
                                <div className="flex gap-1.5 flex-wrap">
                                    <span className="text-[11px] px-2 py-0.5 rounded-md bg-[#fef2f2] text-[#b42318]">
                                        {latestResult.defect_type}
                                    </span>
                                    <span className="text-[11px] px-2 py-0.5 rounded-md bg-[#f4f4f5] text-[#52525b]">
                                        Confidence {latestResult.confidence}
                                    </span>
                                </div>
                            </div>
                        </div>

                        <div className="border-t border-[#ececec] pt-3">
                            <div className="flex items-center gap-1.5 mb-2">
                                <Sparkles size={13} color="#6d4ee0" />
                                <p className="text-xs font-medium text-[#6d4ee0]">Agent summary</p>
                            </div>
                            <p className="text-xs text-[#52525b] mb-2.5">
                                {latestResult.notes || "No description returned by the model."}
                            </p>

                            <button
                                onClick={() => setShowDetails(!showDetails)}
                                className="flex items-center gap-1 text-xs text-[#6d4ee0] font-medium mb-2"
                            >
                                {showDetails ? "Hide details" : "View agent reasoning"}
                                {showDetails ? <ChevronUp size={14} /> : <ChevronDown size={14} />}
                            </button>

                            {showDetails && (
                                <div className="flex flex-col gap-2.5 pt-1">
                                    {latestResult.reasoning_trace.map((line, i) => {
                                        const { Icon, bg, color } = iconForTraceLine(line);
                                        return (
                                            <div key={i} className="flex gap-2.5">
                                                <div
                                                    className="w-[22px] h-[22px] rounded-full flex items-center justify-center flex-shrink-0"
                                                    style={{ background: bg }}
                                                >
                                                    <Icon size={12} color={color} />
                                                </div>
                                                <p className="text-xs text-[#52525b] pt-0.5">{line}</p>
                                            </div>
                                        );
                                    })}
                                </div>
                            )}
                        </div>
                    </>
                )}
            </div>
        </div>
    );
}