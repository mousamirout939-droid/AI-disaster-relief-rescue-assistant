import { Link } from 'react-router-dom';
import './footer.css';

export default function Footer() {
  return (
    <footer className="footer">
      <div className="footer__inner">
        <div>
          <p className="footer__brand">🛟 AI Disaster Relief &amp; Rescue Assistant</p>
          <p className="footer__tagline">Faster help, smarter routes, safer communities.</p>
        </div>
        <div className="footer__links">
          <Link to="/shelters">Shelters</Link>
          <Link to="/hospitals">Hospitals</Link>
          <Link to="/volunteer">Volunteer</Link>
          <Link to="/emergency-guide">Emergency Guide</Link>
        </div>
      </div>
      <p className="footer__copyright">© {new Date().getFullYear()} Disaster Relief Assistant. Built for community safety.</p>
    </footer>
  );
}
