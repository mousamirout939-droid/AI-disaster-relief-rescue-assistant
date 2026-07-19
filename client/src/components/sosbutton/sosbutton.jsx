import { useState } from 'react';
import toast from 'react-hot-toast';
import { Siren } from 'lucide-react';
import { emergencyApi } from '../../api/endpoints';
import useAuth from '../../hooks/useAuth';
import useGeolocation from '../../hooks/useGeolocation';

/** Fixed emergency SOS button — only rendered for authenticated users. */
export default function SOSButton() {
  const { isAuthenticated } = useAuth();
  const { position, requestLocation } = useGeolocation();
  const [sending, setSending] = useState(false);

  if (!isAuthenticated) return null;

  const handleSOS = async () => {
    if (!window.confirm('This will alert nearby rescue teams and hospitals to your location. Continue?')) return;
    setSending(true);
    try {
      let coords = position;
      if (!coords) {
        requestLocation();
        await new Promise((r) => setTimeout(r, 1200));
      }
      const { lat, lng } = coords || { lat: 0, lng: 0 };
      const { data } = await emergencyApi.sos(lat, lng);
      const team = data.data.nearest_rescue_team;
      toast.success(team ? `SOS sent! Nearest team: ${team.name} (${team.distance_km} km away)` : 'SOS sent! Help is on the way.');
    } catch (err) {
      toast.error(err.response?.data?.message || 'Could not send SOS');
    } finally {
      setSending(false);
    }
  };

  return (
    <button onClick={handleSOS} disabled={sending} className="sosbutton" aria-label="Send SOS">
      <Siren size={22} />
      <span className="sosbutton__label">SOS</span>
    </button>
  );
}
