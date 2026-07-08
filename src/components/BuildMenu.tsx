import { TOWERS, TOWER_ORDER, type TowerKind } from "../game/data/towers";

interface Props {
  selectedKind: TowerKind | null;
  cores: number;
  onSelect: (k: TowerKind | null) => void;
}

const ICONS: Record<TowerKind, string> = {
  pulse: "◎",
  laser: "✦",
  emp: "⚡",
  plasma: "❂",
  railgun: "↯",
  nano: "✺",
  quantum: "◉",
};

export function BuildMenu({ selectedKind, cores, onSelect }: Props) {
  const KEY_MAP: Record<number, TowerKind> = {
    1: "pulse",
    2: "laser",
    3: "emp",
    4: "plasma",
    5: "railgun",
    6: "nano",
    7: "quantum",
  };

  return (
    <div className="pointer-events-auto absolute bottom-0 left-0 right-0 p-3 z-20">
      <div className="mx-auto max-w-5xl border border-cyan-500/40 bg-black/80 backdrop-blur-md rounded-lg p-3 shadow-2xl shadow-cyan-500/20">
        <div className="flex items-center justify-between mb-2">
          <h2 className="text-xs font-mono tracking-[0.3em] text-cyan-300 drop-shadow-[0_0_3px_rgba(0,0,0,0.9)]">// BUILD ARRAY</h2>
          <div className="text-[10px] text-white/60 font-mono drop-shadow-[0_0_2px_rgba(0,0,0,0.9)]">
            [1-7] Select Tower • Click to Place • Right-click Cancel
          </div>
        </div>
        <div className="grid grid-cols-7 gap-2">
          {TOWER_ORDER.map((k, idx) => {
            const def = TOWERS[k];
            const cost = def.levels[0].cost;
            const affordable = cores >= cost;
            const active = selectedKind === k;
            const keyNum = idx + 1;
            return (
              <button
                key={k}
                onClick={() => onSelect(active ? null : k)}
                disabled={!affordable && !active}
                className={`relative group p-2 rounded-md border-2 transition text-left ${
                  active
                    ? "bg-cyan-500/25 border-cyan-300 shadow-lg shadow-cyan-400/50"
                    : affordable
                    ? "bg-black/70 border-white/15 hover:border-cyan-400/70 hover:bg-black/80"
                    : "bg-black/50 border-white/5 opacity-50 cursor-not-allowed"
                }`}
                style={
                  active
                    ? { boxShadow: `0 0 25px #${def.color.toString(16).padStart(6, "0")}99` }
                    : undefined
                }
              >
                {/* Keyboard shortcut badge */}
                <div className="absolute -top-1.5 -left-1.5 w-5 h-5 rounded-full bg-slate-800 border border-cyan-400/60 flex items-center justify-center text-[9px] font-mono text-cyan-200 drop-shadow-[0_0_2px_rgba(0,0,0,0.9)]">
                  {keyNum}
                </div>
                <div className="flex items-center gap-2">
                  <div
                    className="w-9 h-9 rounded flex items-center justify-center text-xl font-bold"
                    style={{
                      background: `#${def.baseColor.toString(16).padStart(6, "0")}`,
                      color: `#${def.color.toString(16).padStart(6, "0")}`,
                      textShadow: `0 0 10px #${def.color.toString(16).padStart(6, "0")}`,
                      border: `1px solid #${def.color.toString(16).padStart(6, "0")}99`,
                    }}
                  >
                    {ICONS[k]}
                  </div>
                  <div className="min-w-0">
                    <div className="text-[10px] font-mono text-white/70 truncate drop-shadow-[0_0_2px_rgba(0,0,0,0.8)]">{def.name}</div>
                    <div
                      className={`text-xs font-mono ${affordable ? "text-cyan-200 drop-shadow-[0_0_2px_rgba(0,0,0,0.8)]" : "text-rose-300 drop-shadow-[0_0_2px_rgba(0,0,0,0.8)]"}`}
                    >
                      ⬢ {cost}
                    </div>
                  </div>
                </div>
                <div className="text-[9px] text-white/50 mt-1 leading-tight line-clamp-2 drop-shadow-[0_0_1px_rgba(0,0,0,0.8)]">
                  {def.description}
                </div>
              </button>
            );
          })}
        </div>
      </div>
    </div>
  );
}
