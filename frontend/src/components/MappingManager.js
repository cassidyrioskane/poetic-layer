// frontend/src/components/MappingManager.js
import React, { useEffect, useMemo, useState } from "react";
import { getMotifs, getMappings, createMapping, runMapping } from "../api";

// Built-in and Poetic Layer mapping types
const BUILTIN_TYPES = [
  // Core demos
  { value: "uppercase", label: "Uppercase (demo)" },
  { value: "append", label: "Append Text (demo)" },
  { value: "echo", label: "Echo (demo)" },
  // Linguistic
  { value: "reverse", label: "Reverse Text" },
  { value: "mirror", label: "Mirror Text" },
  { value: "titlecase", label: "Title Case" },
  { value: "mutate", label: "Vowel Mutation" },
  { value: "summarize", label: "Summarize (first 8 words)" },
  { value: "invert_case", label: "Invert Case" },
  // Poetic
  { value: "resonance", label: "Resonance" },
  { value: "echo_chamber", label: "Echo Chamber" },
  { value: "ethical_mirror", label: "Ethical Mirror" },
  { value: "motif_merge", label: "Motif Merge" },
  { value: "temporal_distortion", label: "Temporal Distortion" },
  { value: "dream_sequence", label: "Dream Sequence" },
];

export default function MappingManager({ onNewOutput, refreshSignal }) {
  const [motifs, setMotifs] = useState([]);
  const [mappings, setMappings] = useState([]);
  const [selectedMotif, setSelectedMotif] = useState("");
  const [mappingType, setMappingType] = useState("uppercase");
  const [appendText, setAppendText] = useState("");
  const [mergeMotif, setMergeMotif] = useState("");
  const [message, setMessage] = useState("");

  // --- Load motifs and mapping specs ---
  const load = async () => {
    try {
      const [ms, specs] = await Promise.all([getMotifs(), getMappings()]);
      setMotifs(ms);
      setMappings(specs);
      if (ms.length === 0) setMessage("No motifs available yet.");
      else setMessage("");
    } catch (e) {
      setMessage(`❌ ${e.message}`);
    }
  };

  // --- Load on mount and when refreshSignal changes ---
  useEffect(() => {
    load();
  }, [refreshSignal]);

  // --- Derived map for display ---
  const motifMap = useMemo(() => {
    const map = {};
    for (const m of motifs) map[m.id] = m;
    return map;
  }, [motifs]);

  // --- Create new mapping spec ---
  const handleCreateSpec = async () => {
    if (!selectedMotif) {
      setMessage("❌ Select a motif first");
      return;
    }
    try {
      const spec = await createMapping({
        type: mappingType,
        signature: { input_motif_id: selectedMotif },
        params_schema: {},
        constraints: {},
        tests: [],
        version: "1.0",
      });
      setMappings((prev) => [...prev, spec]);
      setMessage("✅ Mapping spec saved");
    } catch (e) {
      setMessage(`❌ ${e.message}`);
    }
  };

  // --- Run mapping on selected motif ---
  const handleRun = async () => {
    if (!selectedMotif) {
      setMessage("❌ Select a motif first");
      return;
    }

    try {
      // build params dynamically
      const params = {};
      if (mappingType === "append") params.append_text = appendText;
      if (mappingType === "motif_merge") params.other_motif_id = mergeMotif;

      const payload = {
        type: mappingType,
        signature: { input_motif_id: selectedMotif },
        params,
      };

      const res = await runMapping(payload);
      onNewOutput?.(res.output);
      setMessage("✅ Mapping executed");
      await load();
    } catch (e) {
      setMessage(`❌ ${e.message}`);
    }
  };

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
            <option value="">-- choose --</option>
            {motifs.map((m) => (
              <option key={m.id} value={m.id}>
                {m.name}
              </option>
            ))}
          </select>
          <button
            style={{ marginLeft: 8 }}
            type="button"
            onClick={load}
            title="Refresh motifs list"
          >
            ↻ Refresh Motifs
          </button>
        </label>

        {/* Mapping type selector */}
        <label>
          Mapping type:
          <select
            value={mappingType}
            onChange={(e) => setMappingType(e.target.value)}
            style={{ marginLeft: 8 }}
          >
            {BUILTIN_TYPES.map((t) => (
              <option key={t.value} value={t.value}>
                {t.label}
              </option>
            ))}
          </select>
        </label>

        {/* Parameter inputs for specific mappings */}
        {mappingType === "append" && (
          <label>
            Append text:
            <input
              value={appendText}
              onChange={(e) => setAppendText(e.target.value)}
              style={{ marginLeft: 8, width: "60%" }}
              placeholder="(demo) text to append"
            />
          </label>
        )}

        {mappingType === "motif_merge" && (
          <label>
            Merge with motif:
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

        {/* Buttons */}
        <div style={{ display: "flex", gap: 8, marginTop: 8 }}>
          <button onClick={handleCreateSpec}>Save Mapping Spec</button>
          <button type="button" onClick={handleRun}>Run Mapping</button>
        </div>
      </div>

      {/* Mapping specs list */}
      <h3 style={{ marginTop: 16 }}>Existing Specs</h3>
      {mappings.length === 0 ? (
        <p>No mapping specs yet</p>
      ) : (
        <ul>
          {mappings.map((s) => (
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
