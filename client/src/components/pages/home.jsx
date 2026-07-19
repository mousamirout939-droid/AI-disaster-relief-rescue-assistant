import { useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import Hero from '../hero';
import AlertCard from '../alertcard';
import { fetchAlerts } from '../../store/slices/alertSlice';
import Loading from '../loading';

export default function Home() {
  const dispatch = useDispatch();
  const { items: alerts, status } = useSelector((s) => s.alerts);

  useEffect(() => {
    dispatch(fetchAlerts());
  }, [dispatch]);

  return (
    <div>
      <Hero />
      <section className="mx-auto max-w-5xl px-4 py-12">
        <h2 className="mb-4 text-xl font-bold">Active Alerts</h2>
        {status === 'loading' ? (
          <Loading />
        ) : alerts.length === 0 ? (
          <p className="text-sm text-gray-500 dark:text-gray-400">No active alerts right now. Stay safe!</p>
        ) : (
          <div className="grid gap-4 sm:grid-cols-2">
            {alerts.map((a) => <AlertCard key={a.id} alert={a} />)}
          </div>
        )}
      </section>
    </div>
  );
}
