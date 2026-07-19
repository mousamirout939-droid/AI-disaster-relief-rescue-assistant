/** Small display-formatting helpers used across pages/components. */
export function formatDate(timestamp) {
  if (!timestamp) return '—';
  const date = new Date(timestamp * 1000);
  return date.toLocaleString(undefined, {
    year: 'numeric', month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit',
  });
}

export function formatDistance(km) {
  if (km === null || km === undefined) return '';
  return km < 1 ? `${Math.round(km * 1000)} m` : `${km.toFixed(1)} km`;
}

export function titleCase(str = '') {
  return str.replace(/_/g, ' ').replace(/\b\w/g, (c) => c.toUpperCase());
}
