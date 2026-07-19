import { useEffect, useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import toast from 'react-hot-toast';
import { Plus } from 'lucide-react';
import { fetchAlerts, createAlert } from '../../store/slices/alertSlice';
import useAuth from '../../hooks/useAuth';
import AlertCard from '../alertcard';
import Loading from '../loading';

export default function Alerts() {
  const dispatch = useDispatch();
  const { items: alerts, status } = useSelector((s) => s.alerts);
  const { role } = useAuth();
  const [form, setForm] = useState({ title: '', message: '', severity: 'moderate', region: '' });
  const [showForm, setShowForm] = useState(false);

  useEffect(() => {
    dispatch(fetchAlerts());
  }, [dispatch]);

  const handleCreate = async (e) => {
    e.preventDefault();
    const result = await dispatch(createAlert(form));
    if (createAlert.fulfilled.match(result)) {
      toast.success('Alert published');
      setForm({ title: '', message: '', severity: 'moderate', region: '' });
      setShowForm(false);
    } else {
      toast.error(result.payload || 'Could not create alert');
    }
  };

  return (
    <div className="mx-auto max-w-4xl px-4 py-10">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold">Alerts</h1>
        {role === 'admin' && (
          <button className="btn-primary text-sm" onClick={() => setShowForm((v) => !v)}>
            <Plus size={16} /> New Alert
          </button>
        )}
      </div>

      {showForm && (
        <form onSubmit={handleCreate} className="card mt-4 space-y-3">
          <input className="input" placeholder="Title" value={form.title} onChange={(e) => setForm({ ...form, title: e.target.value })} required />
          <textarea className="input" placeholder="Message" value={form.message} onChange={(e) => setForm({ ...form, message: e.target.value })} required />
          <div className="grid grid-cols-2 gap-3">
            <select className="input" value={form.severity} onChange={(e) => setForm({ ...form, severity: e.target.value })}>
              {['low', 'moderate', 'high', 'critical'].map((s) => <option key={s} value={s}>{s}</option>)}
            </select>
            <input className="input" placeholder="Region (optional)" value={form.region} onChange={(e) => setForm({ ...form, region: e.target.value })} />
          </div>
          <button type="submit" className="btn-primary">Publish Alert</button>
        </form>
      )}

      <div className="mt-6 space-y-4">
        {status === 'loading' ? (
          <Loading />
        ) : alerts.length === 0 ? (
          <p className="text-sm text-gray-500 dark:text-gray-400">No active alerts.</p>
        ) : (
          alerts.map((a) => <AlertCard key={a.id} alert={a} />)
        )}
      </div>
    </div>
  );
}
