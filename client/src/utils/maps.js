/** Opens a location directly in Google Maps in a new tab — no API key required. */
export function openInGoogleMaps(lat, lng, label) {
  const query = label ? `${lat},${lng} (${label})` : `${lat},${lng}`;
  const url = `https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(query)}`;
  window.open(url, '_blank', 'noopener,noreferrer');
}

/** Extracts {lat, lng} from a Mongo-style GeoJSON location field: {coordinates: [lng, lat]}. */
export function extractLatLng(item) {
  const coords = item?.location?.coordinates;
  if (!coords) return null;
  return { lat: coords[1], lng: coords[0] };
}