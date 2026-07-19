import { useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import toast from 'react-hot-toast';
import { LocateFixed } from 'lucide-react';
import { fetchRescueTeams, fetchNearbyRescueTeams, dispatchRescueTeam } from '../../store/slices/rescueSlice';
import useGeolocation from '../../hooks/useGeolocation';
import useAuth from '../../hooks/useAuth';
import RescueTeamCard from '../rescueteamcard';
import Loading from '../loading';

export default function RescueTeams() {
  const dispatch = useDispatch();
  const { items: teams, status } = useSelector((s) => s.rescue);
  const { position, requestLocation, loading: locating } = useGeolocation();
  const { role } = useAuth();

  useEffect(() => {
    dispatch(fetchRescueTeams());
  }, [dispatch]);

  useEffect(() => {
    if (position) dispatch(fetchNearbyRescueTeams({ lat: position.lat, lng: position.lng, radius_km: 25 }));
  }, [position, dispatch]);

  const handleDispatch = async (teamId) => {
    const reportId = window.prompt('Enter the disaster report ID to dispatch this team to:');
    if (!reportId) return;
    const result = await dispatch(dispatchRescueTeam({ teamId, reportId }));
    if (dispatchRescueTeam.fulfilled.match(result)) toast.success('Team dispatched');
    else toast.error(result.payload || 'Could not dispatch team');
  };

  return (
    <div className="mx-auto max-w-6xl px-4 py-10">
      <div className="flex flex-wrap items-center justify-between gap-3">
        <h1 className="text-2xl font-bold">Rescue Teams</h1>
        <button className="btn-secondary text-sm" onClick={requestLocation} disabled={locating}>
          <LocateFixed size={16} /> {locating ? 'Locating…' : 'Use my location'}
        </button>
      </div>

      {status === 'loading' ? (
        <Loading />
      ) : teams.length === 0 ? (
        <p className="mt-6 text-sm text-gray-500 dark:text-gray-400">No rescue teams found.</p>
      ) : (
        <div className="mt-6 grid gap-4 sm:grid-cols-2">
          {teams.map((t) => (
            <RescueTeamCard key={t.id} team={t} onDispatch={role === 'admin' ? handleDispatch : undefined} />
          ))}
        </div>
      )}
    </div>
  );
}
