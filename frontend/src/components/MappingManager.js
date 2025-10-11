import React, { useEffect, useMemo, useState } from "react";
import { getMotifs, getMappings, getRegistryMappings, createMapping, runMapping } from "../api";

export default function MappingManager({ onNewOutput, refreshSignal }) {
  const [motifs, setMotifs] = useState([]);
  const [mappingSpecs, setMappingSpecs] = useState([]);     // saved/spec’d mappings (unchanged)
  const [registry, setRegistry] = useState([]);             // discovered mapping functions (with docstrings)
  const [selectedMotif, setSelectedMotif] = useState("");
  const [selectedMapping, setSelectedMapping] = useState("");
  const [mergeMotif, setMergeMotif] = useState("");         // for motif_merge / mycelial_spread
  const [message, setMessage] = useState("");

  // Load motifs, registry, and saved specs
  const loadAll = async () => {
    try {
      const [ms, reg, specs] = await Promise.all([
        getMotifs(),
        getRegistryMappings(),
        getMappings(),       // keep your existing specs list
      ]);
      setMotifs(ms);
      setRegistry(reg);
      setMappingSpecs(specs);
      if (ms.length === 0) setMessage("No motifs available yet.");
      else setMessage("");
    } catch (e) {
      setMessage(`❌ ${e.message}`);
    }
  };

  useEffect(() => {
    loadAll();
  }, [refreshSignal]);

  const motifMap = useMemo(() => {
    const map = {};
    for (const m of motifs) map[m.id] = m;
    return map;
  }, [motifs]);

  const handleCreateSpec = async () => {
    if (!selectedMotif || !selectedMapping) {
      setMessage("❌ Select both a motif and a mapping.");
      return;
    }
    try {
      const spec = await createMapping({
        type: selectedMapping,
        signature: { input_motif_id: selectedMotif },
        params_schema: {},
        constraints: {},
        tests: [],
        version: "1.0",
      });
      setMappingSpecs((prev) => [...prev, spec]);
      setMessage("✅ Mapping spec saved");
    } catch (e) {
      setMessage(`❌ ${e.message}`);
    }
  };

  const handleRun = async () => {
    if (!selectedMotif || !selectedMapping) {
      setMessage("❌ Select both a motif and a mapping.");
      return;
    }
    try {
      const params = {};
      if (selectedMapping === "motif_merge" || selectedMapping === "mycelial_spread") {
        if (!mergeMotif) {
          setMessage("❌ Choose a second motif for this mapping.");
          return;
        }
        const other = motifMap[mergeMotif];
        params.other_text = other?.content ?? other?.text ?? "";
      }

      const payload = {
        type: selectedMapping,
        signature: { input_motif_id: selectedMotif },
        params,
      };

      const res = await runMapping(payload);
      onNewOutput?.(res.output);
      setMessage("✅ Mapping executed");
      await loadAll();
    } catch (e) {
      setMessage(`❌ ${e.message}`);
    }
  };

  // Optional: filter available registry mappings by motif type (text vs image) if desired.
  // For now, show all registered mappings; visual ones will no-op on text unless implemented to guard.

  return (
    <div style={{ padding: 12 }}>
      <h2>Mappings</h2>

      {message && <p>{message}</p>}

      <div style={{ display: "grid", gap: 8, gridTemplateColumns: "1fr" }}>
        {/* Input motif selector (restored) */}
        <label>
          Input motif:
          <select
            value={selectedMotif}
            onChange={(e) => setSelectedMotif(e.target.value)}
            style={{ marginLeft: 8, minWidth: 280 }}
          >
            <option value="">-- choose motif --</option>
            {motifs.map((m) => (
              <option key={m.id} value={m.id}>
                {m.name}
              </option>
            ))}
          </select>
          <button
            style={{ marginLeft: 8 }}
            type="button"
            onClick={loadAll}
            title="Refresh lists"
          >
            ↻ Refresh
          </button>
        </label>

        {/* Mapping selector with hover tooltips from registry */}
        <label>
          Mapping type:
          <select
            value={selectedMapping}
            onChange={(e) => setSelectedMapping(e.target.value)}
            style={{ marginLeft: 8, minWidth: 280 }}
          >
            <option value="">-- choose mapping --</option>
            {registry.map((m) => (
              <option key={m.type} value={m.type} title={m.description}>
                {m.type.replaceAll("_", " ")}
              </option>
            ))}
          </select>
        </label>

        {/* Parameter inputs for mappings that need a second motif */}
        {(selectedMapping === "motif_merge" || selectedMapping === "mycelial_spread") && (
          <label>
            Second motif:
            <select
              value={mergeMotif}
              onChange={(e) => setMergeMotif(e.target.value)}
              style={{ marginLeft: 8, minWidth: 280 }}
            >
              <option value="">-- choose motif to merge with --</option>
              {motifs
                .filter((m) => m.id !== selectedMotif)
                .map((m) => (
                  <option key={m.id} value={m.id}>
                    {m.name}
                  </option>
                ))}
            </select>
          </label>
        )}

        <div style={{ display: "flex", gap: 8, marginTop: 8 }}>
          <button onClick={handleCreateSpec}>Save Mapping Spec</button>
          <button onClick={handleRun}>Run Mapping</button>
        </div>
      </div>

      {/* Existing saved mapping specs (unchanged feature) */}
      <h3 style={{ marginTop: 16 }}>Existing Specs</h3>
      {mappingSpecs.length === 0 ? (
        <p>No mapping specs yet</p>
      ) : (
        <ul>
          {mappingSpecs.map((s) => (
            <li key={s.id || `${s.type}-${s.signature?.input_motif_id || ""}`}>
              <code>{s.type}</code> on motif <code>{s.signature?.input_motif_id}</code>
              {s.signature?.input_motif_id &&
                motifMap[s.signature.input_motif_id] &&
                ` (${motifMap[s.signature.input_motif_id].name})`}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
