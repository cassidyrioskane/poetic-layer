// frontend/src/App.js
import React, { useState } from "react";
import MotifManager from "./components/MotifManager";
import MappingManager from "./components/MappingManager";

export default function App() {
  const [lastOutput, setLastOutput] = useState(null);

  return (
    <div style={{ maxWidth: 1000, margin: "24px auto", fontFamily: "system-ui, sans-serif" }}>
      <h1>Poetic Layer</h1>

      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 24 }}>
        <div style={{ border: "1px solid #ccc", borderRadius: 8 }}>
          <MotifManager onRefresh={() => { /* hook available */ }} />
        </div>
        <div style={{ border: "1px solid #ccc", borderRadius: 8 }}>
          <MappingManager onNewOutput={setLastOutput} />
        </div>
      </div>

      <div style={{ marginTop: 24 }}>
        <h2>Last Output</h2>
        {!lastOutput ? (
          <p>No output yet</p>
        ) : (
          <div style={{ padding: 12, border: "1px solid #ddd", borderRadius: 8 }}>
            <div><strong>{lastOutput.name}</strong></div>
            <pre style={{ whiteSpace: "pre-wrap" }}>{lastOutput.text}</pre>
            <div style={{ color: "#666", marginTop: 8 }}>
              source: {lastOutput?.provenance?.source_ref || "unknown"}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
