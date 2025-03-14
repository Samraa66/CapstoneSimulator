import React, { useEffect, useState } from "react";
import { MapContainer, TileLayer, Polyline } from "react-leaflet";
import "leaflet/dist/leaflet.css";

const getLineWeight = (color) => {
  if (color === "red") return 5; // 🚨 High increase needed
  if (color === "orange") return 4; // ⚠️ Moderate increase needed
  return 3; // ✅ Normal routes
};

const ReplacedTrainMap = ({ flightDistance }) => {
  const [trainRoutes, setTrainRoutes] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchTrainAlternatives = async () => {
      try {
        const response = await fetch(`http://127.0.0.1:8000/api/replaced_routes/${flightDistance}`);
        if (!response.ok) {
          console.error("API Error:", response.status, await response.text());
          return;
        }

        const data = await response.json();
        console.log("🚆 API Response:", JSON.stringify(data, null, 2)); // ✅ Log API response

        // ✅ Detect duplicate paths and log them
        const pathCounts = {};
        data.forEach((route) => {
          route.segments.forEach((segment) => {
            const key = JSON.stringify(segment.path);
            pathCounts[key] = (pathCounts[key] || 0) + 1;
          });
        });
        console.log("🖍️ Path Draw Counts:", pathCounts);

        // ✅ Ensure Berlin → Cologne is actually red
        data.forEach(route => {
          if (route.origin === "Berlin" && route.destination === "Cologne") {
            console.log("🚨 Berlin → Cologne: Color BEFORE setState:", route.segments.map(s => s.color));
          }
        });

        setTrainRoutes([]);
        setTrainRoutes(data);
        //setTimeout(() => setTrainRoutes(data), 10); // Force re-render
        setLoading(false);
      } catch (error) {
        console.error("❌ Error fetching train alternatives:", error);
        setLoading(false);
      }
    };

    fetchTrainAlternatives();
  }, [flightDistance]);

  // ✅ Sort routes so "red" is always drawn last
  const sortedTrainRoutes = [...trainRoutes].sort((a, b) => {
    const priority = { "red": 3, "orange": 2, "blue": 1 };
    return priority[a.segments[0]?.color] - priority[b.segments[0]?.color];
  });

  return (
    <div>
      {loading ? (
        <p>Loading train data...</p>
      ) : (
        <MapContainer center={[51.1657, 10.4515]} zoom={6} style={{ height: "800px", width: "100%" }}>
          <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" attribution="&copy; OpenStreetMap contributors" />
          {sortedTrainRoutes.map((route, index) => (
            route.segments.map((segment, segIndex) => {
              console.log(`🖌️ Rendering Segment: ${route.origin} → ${route.destination}, Color: ${segment.color}`);
              console.log("🔹 Path:", segment.path);

              return (
                <Polyline
                  key={`${index}-${segIndex}`}
                  positions={segment.path}
                  color={segment.color}
                  weight={getLineWeight(segment.color)}
                  opacity={1}
                />
              );
            })
          ))}
        </MapContainer>
      )}
    </div>
  );
};

export default ReplacedTrainMap;
