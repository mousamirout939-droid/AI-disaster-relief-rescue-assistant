import { useEffect, useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { LocateFixed } from 'lucide-react';
import { fetchHospitals, fetchNearbyHospitals } from '../../store/slices/hospitalSlice';
import useGeolocation from '../../hooks/useGeolocation';
import HospitalCard from '../hospitalcard';
import DisasterMap from '../disastermap';
import Loading from '../loading';

export default function HospitalLocator() {
  const dispatch = useDispatch();
  const { items: hospitals, status } = useSelector((s) => s.hospitals);
  const { position, requestLocation, loading: locating } = useGeolocation();
  const [selectedId, setSelectedId] = useState(null);

  useEffect(() => {
    dispatch(fetchHospitals());
  }, [dispatch]);

  useEffect(() => {
    if (position) dispatch(fetchNearbyHospitals({ lat: position.lat, lng: position.lng, radius_km: 15 }));
  }, [position, dispatch]);

  const handleSelect = (hospital) => {
    setSelectedId(hospital.id);
    document.getElementById('hospital-map')?.scrollIntoView({ behavior: 'smooth', block: 'start' });
  };

  return (
    <div className="mx-auto max-w-6xl px-4 py-10">
      <div className="flex flex-wrap items-center justify-between gap-3">
        <h1 className="text-2xl font-bold">Nearby Hospitals</h1>
        <button className="btn-secondary text-sm" onClick={requestLocation} disabled={locating}>
          <LocateFixed size={16} /> {locating ? 'Locating…' : 'Use my location'}
        </button>
      </div>

      <div id="hospital-map" className="mt-6 scroll-mt-20">
        <DisasterMap
          markers={hospitals}
          center={position ? { lat: position.lat, lng: position.lng } : undefined}
          selectedId={selectedId}
        />
      </div>

      <h2 className="mb-3 mt-8 text-lg font-semibold">Hospitals</h2>
      <p className="mb-3 -mt-2 text-xs text-gray-400">Click a hospital to see it on the map above.</p>
      {status === 'loading' ? (
        <Loading />
      ) : hospitals.length === 0 ? (
        <p className="text-sm text-gray-500 dark:text-gray-400">No hospitals found.</p>
      ) : (
        <div className="grid gap-4 sm:grid-cols-2">
          {hospitals.map((h) => (
            <HospitalCard key={h.id} hospital={h} onClick={() => handleSelect(h)} isSelected={h.id === selectedId} />
          ))}
        </div>
      )}
    </div>
  );
}