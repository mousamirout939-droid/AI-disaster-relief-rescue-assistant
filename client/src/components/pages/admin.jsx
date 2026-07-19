import { useEffect, useState } from 'react';
import toast from 'react-hot-toast';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid } from 'recharts';
import { Users, FileWarning, Home, ShieldCheck } from 'lucide-react';
import { adminApi, reportApi, volunteerApi } from '../../api/endpoints';
import Loading from '../loading';

export default function Admin() {
  const [stats, setStats] = useState(null);
  const [users, setUsers] = useState([]);
  const [pendingReports, setPendingReports] = useState([]);
  const [volunteers, setVolunteers] = useState([]);
  const [loading, setLoading] = useState(true);

  const loadAll = async () => {
    setLoading(true);
    try {
      const [statsRes, usersRes, reportsRes, volunteersRes] = await Promise.all([
        adminApi.dashboardStats(),
        adminApi.listUsers(),
        reportApi.list({ status: 'pending' }),
        volunteerApi.list(),
      ]);
      setStats(statsRes.data.data);
      setUsers(usersRes.data.data);
      setPendingReports(reportsRes.data.data);
      setVolunteers(volunteersRes.data.data);
    } catch (err) {
      toast.error(err.response?.data?.message || 'Could not load admin dashboard');
    } finally {
      setLoading(false);
    }
  };

  // eslint-disable-next-line react-hooks/set-state-in-effect -- standard fetch-on-mount pattern
  useEffect(() => { loadAll(); }, []);

  const approveVolunteer = async (id) => {
    await volunteerApi.approve(id);
    toast.success('Volunteer approved');
    loadAll();
  };

  const verifyReport = async (id) => {
    await reportApi.updateStatus(id, 'verified');
    toast.success('Report verified');
    loadAll();
  };

  if (loading || !stats) return <Loading fullScreen label="Loading admin dashboard…" />;

  const chartData = [
    { name: 'Reports', value: stats.total_reports },
    { name: 'Pending', value: stats.pending_reports },
    { name: 'Shelters', value: stats.total_shelters },
    { name: 'Hospitals', value: stats.total_hospitals },
    { name: 'Teams Avail.', value: stats.rescue_teams_available },
  ];

  return (
    <div className="mx-auto max-w-6xl px-4 py-10">
      <h1 className="text-2xl font-bold">Admin Dashboard</h1>

      <div className="mt-6 grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        <StatCard icon={Users} label="Total Users" value={stats.total_users} />
        <StatCard icon={FileWarning} label="Pending Reports" value={stats.pending_reports} />
        <StatCard icon={Home} label="Shelters" value={stats.total_shelters} />
        <StatCard icon={ShieldCheck} label="Teams Available" value={stats.rescue_teams_available} />
      </div>

      <div className="card mt-8 h-72">
        <h2 className="mb-2 font-semibold">Activity Overview</h2>
        <ResponsiveContainer width="100%" height="90%">
          <BarChart data={chartData}>
            <CartesianGrid strokeDasharray="3 3" opacity={0.2} />
            <XAxis dataKey="name" fontSize={12} />
            <YAxis fontSize={12} />
            <Tooltip />
            <Bar dataKey="value" fill="#e51f1f" radius={[4, 4, 0, 0]} />
          </BarChart>
        </ResponsiveContainer>
      </div>

      <h2 className="mb-3 mt-8 text-lg font-semibold">Pending Reports ({pendingReports.length})</h2>
      <div className="space-y-3">
        {pendingReports.map((r) => (
          <div key={r.id} className="card flex items-center justify-between">
            <div>
              <p className="font-medium capitalize">{r.disaster_type}</p>
              <p className="text-sm text-gray-500 dark:text-gray-400 line-clamp-1">{r.description}</p>
            </div>
            <button className="btn-primary !py-1.5 !px-3 text-xs" onClick={() => verifyReport(r.id)}>Verify</button>
          </div>
        ))}
        {pendingReports.length === 0 && <p className="text-sm text-gray-500 dark:text-gray-400">No pending reports.</p>}
      </div>

      <h2 className="mb-3 mt-8 text-lg font-semibold">Pending Volunteers</h2>
      <div className="space-y-3">
        {volunteers.filter((v) => !v.is_approved).map((v) => (
          <div key={v.id} className="card flex items-center justify-between">
            <div>
              <p className="font-medium">{v.name}</p>
              <p className="text-sm text-gray-500 dark:text-gray-400">{v.email} · {v.skills?.join(', ')}</p>
            </div>
            <button className="btn-primary !py-1.5 !px-3 text-xs" onClick={() => approveVolunteer(v.id)}>Approve</button>
          </div>
        ))}
        {volunteers.filter((v) => !v.is_approved).length === 0 && (
          <p className="text-sm text-gray-500 dark:text-gray-400">No pending volunteer applications.</p>
        )}
      </div>

      <h2 className="mb-3 mt-8 text-lg font-semibold">Users ({users.length})</h2>
      <div className="overflow-x-auto rounded-xl border border-gray-200 dark:border-gray-800">
        <table className="w-full text-sm">
          <thead className="bg-gray-50 dark:bg-gray-900 text-left">
            <tr><th className="p-3">Name</th><th className="p-3">Email</th><th className="p-3">Role</th><th className="p-3">Active</th></tr>
          </thead>
          <tbody>
            {users.map((u) => (
              <tr key={u.id} className="border-t border-gray-100 dark:border-gray-800">
                <td className="p-3">{u.name}</td>
                <td className="p-3">{u.email}</td>
                <td className="p-3 capitalize">{u.role}</td>
                <td className="p-3">{u.is_active ? 'Yes' : 'No'}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

function StatCard({ icon: Icon, label, value }) {
  return (
    <div className="card flex items-center gap-3">
      <div className="flex h-10 w-10 items-center justify-center rounded-full bg-primary-100 text-primary-600 dark:bg-primary-900/40 dark:text-primary-300">
        <Icon size={18} />
      </div>
      <div>
        <p className="text-xl font-bold">{value}</p>
        <p className="text-xs text-gray-500 dark:text-gray-400">{label}</p>
      </div>
    </div>
  );
}
