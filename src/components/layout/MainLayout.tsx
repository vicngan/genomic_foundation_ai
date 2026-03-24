import { Outlet, useLocation } from "react-router-dom";
import { TopBar } from "./TopBar";
import { Sidebar } from "./Sidebar";
import { AIChatPanel } from "./AIChatPanel";

export function MainLayout() {
  const location = useLocation();
  // Analysis page owns the full screen — hide the global chat panel there
  const hidePanel = location.pathname === "/" || location.pathname === "/analysis";

  return (
    <div className="h-screen flex flex-col bg-background/90 overflow-hidden">
      <TopBar />
      <div className="flex flex-1 min-h-0">
        <Sidebar />
        <main className="flex-1 overflow-hidden">
          <Outlet />
        </main>
        {!hidePanel && <AIChatPanel />}
      </div>
    </div>
  );
}
