import { Hospital, Phone, BedDouble, MapPin } from 'lucide-react';
import { formatDistance } from '../../utils/formatters';
import './hospitalcard.css';

export default function HospitalCard({ hospital, onClick, isSelected }) {
  return (
    <div
      className={`hospitalcard ${onClick ? 'hospitalcard--clickable' : ''} ${isSelected ? 'hospitalcard--selected' : ''}`}
      onClick={onClick}
      role={onClick ? 'button' : undefined}
      tabIndex={onClick ? 0 : undefined}
      onKeyDown={onClick ? (e) => (e.key === 'Enter' || e.key === ' ') && onClick() : undefined}
    >
      <div className="hospitalcard__icon">
        <Hospital size={20} />
      </div>
      <div className="flex-1">
        <div className="flex items-center justify-between gap-2">
          <h3 className="hospitalcard__title">{hospital.name}</h3>
          {onClick && <MapPin size={16} className="shrink-0 text-gray-400" />}
        </div>
        {hospital.address && <p className="hospitalcard__address">{hospital.address}</p>}

        <div className="hospitalcard__meta">
          <span className="flex items-center gap-1">
            <BedDouble size={14} /> {hospital.beds_available ?? 0} beds available
          </span>
          {hospital.contact_number && (
            <span className="flex items-center gap-1">
              <Phone size={14} /> {hospital.contact_number}
            </span>
          )}
          {typeof hospital.distance_km === 'number' && <span>{formatDistance(hospital.distance_km)} away</span>}
        </div>

        {hospital.specialities?.length > 0 && (
          <div className="hospitalcard__tags">
            {hospital.specialities.map((s) => (
              <span key={s} className="hospitalcard__tag">{s}</span>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}