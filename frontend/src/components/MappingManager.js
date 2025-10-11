import React, { useEffect, useMemo, useState } from "react";
import {
  getMotifs,
  getMappings,
  getRegistryMappings,
  createMapping,
  runMapping,
} from "../api";

export default function MappingManager({ onNewOutput, refreshSignal }) {
  const [motifs, setMotifs] = useState([]);
  const [mappingSpecs, setMappingSpecs] = useState([]);
  const [registry, setRegistry] = useState([]);
  const [selectedMotif, setSelectedMotif] = useState("");
  const [selectedMapping, setSelectedMapping] = useState("");
  const [mergeMotif, setMergeMotif] = useState("");
  const [message, setMessage] = useState("");

  // --- Load motifs + registry + saved specs ---
  const loadAll = async () => {
    try {
      const [ms, reg, specs] = await Promise.all([
        getMotifs(),
        getRegistryMappings(),
        getMappings(),
      ]);
      setMotifs(ms);
      setRegistry(reg);
      setMappingSpecs(specs);
      setMessage(ms.length ? "" : "No motifs available yet.");
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

  // --- Filter registry mappings based on motif type ---
  const selectedMotifType = selectedMotif
    ? motifMap[selectedMotif]?.type || "text"
    : "text";

  const filteredRegistry = registry.filter((m) => {
    if (!m.domain) return true; // fallback if backend hasn't tagged it yet
    return m.domain === (selectedMotifType === "image" ? "image" : "text");
  });


  // --- Create spec ---
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

  // --- Run mapping ---
  const handleRun = async () => {
    if (!selectedMotif || !selectedMapping) {
      setMessage("❌ Select both a motif and a mapping.");
      return;
    }
    try {
      const params = {};
      if (["motif_merge", "mycelial_spread"].includes(selectedMapping)) {
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

  // --- UI rendering ---
  return (
    <div style={{ padding: 12 }}>
      <h2>Mappings</h2>
      {message && <p>{message}</p>}

      <div style={{ display: "grid", gap: 8, gridTemplateColumns: "1fr" }}>
        {/* Input motif selector */}
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
                {m.name} ({m.type})
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

        {/* Thumbnail preview for image motifs */}
        {selectedMotif && motifMap[selectedMotif]?.type === "image" && (
          <div style={{ marginTop: 8 }}>
            <img
              src={`data:image/png;base64,${motifMap[selectedMotif].content}`}
              alt={motifMap[selectedMotif].name}
              style={{
                maxWidth: "100%",
                maxHeight: 200,
                border: "1px solid #ccc",
                borderRadius: 6,
              }}
            />
          </div>
        )}

        {/* Mapping selector with hover tooltip */}
        <label>
          Mapping type:
          <select
            value={selectedMapping}
            onChange={(e) => setSelectedMapping(e.target.value)}
            style={{ marginLeft: 8, minWidth: 280 }}
          >
            <option value="">-- choose mapping --</option>
            {filteredRegistry.map((m) => (
              <option key={m.type} value={m.type} title={m.description}>
                {m.type.replaceAll("_", " ")}
              </option>
            ))}
          </select>
        </label>

        {/* Parameter inputs for merge-style mappings */}
        {["motif_merge", "mycelial_spread"].includes(selectedMapping) && (
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

      {/* Existing mapping specs */}
      <h3 style={{ marginTop: 16 }}>Existing Specs</h3>
      {mappingSpecs.length === 0 ? (
        <p>No mapping specs yet</p>
      ) : (
        <ul>
          {mappingSpecs.map((s) => (
            <li
              key={s.id || `${s.type}-${s.signature?.input_motif_id || ""}`}
            >
              <code>{s.type}</code> on motif{" "}
              <code>{s.signature?.input_motif_id}</code>
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
