import Link from 'next/link';
import {
  ShieldAlert,
  Compass,
  Layers,
  Flame,
  Satellite,
  ArrowRight,
  Eye,
  CheckCircle2,
  TreePine,
  Activity,
} from 'lucide-react';

export default function HomePage() {
  return (
    <div className="min-h-screen bg-gis-dark text-slate-100 flex flex-col">
      {/* Navigation Header */}
      <header className="h-16 border-b border-slate-800/80 bg-gis-surface/90 backdrop-blur px-8 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 rounded-lg bg-emerald-950/90 border border-emerald-500/60 flex items-center justify-center text-emerald-400">
            <TreePine className="w-4 h-4" />
          </div>
          <span className="font-mono font-bold tracking-wider text-sm text-white">
            WILDLIFE WATCH
          </span>
          <span className="text-[11px] px-2 py-0.5 rounded bg-emerald-950/60 border border-emerald-500/30 text-emerald-300 font-mono">
            GEO-INTELLIGENCE v1.0
          </span>
        </div>

        <div className="flex items-center gap-4">
          <Link
            href="/login"
            className="text-xs font-medium text-slate-300 hover:text-white transition-colors"
          >
            Ranger Sign In
          </Link>
          <Link
            href="/dashboard"
            className="px-3.5 py-1.5 rounded-lg bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-medium flex items-center gap-1.5 transition-colors shadow-lg shadow-emerald-950/50"
          >
            <span>Launch Platform</span>
            <ArrowRight className="w-3.5 h-3.5" />
          </Link>
        </div>
      </header>

      {/* Hero Section */}
      <main className="flex-1 flex flex-col justify-center items-center px-6 py-16 text-center max-w-5xl mx-auto">
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-slate-900 border border-slate-800 text-xs text-slate-300 mb-6 font-mono">
          <Satellite className="w-3.5 h-3.5 text-emerald-400 animate-spin" style={{ animationDuration: '10s' }} />
          <span>Real-Time Sentinel-2 & Landsat-9 Ingestion</span>
        </div>

        <h1 className="text-4xl md:text-6xl font-extrabold tracking-tight text-white mb-6 leading-tight">
          Wildlife Habitat Monitoring &{' '}
          <span className="text-emerald-400 underline decoration-emerald-500/40 underline-offset-8">
            Change Detection
          </span>
        </h1>

        <p className="text-base md:text-lg text-slate-400 max-w-2xl mb-10">
          Empowering conservation teams and national park authorities with autonomous multi-spectral satellite telemetry, canopy loss alerts, and threat boundary intelligence.
        </p>

        <div className="flex flex-wrap items-center justify-center gap-4 mb-16">
          <Link
            href="/dashboard"
            className="px-6 py-3 rounded-lg bg-emerald-600 hover:bg-emerald-500 text-white text-sm font-semibold flex items-center gap-2 shadow-xl shadow-emerald-900/30 transition-colors"
          >
            <span>Open Intelligence Dashboard</span>
            <ArrowRight className="w-4 h-4" />
          </Link>
          <Link
            href="/explore"
            className="px-6 py-3 rounded-lg bg-slate-900 hover:bg-slate-800 border border-slate-800 text-slate-200 text-sm font-semibold flex items-center gap-2 transition-colors"
          >
            <Compass className="w-4 h-4 text-emerald-400" />
            <span>Interactive Map Explorer</span>
          </Link>
        </div>

        {/* Feature Grid */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 text-left w-full">
          <div className="gis-glass-card p-6 rounded-xl border border-slate-800/80">
            <div className="w-10 h-10 rounded-lg bg-slate-900 border border-slate-800 flex items-center justify-center text-emerald-400 mb-4">
              <Layers className="w-5 h-5" />
            </div>
            <h3 className="text-sm font-bold text-white mb-2 font-mono">SPECTRAL INDICES</h3>
            <p className="text-xs text-slate-400 leading-relaxed">
              Automated computing of cloud-masked NDVI (vegetation), NDWI (water bodies), and NDBI (built-up encroachment).
            </p>
          </div>

          <div className="gis-glass-card p-6 rounded-xl border border-slate-800/80">
            <div className="w-10 h-10 rounded-lg bg-slate-900 border border-slate-800 flex items-center justify-center text-amber-400 mb-4">
              <Flame className="w-5 h-5" />
            </div>
            <h3 className="text-sm font-bold text-white mb-2 font-mono">FIRE HOTSPOTS</h3>
            <p className="text-xs text-slate-400 leading-relaxed">
              NASA FIRMS 375m thermal anomaly ingestion detecting active wildfire fronts and charcoal kilns inside reserve boundaries.
            </p>
          </div>

          <div className="gis-glass-card p-6 rounded-xl border border-slate-800/80">
            <div className="w-10 h-10 rounded-lg bg-slate-900 border border-slate-800 flex items-center justify-center text-red-400 mb-4">
              <ShieldAlert className="w-5 h-5" />
            </div>
            <h3 className="text-sm font-bold text-white mb-2 font-mono">VECTORIZED ALERTS</h3>
            <p className="text-xs text-slate-400 leading-relaxed">
              DBSCAN spatial clustering vectorizing pixel-level canopy loss into discrete polygon incident records with severity tags.
            </p>
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="h-14 border-t border-slate-800/60 bg-gis-surface/50 px-8 flex items-center justify-between text-xs text-slate-500">
        <div>Protected Area Database: WDPA 2026 Compatible</div>
        <div>Wildlife Habitat Monitoring Platform • Enterprise Edition</div>
      </footer>
    </div>
  );
}
