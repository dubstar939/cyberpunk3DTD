import type { Stats } from "../game/types";

interface Props {
  stats: Stats;
  bossHp: { hp: number; max: number; shield: number; maxShield: number; phase: number } | null;
  onPause: () => void;
  onResume: () => void;
  onReset: () => void;
  onSpeedChange: (m: number) => void;
  speed: number;
  onShowDocs: () => void;
}

export function HUD({ stats, bossHp, onPause, onResume, onReset, onSpeedChange, speed, onShowDocs }: Props) {
  const wavePct = stats.totalWaves > 0 ? (stats.wave / stats.totalWaves) * 100 : 0;
  return (
    <div className="pointer-events-none absolute top-0 left-0 right-0 p-4 flex flex-col gap-2 z-20">
      <div className="pointer-events-auto flex flex-wrap items-center gap-3">
        <Pill label="LIVES" value={stats.lives} color="text-rose-300" border="border-rose-500/70" glow="shadow-rose-500/40" />
        <Pill label="ENERGY CORES" value={stats.cores} color="text-cyan-200" border="border-cyan-400/70" glow="shadow-cyan-500/40" />
        <Pill
          label="WAVE"
          value={`${Math.max(0, stats.wave)} / ${stats.totalWaves}`}
          color="text-fuchsia-200"
          border="border-fuchsia-400/70"
          glow="shadow-fuchsia-500/40"
        />
        <Pill label="ALIVE" value={stats.enemiesAlive} color="text-amber-200" border="border-amber-400/70" glow="shadow-amber-500/40" />
        <Pill label="KILLS" value={stats.killCount} color="text-emerald-200" border="border-emerald-400/70" glow="shadow-emerald-500/40" />
        <div className="flex-1" />
        <div className="flex items-center gap-2 px-3 py-2 rounded-md border-2 border-cyan-500/50 bg-slate-950/80 backdrop-blur-sm shadow-lg shadow-cyan-500/20">
          <span className="text-[10px] tracking-widest text-cyan-300 drop-shadow-[0_0_2px_rgba(0,0,0,0.9)]">SPEED [P]</span>
          {[1, 2, 3].map((s) => (
            <button
              key={s}
              onClick={() => onSpeedChange(s)}
              className={`px-2 py-0.5 text-xs font-mono rounded border-2 transition drop-shadow-[0_0_2px_rgba(0,0,0,0.8)] ${
                speed === s
                  ? "bg-cyan-400/40 text-cyan-100 border-cyan-300"
                  : "bg-transparent text-cyan-300/80 border-cyan-500/40 hover:border-cyan-300"
              }`}
            >
              {s}x
            </button>
          ))}
        </div>
        {stats.state === "playing" && (
          <button
            onClick={onPause}
            className="px-3 py-2 text-xs font-mono uppercase tracking-widest rounded-md border-2 border-fuchsia-400/70 bg-slate-950/80 text-fuchsia-200 hover:bg-fuchsia-500/30 transition drop-shadow-[0_0_2px_rgba(0,0,0,0.8)]"
            title="Press P to pause"
          >
            Pause
          </button>
        )}
        {stats.state === "paused" && (
          <button
            onClick={onResume}
            className="px-3 py-2 text-xs font-mono uppercase tracking-widest rounded-md border-2 border-emerald-400/70 bg-slate-950/80 text-emerald-200 hover:bg-emerald-500/30 transition drop-shadow-[0_0_2px_rgba(0,0,0,0.8)]"
            title="Press P to resume"
          >
            Resume
          </button>
        )}
        <button
          onClick={onShowDocs}
          className="px-3 py-2 text-xs font-mono uppercase tracking-widest rounded-md border-2 border-cyan-400/70 bg-slate-950/80 text-cyan-200 hover:bg-cyan-500/30 transition drop-shadow-[0_0_2px_rgba(0,0,0,0.8)]"
        >
          Design Doc
        </button>
        <button
          onClick={onReset}
          className="px-3 py-2 text-xs font-mono uppercase tracking-widest rounded-md border-2 border-rose-400/70 bg-slate-950/80 text-rose-200 hover:bg-rose-500/30 transition drop-shadow-[0_0_2px_rgba(0,0,0,0.8)]"
        >
          Reset
        </button>
      </div>

      {/* Wave progress bar */}
      <div className="pointer-events-auto mt-1">
        <div className="h-2 w-full bg-fuchsia-950/70 border-2 border-fuchsia-500/40 rounded overflow-hidden shadow-lg shadow-fuchsia-500/20">
          <div
            className="h-full bg-gradient-to-r from-cyan-400 via-fuchsia-400 to-rose-400 transition-all"
            style={{ width: `${wavePct}%` }}
          />
        </div>
        {stats.intermission && stats.intermissionLeft > 0 && (
          <div className="text-[10px] mt-1 font-mono text-cyan-300 tracking-widest drop-shadow-[0_0_2px_rgba(0,0,0,0.9)]">
            NEXT WAVE IN {stats.intermissionLeft.toFixed(1)}s • Press SPACE to start early
          </div>
        )}
      </div>

      {/* Boss bar */}
      {bossHp && (
        <div className="pointer-events-auto mt-2 mx-auto w-full max-w-2xl border-2 border-fuchsia-500/70 bg-slate-950/85 backdrop-blur-md rounded-md p-3 shadow-2xl shadow-fuchsia-500/30">
          <div className="flex justify-between text-[10px] font-mono tracking-widest text-fuchsia-200 mb-2 drop-shadow-[0_0_2px_rgba(0,0,0,0.9)]">
            <span>⚠️ OMEGA CORE TITAN — PHASE {bossHp.phase}/3</span>
            <span>{Math.ceil(bossHp.hp).toLocaleString()} / {bossHp.max.toLocaleString()}</span>
          </div>
          {/* Shield bar */}
          {bossHp.maxShield > 0 && (
            <div className="mb-1">
              <div className="flex justify-between text-[9px] font-mono text-cyan-300 mb-0.5 drop-shadow-[0_0_1px_rgba(0,0,0,0.9)]">
                <span>🛡️ SHIELD</span>
                <span>{Math.ceil(bossHp.shield).toLocaleString()} / {bossHp.maxShield.toLocaleString()}</span>
              </div>
              <div className="h-2.5 bg-cyan-950/80 rounded overflow-hidden border border-cyan-500/50">
                <div className="h-full bg-gradient-to-r from-cyan-300 to-blue-400 shadow-[0_0_10px_rgba(34,211,238,0.6)]" style={{ width: `${(bossHp.shield / bossHp.maxShield) * 100}%` }} />
              </div>
            </div>
          )}
          {/* HP bar */}
          <div className="mt-2">
            <div className="flex justify-between text-[9px] font-mono text-rose-300 mb-0.5 drop-shadow-[0_0_1px_rgba(0,0,0,0.9)]">
              <span>❤️ HULL INTEGRITY</span>
              <span>{Math.ceil(bossHp.hp).toLocaleString()} / {bossHp.max.toLocaleString()}</span>
            </div>
            <div className="h-3.5 bg-rose-950/80 rounded overflow-hidden border-2 border-rose-500/60">
              <div className="h-full bg-gradient-to-r from-rose-500 to-fuchsia-400 shadow-[0_0_10px_rgba(244,63,94,0.6)]" style={{ width: `${(bossHp.hp / bossHp.max) * 100}%` }} />
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

function Pill({ label, value, color, border, glow }: { label: string; value: any; color: string; border: string; glow: string }) {
  return (
    <div className={`px-3 py-2 rounded-md border ${border} bg-black/60 backdrop-blur-sm shadow-lg ${glow}`}>
      <div className="text-[9px] tracking-[0.2em] text-white/50">{label}</div>
      <div className={`text-lg font-mono leading-tight ${color}`}>{value}</div>
    </div>
  );
}
