import { Home, Phone, Users } from 'lucide-react';
import { formatDistance } from '../../utils/formatters';
import './sheltercard.css';

export default function ShelterCard({ shelter, onClick, isSelected }) {
  const full = shelter.capacity > 0 && shelter.occupancy >= shelter.capacity;

  return (
    <div
      className={`sheltercard ${onClick ? 'sheltercard--clickable' : ''} ${isSelected ? 'sheltercard--selected' : ''}`}
      onClick={onClick}
      role={onClick ? 'button' : undefined}
      tabIndex={onClick ? 0 : undefined}
      onKeyDown={onClick ? (e) => (e.key === 'Enter' || e.key === ' ') && onClick() : undefined}
    >
      <div className="sheltercard__icon">
        <Home size={20} />
      </div>
      <div className="flex-1">
        <div className="flex items-center justify-between gap-2">
          <h3 className="sheltercard__title">{shelter.name}</h3>
          <span className={`sheltercard__status ${full ? 'sheltercard__status--full' : ''}`}>
            {full ? 'Full' : shelter.status || 'Open'}
          </span>
        </div>
        {shelter.address && <p className="sheltercard__address">{shelter.address}</p>}

        <div className="sheltercard__meta">
          <span className="flex items-center gap-1">
            <Users size={14} /> {shelter.occupancy || 0}/{shelter.capacity || '—'}
          </span>
          {shelter.contact_number && (
            <span className="flex items-center gap-1">
              <Phone size={14} /> {shelter.contact_number}
            </span>
          )}
          {typeof shelter.distance_km === 'number' && <span>{formatDistance(shelter.distance_km)} away</span>}
        </div>

        {shelter.resources?.length > 0 && (
          <div className="sheltercard__tags">
            {shelter.resources.map((r) => (
              <span key={r} className="sheltercard__tag">{r}</span>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}