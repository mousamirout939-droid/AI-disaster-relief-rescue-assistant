import { Users, Phone, Radio } from 'lucide-react';
import { formatDistance } from '../../utils/formatters';
import './rescueteamcard.css';

const STATUS_STYLES = {
  available: 'rescueteamcard__status--available',
  dispatched: 'rescueteamcard__status--dispatched',
  off_duty: 'rescueteamcard__status--offduty',
};

export default function RescueTeamCard({ team, onDispatch }) {
  return (
    <div className="rescueteamcard">
      <div className="rescueteamcard__icon">
        <Radio size={20} />
      </div>
      <div className="flex-1">
        <div className="flex items-center justify-between gap-2">
          <h3 className="rescueteamcard__title">{team.name}</h3>
          <span className={`rescueteamcard__status ${STATUS_STYLES[team.status] || ''}`}>{team.status}</span>
        </div>
        <p className="rescueteamcard__spec">{team.specialization}</p>

        <div className="rescueteamcard__meta">
          <span className="flex items-center gap-1">
            <Users size={14} /> {team.members_count} members
          </span>
          {team.contact_number && (
            <span className="flex items-center gap-1">
              <Phone size={14} /> {team.contact_number}
            </span>
          )}
          {typeof team.distance_km === 'number' && <span>{formatDistance(team.distance_km)} away</span>}
        </div>

        {onDispatch && team.status === 'available' && (
          <button className="btn-primary !py-1.5 !px-3 mt-3 text-xs" onClick={() => onDispatch(team.id)}>
            Dispatch Team
          </button>
        )}
      </div>
    </div>
  );
}
