import { useState } from 'react';
import toast from 'react-hot-toast';
import { Navigation, ShieldCheck } from 'lucide-react';
import { routeApi } from '../../api/endpoints';

export default function SafeRoute() {
  const [origin, setOrigin] = useState('');
  const [destination, setDestination] = useState('');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const { data } = await routeApi.safe(origin, destination);
      setResult(data.data);
    } catch (err) {
      toast.error(err.response?.data?.message || 'Could not compute route');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="mx-auto max-w-2xl px-4 py-10">
      <h1 className="text-2xl font-bold">Safe Route Planner</h1>
      <p className="mt-1 text-sm text-gray-500 dark:text-gray-400">
        Enter an origin and destination (address or "lat,lng") to get a route that avoids active hazard zones.
      </p>

      <form onSubmit={handleSubmit} className="card mt-6 space-y-4">
        <div>
          <label className="label">Origin</label>
          <input className="input" placeholder="e.g. 12.97,77.59 or an address" value={origin} onChange={(e) => setOrigin(e.target.value)} required />
        </div>
        <div>
          <label className="label">Destination</label>
          <input className="input" placeholder="e.g. 12.95,77.61 or an address" value={destination} onChange={(e) => setDestination(e.target.value)} required />
        </div>
        <button type="submit" className="btn-primary w-full" disabled={loading}>
          <Navigation size={16} /> {loading ? 'Calculating…' : 'Get Safe Route'}
        </button>
      </form>

      {result && (
        <div className="card mt-6">
          <p className="flex items-center gap-2 font-semibold">
            <ShieldCheck size={18} className="text-safe-600" /> Hazards considered: {result.active_hazards_considered}
          </p>
          <p className="mt-2 text-sm text-gray-500 dark:text-gray-400">{result.note}</p>
          {!result.directions?.available && (
            <p className="mt-3 rounded-lg bg-yellow-50 dark:bg-yellow-900/30 p-3 text-sm text-yellow-800 dark:text-yellow-300">
              Live turn-by-turn directions need a Google Maps API key configured on the server.
            </p>
          )}
        </div>
      )}
    </div>
  );
}
