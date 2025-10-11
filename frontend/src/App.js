import React, { useState } from "react";
import MotifManager from "./components/MotifManager";
import MappingManager from "./components/MappingManager";

export default function App() {
  const [refreshTick, setRefreshTick] = useState(0);
  const [lastOutput, setLastOutput] = useState(null);

  const handleRefresh = () => setRefreshTick((n) => n + 1);
  const handleNewOutput = (motif) => {
    // store newest motif so Last Output renders its content correctly
    setLastOutput(motif || null);
    // optional: scroll to output panel
    setTimeout(() => {
      const el = document.getElementById("last-output");
      if (el) el.scrollIntoView({ behavior: "smooth", block: "start" });
    }, 10);
  };

  return (
    <div style={{ padding: 16, fontFamily: "system-ui, sans-serif" }}>
      <h1 style={{ marginBottom: 16 }}>Poetic Layer</h1>

      <div
        style={{
          display: "grid",
          gridTemplateColumns: "1fr 1fr",
          gap: 16,
          alignItems: "start",
        }}
      >
        <div style={{ border: "1px solid #ddd", borderRadius: 6, padding: 12 }}>
          <MotifManager onRefresh={handleRefresh} />
        </div>

        <div style={{ border: "1px solid #ddd", borderRadius: 6, padding: 12 }}>
          <MappingManager
            refreshSignal={refreshTick}
            onNewOutput={handleNewOutput}
          />
        </div>
      </div>

      <section id="last-output" style={{ marginTop: 24 }}>
        <h2>Last Output</h2>
        {!lastOutput ? (
          <p>No output yet</p>
        ) : (
          <div
            style={{
              border: "1px solid #eee",
              borderRadius: 6,
              padding: 12,
              background: "#fafafa",
            }}
          >
            <div style={{ marginBottom: 8 }}>
              <strong>Name:</strong> {lastOutput.name || "(untitled)"}
            </div>
            <div style={{ marginBottom: 8 }}>
              <strong>ID:</strong> {lastOutput.id}
              {lastOutput?.provenance?.source_ref && (
                <>
                  {" "}
                  <span style={{ marginLeft: 8 }}>
                    <strong>Source:</strong> {lastOutput.provenance.source_ref}
                  </span>
                </>
              )}
            </div>

            {/* 🔑 Render the body correctly for both text and image motifs */}
            {lastOutput.type === "image" ? (
              <div style={{ marginTop: 8 }}>
                <img
                  alt={lastOutput.name || "image motif"}
                  src={`data:image/png;base64,${lastOutput.content || ""}`}
                  style={{ maxWidth: "100%", height: "auto", display: "block" }}
                />
              </div>
            ) : (
              <pre
                style={{
                  whiteSpace: "pre-wrap",
                  wordBreak: "break-word",
                  marginTop: 8,
                  fontFamily: "inherit",
                  background: "white",
                  border: "1px solid #eaeaea",
                  borderRadius: 4,
                  padding: 10,
                }}
              >
                {lastOutput.content ?? lastOutput.text ?? ""}
              </pre>
            )}
          </div>
        )}
      </section>
    </div>
  );
}
