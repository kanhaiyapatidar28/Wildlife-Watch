'use client';

import React, { useState, useMemo } from 'react';
import { AppLayout } from '@/components/layout/AppLayout';
import { MOCK_HOTSPOTS } from '@/lib/mock-data';
import { ChangeEventHotspot } from '@/types';
import {
  HotspotFilters,
  HotspotFilterState,
} from '@/components/hotspots/HotspotFilters';
import { HotspotTable } from '@/components/hotspots/HotspotTable';
import { HotspotMapPane } from '@/components/hotspots/HotspotMapPane';
import { HotspotDetailDrawer } from '@/components/hotspots/HotspotDetailDrawer';
import {
  Flame,
  ShieldAlert,
  AlertTriangle,
  Layers,
  Activity,
  CheckCircle2,
  Download,
} from 'lucide-react';

const INITIAL_FILTERS: HotspotFilterState = {
  search: '',
  changeType: 'ALL',
  severity: 'ALL',
  dateRange: 'ALL',
  areaId: 'ALL',
  minConfidence: 0,
};

export default function HotspotsPage() {
  const [filters, setFilters] = useState<HotspotFilterState>(INITIAL_FILTERS);
  const [selectedHotspot, setSelectedHotspot] = useState<ChangeEventHotspot | null>(
    MOCK_HOTSPOTS[0] || null
  );
  const [isDrawerOpen, setIsDrawerOpen] = useState(false);

  // Filter computation
  const filteredHotspots = useMemo(() => {
    return MOCK_HOTSPOTS.filter((hs) => {
      // 1. Text search
      if (filters.search) {
        const query = filters.search.toLowerCase();
        const matchesId = hs.id.toLowerCase().includes(query);
        const matchesArea = hs.area_name.toLowerCase().includes(query);
        const matchesLocation = (hs.location_detail || '').toLowerCase().includes(query);
        const matchesType = hs.change_type.toLowerCase().includes(query);
        if (!matchesId && !matchesArea && !matchesLocation && !matchesType) {
          return false;
        }
      }

      // 2. Change Type filter
      if (filters.changeType !== 'ALL') {
        if (filters.changeType === 'VEGETATION_LOSS') {
          if (
            hs.change_type !== 'VEGETATION_LOSS' &&
            hs.change_type !== 'DEFORESTATION' &&
            hs.change_type !== 'CANOPY_THINNING'
          ) {
            return false;
          }
        } else if (filters.changeType === 'URBAN_EXPANSION') {
          if (hs.change_type !== 'URBAN_EXPANSION' && hs.change_type !== 'ENCROACHMENT') {
            return false;
          }
        } else if (filters.changeType === 'FIRE') {
          if (hs.change_type !== 'FIRE' && hs.change_type !== 'BURN_SCAR') {
            return false;
          }
        } else if (filters.changeType === 'WATER_LOSS') {
          if (hs.change_type !== 'WATER_LOSS') {
            return false;
          }
        } else if (filters.changeType === 'OTHER') {
          if (hs.change_type !== 'OTHER') {
            return false;
          }
        }
      }

      // 3. Severity filter
      if (filters.severity !== 'ALL' && hs.severity !== filters.severity) {
        return false;
      }

      // 4. Area filter
      if (filters.areaId !== 'ALL' && hs.area_id !== filters.areaId) {
        return false;
      }

      // 5. Confidence filter
      if (filters.minConfidence > 0 && hs.confidence_score * 100 < filters.minConfidence) {
        return false;
      }

      // 6. Date Range filter (mock relative filter)
      if (filters.dateRange !== 'ALL') {
        const detectedTime = new Date(hs.detected_at).getTime();
        const now = new Date('2026-09-18T12:00:00Z').getTime();
        const diffHours = (now - detectedTime) / (1000 * 60 * 60);

        if (filters.dateRange === '24H' && diffHours > 24) return false;
        if (filters.dateRange === '7D' && diffHours > 24 * 7) return false;
        if (filters.dateRange === '30D' && diffHours > 24 * 30) return false;
        if (filters.dateRange === '90D' && diffHours > 24 * 90) return false;
      }

      return true;
    });
  }, [filters]);

  // Handle row click: zoom map, open popup, and reveal detail drawer
  const handleSelectHotspot = (hs: ChangeEventHotspot) => {
    setSelectedHotspot(hs);
    setIsDrawerOpen(true);
  };

  const handleMapMarkerSelect = (hs: ChangeEventHotspot) => {
    setSelectedHotspot(hs);
  };

  const handleOpenDrawerFromMap = (hs: ChangeEventHotspot) => {
    setSelectedHotspot(hs);
    setIsDrawerOpen(true);
  };

  // KPI Calculations
  const criticalCount = filteredHotspots.filter((h) => h.severity === 'CRITICAL').length;
  const highCount = filteredHotspots.filter((h) => h.severity === 'HIGH').length;
  const totalAreaHa = filteredHotspots.reduce((acc, h) => acc + h.area_ha, 0);

  return (
    <AppLayout>
      <div className="space-y-5 max-w-[1600px] mx-auto pb-10">
        {/* ========================================================================= */}
        {/* HEADER & QUICK KPIS */}
        {/* ========================================================================= */}
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-slate-800 pb-4">
          <div>
            <div className="flex items-center gap-2 text-xs font-mono text-amber-400 font-semibold uppercase tracking-wider mb-1">
              <Flame className="w-3.5 h-3.5" />
              <span>Real-Time Geospatial Incident Tracker</span>
            </div>
            <h1 className="text-2xl font-bold tracking-tight text-white font-mono flex items-center gap-2.5">
              <ShieldAlert className="w-6 h-6 text-amber-400" />
              <span>HABITAT CHANGE HOTSPOTS & SEVERITY CLASSIFICATION</span>
            </h1>
            <p className="text-xs text-slate-400 mt-1">
              Vectorized degradation clusters ranked by canopy loss rate, spectral anomalies & remote sensing confidence
            </p>
          </div>

          {/* Quick Stats Pill Row */}
          <div className="flex items-center gap-2.5 flex-wrap">
            <div className="px-3 py-1.5 rounded-lg bg-red-950/60 border border-red-500/30 text-xs font-mono text-red-300 flex items-center gap-2">
              <span className="w-2 h-2 rounded-full bg-red-500 animate-pulse" />
              <span>Critical: <strong className="text-white font-bold">{criticalCount}</strong></span>
            </div>
            <div className="px-3 py-1.5 rounded-lg bg-orange-950/60 border border-orange-500/30 text-xs font-mono text-orange-300 flex items-center gap-2">
              <span className="w-2 h-2 rounded-full bg-orange-500" />
              <span>High: <strong className="text-white font-bold">{highCount}</strong></span>
            </div>
            <div className="px-3 py-1.5 rounded-lg bg-slate-900 border border-slate-800 text-xs font-mono text-slate-300 flex items-center gap-2">
              <Layers className="w-3.5 h-3.5 text-emerald-400" />
              <span>Affected: <strong className="text-emerald-400">{totalAreaHa.toFixed(1)} ha</strong></span>
            </div>
          </div>
        </div>

        {/* ========================================================================= */}
        {/* TOP FILTERS TOOLBAR */}
        {/* ========================================================================= */}
        <HotspotFilters
          filters={filters}
          onFilterChange={setFilters}
          onReset={() => setFilters(INITIAL_FILTERS)}
          activeCount={filteredHotspots.length}
          totalCount={MOCK_HOTSPOTS.length}
        />

        {/* ========================================================================= */}
        {/* MAIN SPLIT WORKSPACE (LEFT: TABLE, RIGHT: MAP) */}
        {/* ========================================================================= */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-5 items-start">
          {/* LEFT: HOTSPOT TABLE (7 COLS ON LARGE) */}
          <div className="lg:col-span-7 h-[680px]">
            <HotspotTable
              hotspots={filteredHotspots}
              selectedHotspotId={selectedHotspot?.id || null}
              onSelectHotspot={handleSelectHotspot}
            />
          </div>

          {/* RIGHT: INTERACTIVE MAP PANE (5 COLS ON LARGE) */}
          <div className="lg:col-span-5 h-[680px]">
            <HotspotMapPane
              hotspots={filteredHotspots}
              selectedHotspot={selectedHotspot}
              onSelectHotspot={handleMapMarkerSelect}
              onOpenDrawer={handleOpenDrawerFromMap}
            />
          </div>
        </div>

        {/* ========================================================================= */}
        {/* SLIDE-OUT HOTSPOT DETAIL DRAWER */}
        {/* ========================================================================= */}
        <HotspotDetailDrawer
          hotspot={selectedHotspot}
          isOpen={isDrawerOpen}
          onClose={() => setIsDrawerOpen(false)}
        />
      </div>
    </AppLayout>
  );
}
