import { useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { Link } from 'react-router-dom';
import { ShieldAlert, MapPin, Clock } from 'lucide-react';
import useAuth from '../../hooks/useAuth';
import { fetchMyReports } from '../../store/slices/reportSlice';
import { SEVERITY_COLORS } from '../../utils/constants';
import { formatDate, titleCase } from '../../utils/formatters';
import Loading from '../loading';

export default function Dashboard() {
  const dispatch = useDispatch();
  const { user } = useAuth();
  const { myReports, status } = useSelector((s) => s.reports);

  useEffect(() => {
    dispatch(fetchMyReports());
  }, [dispatch]);

  return (
    <div className="mx-auto max-w-5xl px-4 py-10">
      <h1 className="text-2xl font-bold">Welcome back{user?.name ? `, ${user.name}` : ''} 👋</h1>
      <p className="mt-1 text-gray-500 dark:text-gray-400">Here's what's happening with your reports.</p>

      <div className="mt-6 flex flex-wrap gap-3">
        <Link to="/report-disaster" className="btn-primary"><ShieldAlert size={16} /> Report a Disaster</Link>
        <Link to="/safe-route" className="btn-secondary"><MapPin size={16} /> Plan a Safe Route</Link>
      </div>

      <h2 className="mb-3 mt-8 text-lg font-semibold">Your Reports</h2>
      {status === 'loading' ? (
        <Loading />
      ) : myReports.length === 0 ? (
        <p className="text-sm text-gray-500 dark:text-gray-400">You haven't submitted any reports yet.</p>
      ) : (
        <div className="space-y-3">
          {myReports.map((r) => (
            <div key={r.id} className="card flex items-start justify-between gap-3">
              <div>
                <p className="font-medium">{titleCase(r.disaster_type)}</p>
                <p className="mt-0.5 text-sm text-gray-500 dark:text-gray-400 line-clamp-2">{r.description}</p>
                <p className="mt-1 flex items-center gap-1 text-xs text-gray-400">
                  <Clock size={12} /> {formatDate(r.created_at)}
                </p>
              </div>
              <div className="flex flex-col items-end gap-2">
                {r.ai_severity && (
                  <span className={`rounded-full px-2.5 py-0.5 text-xs font-semibold ${SEVERITY_COLORS[r.ai_severity]}`}>
                    {titleCase(r.ai_severity)}
                  </span>
                )}
                <span className="text-xs font-medium capitalize text-gray-500">{r.status}</span>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
