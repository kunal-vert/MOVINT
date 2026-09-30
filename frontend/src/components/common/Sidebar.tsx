import React from "react";

export interface SidebarProps {
  activeTab?: string;
  onSelectTab?: (tab: string) => void;
}

export const Sidebar: React.FC<SidebarProps> = ({ activeTab = "registry", onSelectTab }) => {
  return (
    <aside className="sidebar w-64 p-4 bg-slate-100 border-r min-h-screen">
      <ul className="space-y-2">
        <li
          className={`p-2 rounded cursor-pointer ${activeTab === "registry" ? "bg-slate-200 font-bold" : "hover:bg-slate-50"}`}
          onClick={() => onSelectTab?.("registry")}
        >
          Traveler Registry
        </li>
        <li
          className={`p-2 rounded cursor-pointer ${activeTab === "logs" ? "bg-slate-200 font-bold" : "hover:bg-slate-50"}`}
          onClick={() => onSelectTab?.("logs")}
        >
          Entry / Exit Logs
        </li>
      </ul>
    </aside>
  );
};

export default Sidebar;
