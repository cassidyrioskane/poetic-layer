import React, { useEffect, useState } from "react";
import { getMappings, createMapping, getMotifs } from "../api";
import { v4 as uuidv4 } from "uuid";

export default function MappingManager() {
  const [mappings, setMappings] = useState([]);
  const [motifs, setMotifs] = useState([]);
  const [newMapping, setNewMapping] = useState({
    motif_id: "",
    type: "ode",
  });

  useEffect(() => {
    // Load existing mappings and motifs
    const fetchData = async () => {
      try {
        const [mappingsData, motifsData] = await Promise.all([
          getMappings(),
          getMotifs(),
        ]);
        setMappings(mappingsData);
        setMotifs(motifsData);
      } catch (err) {
        console.error("Error loading data:", err);
      }
    };
    fetchData();
  }, []);

  const handleCreate = async () => {
    if (!newMapping.motif_id) {
      alert("Please select a motif before creating a mapping.");
      return;
    }

    const mappingPayload = {
      id: uuidv4(),
      motif_id: newMapping.motif_id,
      type: newMapping.type,
      signature: {},
      constraints: {},
      codegen_ref: "default_codegen",
      params_schema: {},
      tests: [],
      score: 0,
      version: "1.0",
    };

    try {
      const created = await createMapping(mappingPayload);
      setMappings([...mappings, created]);
      setNewMapping({ motif_id: "", type: "ode" });
    } catch (err) {
      console.error("Error creating mapping:", err);
      alert("Failed to create mapping. Check the console for details.");
    }
  };

  return (
    <div className="p-4">
      <h2 className="text-xl font-bold mb-4">Mapping Manager</h2>

      {/* Create New Mapping */}
      <div className="mb-6 space-y-3">
        <h3 className="font-semibold">Create New Mapping</h3>

        <div>
          <label className="block mb-1 text-sm">Motif</label>
          <select
            className="border rounded p-2 w-full"
            value={newMapping.motif_id}
            onChange={(e) =>
              setNewMapping({ ...newMapping, motif_id: e.target.value })
            }
          >
            <option value="">Select a motif</option>
            {motifs.map((m) => (
              <option key={m.id} value={m.id}>
                {m.name}
              </option>
            ))}
          </select>
        </div>

        <div>
          <label className="block mb-1 text-sm">Mapping Type</label>
          <select
            className="border rounded p-2 w-full"
            value={newMapping.type}
            onChange={(e) =>
              setNewMapping({ ...newMapping, type: e.target.value })
            }
          >
            <option value="ode">ODE</option>
            <option value="pde">PDE</option>
            <option value="bc">Boundary Condition</option>
            <option value="regularizer">Regularizer</option>
            <option value="data_labeler">Data Labeler</option>
            <option value="search_operator">Search Operator</option>
          </select>
        </div>

        <button
          onClick={handleCreate}
          className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
        >
          Create Mapping
        </button>
      </div>

      {/* List Mappings */}
      <div>
        <h3 className="font-semibold mb-2">Existing Mappings</h3>
        {mappings.length === 0 ? (
          <p className="text-gray-500">No mappings yet.</p>
        ) : (
          <ul className="space-y-2">
            {mappings.map((mapping) => {
              const motif = motifs.find((m) => m.id === mapping.motif_id);
              return (
                <li
                  key={mapping.id}
                  className="border rounded p-2 flex justify-between items-center"
                >
                  <div>
                    <strong>{motif ? motif.name : "Unknown Motif"}</strong> →{" "}
                    {mapping.type}
                  </div>
                  <div className="text-xs text-gray-500">v{mapping.version}</div>
                </li>
              );
            })}
          </ul>
        )}
      </div>
    </div>
  );
}
