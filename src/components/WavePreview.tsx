import type { WaveDef } from "../game/data/enemies";

interface Props {
  current: WaveDef | null;
  next: WaveDef | null;
  intermission: boolean;
  onStartNow: () => void;
}

export function WavePreview({ current, next, intermission, onStartNow }: Props) {
  const showWave = current ?? next;
  if (!showWave) return null;

  const display = intermission ? next : current;
  if (!display) return null;
  return (
    <div className="pointer-events-auto absolute left-4 top-32 w-72 z-20">
      <div className={`border-2 ${display.isBoss ? "border-fuchsia-400/80 bg-fuchsia-950/60" : "border-cyan-500/50 bg-slate-950/70"} backdrop-blur-md rounded-lg p-3 shadow-2xl ${display.isBoss ? "shadow-fuchsia-500/30" : "shadow-cyan-500/20"}`}>
        <div className="flex items-center justify-between">
          <div>
            <div className="text-[10px] font-mono tracking-widest text-white/60 drop-shadow-[0_0_2px_rgba(0,0,0,0.9)]">
              {intermission ? "// INCOMING" : "// CURRENT"}
            </div>
            <div className={`font-bold drop-shadow-[0_0_3px_rgba(0,0,0,0.9)] ${display.isBoss ? "text-fuchsia-200" : "text-cyan-100"}`}>
              {display.label}
            </div>
          </div>
          {intermission && (
            <button
              onClick={onStartNow}
              className="px-2 py-1 text-[10px] font-mono tracking-widest border-2 border-emerald-400/70 bg-emerald-500/20 text-emerald-200 rounded hover:bg-emerald-400/30 drop-shadow-[0_0_2px_rgba(0,0,0,0.8)]"
              title="Press SPACE to start early"
            >
              ▶ START
            </button>
          )}
        </div>

        <div className="mt-2">
          <div className="text-[9px] tracking-widest text-white/50 drop-shadow-[0_0_1px_rgba(0,0,0,0.8)]">ENEMY TYPES</div>
          <ul className="mt-1 space-y-0.5">
            {display.preview.map((p, i) => (
              <li key={i} className="text-xs text-white/90 font-mono flex items-center gap-1.5 drop-shadow-[0_0_1px_rgba(0,0,0,0.8)]">
                <span className="text-cyan-300">▸</span> {p}
              </li>
            ))}
          </ul>
        </div>

        {display.resistances.length > 0 && (
          <div className="mt-2">
            <div className="text-[9px] tracking-widest text-white/50 drop-shadow-[0_0_1px_rgba(0,0,0,0.8)]">RESISTANCES</div>
            <div className="flex flex-wrap gap-1 mt-1">
              {display.resistances.map((r, i) => (
                <span key={i} className="text-[10px] px-1.5 py-0.5 rounded border-2 border-rose-400/50 bg-rose-500/20 text-rose-200 font-mono drop-shadow-[0_0_2px_rgba(0,0,0,0.8)]">
                  {r}
                </span>
              ))}
            </div>
          </div>
        )}

        <div className="mt-2 text-[10px] font-mono text-amber-200 drop-shadow-[0_0_2px_rgba(0,0,0,0.8)]">
          REWARD ⬢ {display.reward}
        </div>
      </div>
    </div>
  );
}
