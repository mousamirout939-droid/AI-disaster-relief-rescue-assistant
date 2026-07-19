import { AlertTriangle } from 'lucide-react';
import { SEVERITY_COLORS } from '../../utils/constants';
import { formatDate, titleCase } from '../../utils/formatters';
import './alertcard.css';

export default function AlertCard({ alert }) {
  return (
    <div className="alertcard">
      <div className="alertcard__icon">
        <AlertTriangle size={20} />
      </div>
      <div className="flex-1">
        <div className="flex items-center justify-between gap-2">
          <h3 className="alertcard__title">{alert.title}</h3>
          <span className={`alertcard__badge ${SEVERITY_COLORS[alert.severity] || ''}`}>
            {titleCase(alert.severity)}
          </span>
        </div>
        <p className="alertcard__message">{alert.message}</p>
        <div className="alertcard__meta">
          {alert.region && <span>{alert.region}</span>}
          <span>{formatDate(alert.created_at)}</span>
        </div>
      </div>
    </div>
  );
}
