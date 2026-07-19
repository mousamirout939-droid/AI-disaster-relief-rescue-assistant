import { useEffect, useState } from 'react';
import { BookOpen } from 'lucide-react';
import { translationApi } from '../../api/endpoints';
import { LANGUAGES } from '../../utils/constants';

const GUIDE_KEYS = ['stay_calm_move_to_safety', 'call_emergency_services'];

const GENERAL_TIPS = [
  { title: 'Before a disaster', points: ['Prepare an emergency kit (water, food, torch, first aid).', 'Know your nearest shelter and evacuation route.', 'Save local emergency numbers in your phone.'] },
  { title: 'During a disaster', points: ['Stay calm and follow official instructions.', 'Move away from the hazard to higher/open ground.', 'Avoid downed power lines and floodwater.'] },
  { title: 'After a disaster', points: ['Check yourself and others for injuries.', 'Avoid damaged buildings and structures.', 'Use the in-app SOS button if you need urgent help.'] },
];

export default function EmergencyGuide() {
  const [lang, setLang] = useState(localStorage.getItem('preferred_language') || 'en');
  const [phrases, setPhrases] = useState({});

  useEffect(() => {
    Promise.all(GUIDE_KEYS.map((key) => translationApi.corePhrase(key, lang)))
      .then((responses) => {
        const map = {};
        responses.forEach((r, i) => { map[GUIDE_KEYS[i]] = r.data.data.text; });
        setPhrases(map);
      })
      .catch(() => {});
  }, [lang]);

  return (
    <div className="mx-auto max-w-3xl px-4 py-10">
      <div className="flex items-center justify-between">
        <h1 className="flex items-center gap-2 text-2xl font-bold"><BookOpen size={24} /> Emergency Guide</h1>
        <select className="input !w-auto" value={lang} onChange={(e) => setLang(e.target.value)}>
          {LANGUAGES.map((l) => <option key={l.code} value={l.code}>{l.label}</option>)}
        </select>
      </div>

      <div className="card mt-6 space-y-2">
        {GUIDE_KEYS.map((key) => (
          <p key={key} className="text-gray-800 dark:text-gray-100">🔹 {phrases[key] || '…'}</p>
        ))}
      </div>

      <div className="mt-8 space-y-6">
        {GENERAL_TIPS.map((section) => (
          <div key={section.title} className="card">
            <h2 className="mb-2 font-semibold">{section.title}</h2>
            <ul className="list-disc space-y-1 pl-5 text-sm text-gray-600 dark:text-gray-300">
              {section.points.map((p) => <li key={p}>{p}</li>)}
            </ul>
          </div>
        ))}
      </div>
    </div>
  );
}
