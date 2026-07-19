import { useEffect, useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { LocateFixed } from 'lucide-react';
import { fetchShelters, fetchNearbyShelters } from '../../store/slices/shelterSlice';
import useGeolocation from '../../hooks/useGeolocation';
import ShelterCard from '../sheltercard';
import DisasterMap from '../disastermap';
import Loading from '../loading';
import { openInGoogleMaps, extractLatLng } from '../../utils/maps';

const HAS_MAPS_KEY = Boolean(import.meta.env.VITE_GOOGLE_MAPS_API_KEY);

export default function ShelterLocator() {
  const dispatch = useDispatch();
  const { items: shelters, status } = useSelector((s) => s.shelters);
  const { position, requestLocation, loading: locating } = useGeolocation();
  const radius = 15;
  const [selectedId, setSelectedId] = useState(null);

  useEffect(() => {
    dispatch(fetchShelters());
  }, [dispatch]);

  useEffect(() => {
    if (position) dispatch(fetchNearbyShelters({ lat: position.lat, lng: position.lng, radius_km: radius }));
  }, [position, radius, dispatch]);

  const handleSelect = (shelter) => {
    if (HAS_MAPS_KEY) {
      setSelectedId(shelter.id);
      document.getElementById('shelter-map')?.scrollIntoView({ behavior: 'smooth', block: 'start' });
      return;
    }
    const coords = extractLatLng(shelter);
    if (coords) openInGoogleMaps(coords.lat, coords.lng, shelter.name);
  };

  return (
    <div className="mx-auto max-w-6xl px-4 py-10">
      <div className="flex flex-wrap items-center justify-between gap-3">
        <h1 className="text-2xl font-bold">Nearby Shelters</h1>
        <button className="btn-secondary text-sm" onClick={requestLocation} disabled={locating}>
          <LocateFixed size={16} /> {locating ? 'Locating…' : 'Use my location'}
        </button>
      </div>

      <div id="shelter-map" className="mt-6 scroll-mt-20">
        <DisasterMap
          markers={shelters}
          center={position ? { lat: position.lat, lng: position.lng } : undefined}
          selectedId={selectedId}
        />
      </div>

      <h2 className="mb-3 mt-8 text-lg font-semibold">{position ? `Within ${radius} km` : 'All Shelters'}</h2>
      <p className="mb-3 -mt-2 text-xs text-gray-400">
        {HAS_MAPS_KEY ? 'Click a shelter to see it on the map above.' : 'Click a shelter to open it in Google Maps.'}
      </p>
      {status === 'loading' ? (
        <Loading />
      ) : shelters.length === 0 ? (
        <p className="text-sm text-gray-500 dark:text-gray-400">No shelters found.</p>
      ) : (
        <div className="grid gap-4 sm:grid-cols-2">
          {shelters.map((s) => (
            <ShelterCard key={s.id} shelter={s} onClick={() => handleSelect(s)} isSelected={s.id === selectedId} />
          ))}
        </div>
      )}
    </div>
  );
}