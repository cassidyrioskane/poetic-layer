import React, { useState } from "react";
import MotifManager from "./components/MotifManager";
import MappingManager from "./components/MappingManager";

export default function App() {
  const [view, setView] = useState("motifs");

  return (
    <div className="max-w-2xl mx-auto mt-8">
      <div className="flex space-x-4 mb-6">
        <button
          onClick={() => setView("motifs")}
          className={`px-4 py-2 rounded ${
            view === "motifs" ? "bg-blue-600 text-white" : "bg-gray-200"
          }`}
        >
          Motifs
        </button>
        <button
          onClick={() => setView("mappings")}
          className={`px-4 py-2 rounded ${
            view === "mappings" ? "bg-blue-600 text-white" : "bg-gray-200"
          }`}
        >
          Mappings
        </button>
      </div>

      {view === "motifs" && <MotifManager />}
      {view === "mappings" && <MappingManager />}
    </div>
  );
}
