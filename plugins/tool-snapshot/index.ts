import { promises as fs } from "node:fs";
import path from "node:path";
import { Plugin } from "@opencode/plugin";

type ToolInfo = {
  id: string;
  name?: string;
  namespace?: string;
  description?: string;
};

function namespaceOf(tool: ToolInfo): string {
  if (tool.namespace) return tool.namespace;
  const match = tool.id.match(/^([a-z0-9-]+)[._]/i);
  return match ? match[1] : "opencode";
}

export default Plugin.define({
  id: "tool-snapshot",
  async setup(ctx) {
    const workspace = String(
      (ctx.options as { workspace?: string } | undefined)?.workspace ??
        ctx.location.directory,
    );
    const registries = path.join(workspace, "registries");
    // OpenCode connects MCP servers per open directory. Two windows (e.g. the SAP
    // workspace and C:\Users\you) therefore produce different tool sets, and both
    // used to write the same files. Only the workspace that owns this toolkit
    // publishes, so the numbers in registries/ describe one known directory.
    const canonical = path.resolve(path.dirname(workspace));
    const directory = path.resolve(String(ctx.location.directory ?? canonical));
    const publish = directory === canonical;
    let lastRun = 0;
    let timer: ReturnType<typeof setTimeout> | undefined;
    let running = false;

    const write = async (name: string, data: unknown) => {
      await fs.writeFile(
        path.join(registries, name),
        JSON.stringify(data, null, 2) + "\n",
        "utf8",
      );
    };

    const read = async (name: string): Promise<unknown | undefined> => {
      try {
        return JSON.parse(await fs.readFile(path.join(registries, name), "utf8"));
      } catch {
        return undefined;
      }
    };

    const same = (a: unknown, b: unknown) => JSON.stringify(a) === JSON.stringify(b);

    const snapshot = async () => {
      if (running) return;
      running = true;
      try {
        if (!publish) {
          console.log(
            `[tool-snapshot] ${directory} is not ${canonical}; registries left alone`,
          );
          return;
        }
        const tools = (await ctx.tool.list()) as ToolInfo[];
        const namespaces: Record<string, number> = {};
        for (const tool of tools) {
          const ns = namespaceOf(tool);
          namespaces[ns] = (namespaces[ns] ?? 0) + 1;
        }

        const generated_at = new Date().toISOString();
        const nextSnapshot = {
          generated_at,
          source: "opencode plugin ctx.tool.list",
          directory,
          total: tools.length,
          namespaces,
        };
        const prevSnapshot = (await read("tools-snapshot.json")) as
          | { total?: number; namespaces?: Record<string, number> }
          | undefined;
        if (
          !prevSnapshot ||
          prevSnapshot.total !== nextSnapshot.total ||
          !same(prevSnapshot.namespaces, nextSnapshot.namespaces)
        ) {
          await write("tools-snapshot.json", nextSnapshot);
        }

        const nextTools = tools.map((tool) => ({
          id: tool.id,
          name: tool.name ?? "",
          namespace: namespaceOf(tool),
          description: (tool.description ?? "").slice(0, 200),
        }));
        const prevFull = (await read("tools-full.json")) as
          | { tools?: unknown }
          | undefined;
        if (!prevFull || !same(prevFull.tools, nextTools)) {
          await write("tools-full.json", {
            generated_at,
            directory,
            total: tools.length,
            tools: nextTools,
          });
        }

        lastRun = Date.now();
        console.log(
          `[tool-snapshot] ${tools.length} tools, ${Object.keys(namespaces).length} namespaces`,
        );
      } catch (error) {
        console.error("[tool-snapshot] failed:", error);
      } finally {
        running = false;
      }
    };

    const schedule = (delayMs = 2000) => {
      if (Date.now() - lastRun < 60_000) return;
      if (timer) clearTimeout(timer);
      timer = setTimeout(() => void snapshot(), delayMs);
    };

    // MCP servers may connect after plugin setup, so take a few early snapshots.
    schedule(3000);
    setTimeout(() => void snapshot(), 15_000);
    const interval = setInterval(() => void snapshot(), 10 * 60_000);

    const controller = new AbortController();
    void (async () => {
      try {
        for await (const event of ctx.event.subscribe({ signal: controller.signal })) {
          const type = String(event.type);
          if (
            type.startsWith("mcp.") ||
            type.startsWith("tool.") ||
            type.startsWith("session.")
          ) {
            schedule(2000);
          }
        }
      } catch (error) {
        if (!controller.signal.aborted) {
          console.error("[tool-snapshot] event stream failed:", error);
        }
      }
    })();

    return () => {
      controller.abort();
      if (timer) clearTimeout(timer);
      clearInterval(interval);
    };
  },
});
