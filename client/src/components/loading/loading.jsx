import './loading.css';

/** Full-screen or inline loading spinner. Pass `fullScreen` for a page-level overlay. */
export default function Loading({ fullScreen = false, label = 'Loading…' }) {
  if (fullScreen) {
    return (
      <div className="fixed inset-0 z-50 flex flex-col items-center justify-center gap-3 bg-white/80 dark:bg-gray-950/80 backdrop-blur-sm">
        <span className="loading-spinner" />
        <p className="text-sm text-gray-600 dark:text-gray-400">{label}</p>
      </div>
    );
  }
  return (
    <div className="flex items-center justify-center gap-2 py-8">
      <span className="loading-spinner loading-spinner--sm" />
      <span className="text-sm text-gray-500 dark:text-gray-400">{label}</span>
    </div>
  );
}
