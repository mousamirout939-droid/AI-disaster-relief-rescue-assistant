import { useState } from 'react';
import { Languages } from 'lucide-react';
import { LANGUAGES } from '../../utils/constants';
import './languageselector.css';

/** Sets the app's preferred instruction language (stored locally; used by the Emergency Guide page). */
export default function LanguageSelector() {
  const [lang, setLang] = useState(localStorage.getItem('preferred_language') || 'en');

  const handleChange = (e) => {
    const value = e.target.value;
    setLang(value);
    localStorage.setItem('preferred_language', value);
  };

  return (
    <label className="languageselector">
      <Languages size={16} className="text-gray-500 dark:text-gray-400" />
      <select value={lang} onChange={handleChange} aria-label="Select language">
        {LANGUAGES.map((l) => (
          <option key={l.code} value={l.code}>{l.label}</option>
        ))}
      </select>
    </label>
  );
}
