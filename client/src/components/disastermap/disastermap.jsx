import { useEffect, useRef, useState } from 'react';
import './disastermap.css';

const GOOGLE_MAPS_KEY = import.meta.env.VITE_GOOGLE_MAPS_API_KEY;

function loadGoogleMapsScript(apiKey) {
  return new Promise((resolve, reject) => {
    if (window.google?.maps) return resolve(window.google);
    const existing = document.getElementById('google-maps-script');
    if (existing) {
      existing.addEventListener('load', () => resolve(window.google));
      return;
    }
    const script = document.createElement('script');
    script.id = 'google-maps-script';
    script.src = `https://maps.googleapis.com/maps/api/js?key=${apiKey}`;
    script.async = true;
    script.onload = () => resolve(window.google);
    script.onerror = reject;
    document.head.appendChild(script);
  });
}

/**
 * Renders markers for a list of {name, location:{coordinates:[lng,lat]}} items on Google Maps.
 * Falls back to a plain coordinate list if no VITE_GOOGLE_MAPS_API_KEY is configured.
 *
 * Pass `selectedId` to auto-center/zoom on one marker and pop open its info window
 * (used by the hospital/shelter locator pages when a card is clicked).
 */
export default function DisasterMap({ markers = [], center, zoom = 12, height = 400, selectedId }) {
  const mapRef = useRef(null);
  const [mapReady, setMapReady] = useState(false);
  const [loadFailed, setLoadFailed] = useState(!GOOGLE_MAPS_KEY);
  const mapInstanceRef = useRef(null);
  const markerRefsRef = useRef({});
  const infoWindowRef = useRef(null);

  useEffect(() => {
    if (!GOOGLE_MAPS_KEY) {
      return;
    }
    loadGoogleMapsScript(GOOGLE_MAPS_KEY)
      .then((google) => {
        const defaultCenter = center || { lat: 12.9716, lng: 77.5946 };
        const mapInstance = new google.maps.Map(mapRef.current, {
          center: defaultCenter,
          zoom,
          disableDefaultUI: false,
        });
        mapInstanceRef.current = mapInstance;
        infoWindowRef.current = new google.maps.InfoWindow();

        markers.forEach((m) => {
          const [lng, lat] = m.location?.coordinates || [m.lng, m.lat];
          if (lat === undefined || lng === undefined) return;
          const marker = new google.maps.Marker({ position: { lat, lng }, map: mapInstance, title: m.name });
          marker.addListener('click', () => {
            infoWindowRef.current.setContent(
              `<strong>${m.name}</strong>${m.address ? `<br/>${m.address}` : ''}`
            );
            infoWindowRef.current.open({ map: mapInstance, anchor: marker });
          });
          if (m.id) markerRefsRef.current[m.id] = { marker, lat, lng, data: m };
        });
        setMapReady(true);
      })
      .catch(() => setLoadFailed(true));
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [markers]);

  useEffect(() => {
    if (!selectedId || !mapReady) return;
    const entry = markerRefsRef.current[selectedId];
    const map = mapInstanceRef.current;
    if (!entry || !map) return;

    map.panTo({ lat: entry.lat, lng: entry.lng });
    map.setZoom(15);
    infoWindowRef.current.setContent(
      `<strong>${entry.data.name}</strong>${entry.data.address ? `<br/>${entry.data.address}` : ''}`
    );
    infoWindowRef.current.open({ map, anchor: entry.marker });
  }, [selectedId, mapReady]);

  if (loadFailed) {
    return (
      <div className="disastermap__fallback" style={{ height }}>
        <p className="mb-2 font-medium">Map preview unavailable (no Google Maps API key configured).</p>
        <ul className="disastermap__list">
          {markers.slice(0, 8).map((m, i) => (
            <li key={m.id || i}>📍 {m.name}</li>
          ))}
        </ul>
      </div>
    );
  }

  return <div ref={mapRef} className="disastermap" style={{ height }} aria-busy={!mapReady} />;
}