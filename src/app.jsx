import { useState, useEffect } from "react";
import Sidebar from "./components/Sidebar";
import StatCard from "./components/StatCard";
import InspectionPanel from "./components/InspectionPanel";
import DefectBreakdown from "./components/DefectBreakdown";
import RecentInspections from "./components/RecentInspections";
import { getStats, getHistory } from "./api";

export default function App() {
    const [stats, setStats] = useState(null);
    const [history, setHistory] = useState([]);
    const [latestResult, setLatestResult] = useState(null);

    async function loadDashboardData() {
        const [statsData, historyData] = await Promise.all([
            getStats(),
            getHistory(10),
        ]);
        setStats(statsData);
        setHistory(historyData);
    }

    // Runs once, right after the component first renders (empty dependency array
    // means "don't re-run this on every re-render, only on mount").
    useEffect(() => {
        loadDashboardData();
    }, []);

    // Called by InspectionPanel every time a new inspection completes.
    // This is the "lifting state up" callback we discussed while building
    // InspectionPanel: it owns the upload UI, but App owns the shared data.
    function handleNewResult(result) {
        setLatestResult(result);
        loadDashboardData(); // refresh stats + history so the new inspection shows up everywhere
    }

    return (
        <div className="grid grid-cols-[56px_1fr] min-h-screen">
            <Sidebar />

            <div className="bg-white px-5 py-4">
                <div className="flex items-center justify-between mb-5">
                    <div>
                        <p className="text-lg font-medium text-[#18181b]">Quality inspection</p>
                        <p className="text-[13px] text-[#71717a] mt-0.5">
                            Line A &middot; Bottle assembly
                        </p>
                    </div>
                    <div className="flex items-center gap-1.5 text-xs px-2.5 py-1 rounded-md bg-[#ecfdf3] text-[#067647]">
                        <span className="w-1.5 h-1.5 rounded-full bg-[#17b26a]" />
                        Live
                    </div>
                </div>

                <div className="grid grid-cols-4 gap-2.5 mb-3.5">
                    <StatCard
                        label="Total inspections"
                        value={stats?.total_inspections ?? "—"}
                    />
                    <StatCard
                        label="Passed"
                        value={stats?.verdict_counts?.pass ?? 0}
                        valueColor="#17b26a"
                    />
                    <StatCard
                        label="Escalated"
                        value={stats?.verdict_counts?.escalate ?? 0}
                        valueColor="#e0392f"
                    />
                    <StatCard
                        label="Pass rate"
                        value={
                            stats?.total_inspections
                                ? `${Math.round(
                                    ((stats.verdict_counts?.pass ?? 0) / stats.total_inspections) * 100
                                )}%`
                                : "—"
                        }
                    />
                </div>

                <div className="grid grid-cols-[1.15fr_0.85fr] gap-3">
                    <InspectionPanel
                        latestResult={latestResult}
                        onNewResult={handleNewResult}
                    />

                    <div className="flex flex-col gap-3">
                        <DefectBreakdown defectCounts={stats?.defect_type_counts} />
                        <RecentInspections history={history} />
                    </div>
                </div>
            </div>
        </div>
    );
}