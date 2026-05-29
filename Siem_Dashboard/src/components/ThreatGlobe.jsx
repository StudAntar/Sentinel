import { useEffect, useState } from "react";
import Globe from "react-globe.gl";

function ThreatGlobe() {
  const [locations, setLocations] = useState([]);

  useEffect(() => {
    fetch("http://127.0.0.1:5000/api/login-locations")
      .then((response) => response.json())
      .then((data) => setLocations(data))
      .catch((error) => console.error("Error fetching login locations:", error));
  }, []);

  const dxcBase = {
    lat: 55.6761,
    lng: 12.5683,
    city: "Copenhagen",
  };

  const arcs = locations.map((location) => ({
    startLat: dxcBase.lat,
    startLng: dxcBase.lng,
    endLat: location.lat,
    endLng: location.lng,
    city: location.city,
    country: location.country,
    count: location.count,
  }));

  return (
    <div
      style={{
        height: "420px",
        width: "100%",
        overflow: "hidden",
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
      }}
    >
      <Globe
        globeImageUrl="//unpkg.com/three-globe/example/img/earth-night.jpg"
        backgroundColor="rgba(0,0,0,0)"
        pointsData={locations}
        pointLat={(d) => d.lat}
        pointLng={(d) => d.lng}
        pointAltitude={0.04}
        pointRadius={(d) => Math.min(0.12, 0.025 + d.count * 0.003)}
        pointColor={() => "#ffffff"}
        pointLabel={(d) =>
          `${d.city}, ${d.country}<br/>Logins: ${d.count}`
        }
        arcsData={arcs}
        arcStartLat={(d) => d.startLat}
        arcStartLng={(d) => d.startLng}
        arcEndLat={(d) => d.endLat}
        arcEndLng={(d) => d.endLng}
        arcColor={() => "#ffffff"}
        arcAltitude={0.25}
        arcStroke={0.25}
        arcDashLength={0.4}
        arcDashGap={0.2}
        arcDashAnimateTime={1800}
        width={420}
        height={350}
      />
    </div>
  );
}

export default ThreatGlobe;