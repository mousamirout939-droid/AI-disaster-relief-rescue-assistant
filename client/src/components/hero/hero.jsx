import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import { ShieldAlert, MapPin, Siren } from 'lucide-react';
import './hero.css';

export default function Hero() {
  return (
    <section className="hero">
      <div className="hero__inner">
        <motion.div initial={{ opacity: 0, y: 16 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.5 }}>
          <span className="hero__badge">
            <Siren size={14} /> Real-time disaster response
          </span>
          <h1 className="hero__title">
            AI-powered help when <span className="text-primary-600 dark:text-primary-400">every second counts</span>
          </h1>
          <p className="hero__subtitle">
            Report disasters with photo detection, find the nearest shelter or hospital,
            get a hazard-aware safe route, and reach rescue teams — all in one place.
          </p>
          <div className="hero__actions">
            <Link to="/report-disaster" className="btn-primary">
              <ShieldAlert size={18} /> Report a Disaster
            </Link>
            <Link to="/shelters" className="btn-secondary">
              <MapPin size={18} /> Find Nearby Shelter
            </Link>
          </div>
        </motion.div>
      </div>
    </section>
  );
}
