import { useMemo, useState } from "react";
import { Bot, ChevronRight, X } from "lucide-react";
import ParlantChatbox from "parlant-chat-react";
import { Button } from "@/components/UI/button";
import { Badge } from "@/components/UI/badge";
import { cn } from "@/lib/utils";

const defaultServer = "http://localhost:8800";

export function AIChatPanel() {
  const [isOpen, setIsOpen] = useState(true);

  const config = useMemo(() => {
    const server = (import.meta.env.VITE_PARLANT_SERVER as string | undefined) || defaultServer;
    const agentId = (import.meta.env.VITE_PARLANT_AGENT_ID as string | undefined) || "";
    return { server, agentId };
  }, []);

  if (!isOpen) {
    return (
      <button
        type="button"
        aria-label="Open AI Chat Panel"
        onClick={() => setIsOpen(true)}
        className="fixed right-0 top-1/2 -translate-y-1/2 bg-primary text-primary-foreground p-2 rounded-l-lg shadow-lg hover:bg-primary/90 transition-colors"
      >
        <ChevronRight className="h-5 w-5 rotate-180" />
      </button>
    );
  }

  const hasConfig = Boolean(config.agentId);

  return (
    <aside className="w-96 border-l border-border bg-card/90 backdrop-blur flex flex-col h-full">
      <div className="p-4 border-b border-border flex items-center justify-between">
        <div className="flex items-center gap-2">
          <div className="h-8 w-8 rounded-full bg-primary/10 flex items-center justify-center">
            <Bot className="h-5 w-5 text-primary" />
          </div>
          <div>
            <h3 className="font-semibold text-sm">GFM Assistant</h3>
            <p className="text-xs text-muted-foreground">Powered by Parlant + Emcie</p>
          </div>
        </div>
        <Button
          variant="ghost"
          size="icon"
          className="h-8 w-8"
          onClick={() => setIsOpen(false)}
        >
          <X className="h-4 w-4" />
        </Button>
      </div>

      <div className="flex-1 min-h-0 p-3">
        {hasConfig ? (
          <div className={cn("h-full w-full rounded-xl border border-border bg-background/70")}> 
            <ParlantChatbox server={config.server} agentId={config.agentId} />
          </div>
        ) : (
          <div className="h-full w-full rounded-xl border border-dashed border-border bg-background/70 p-4 text-sm text-muted-foreground flex flex-col gap-3">
            <Badge variant="secondary" className="w-fit">Setup required</Badge>
            <p>
              Add <span className="font-mono">VITE_PARLANT_AGENT_ID</span> and <span className="font-mono">VITE_PARLANT_SERVER</span> to your
              <span className="font-mono">.env</span> (example in <span className="font-mono">.env.example</span>), then restart the dev server.
            </p>
            <div className="rounded-lg bg-muted/60 p-3 text-xs leading-relaxed text-muted-foreground">
              <div className="font-semibold text-foreground">Quick setup</div>
              <div>1. <span className="font-mono">pip install parlant</span></div>
              <div>2. <span className="font-mono">export EMCIE_API_KEY=... </span></div>
              <div>3. <span className="font-mono">parlant-server run</span></div>
              <div>4. <span className="font-mono">parlant agent create --name "GFM Assistant"</span></div>
            </div>
          </div>
        )}
      </div>
    </aside>
  );
}
