/** Shared frontend constants mirroring the backend enums. */
export const DISASTER_TYPES = [
  { value: 'flood', label: 'Flood' },
  { value: 'fire', label: 'Fire' },
  { value: 'earthquake', label: 'Earthquake' },
  { value: 'cyclone', label: 'Cyclone' },
  { value: 'tsunami', label: 'Tsunami' },
  { value: 'landslide', label: 'Landslide' },
  { value: 'building_damage', label: 'Building Damage' },
  { value: 'other', label: 'Other' },
];

export const SEVERITY_COLORS = {
  low: 'bg-safe-100 text-safe-800 dark:bg-safe-900/40 dark:text-safe-300',
  moderate: 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900/40 dark:text-yellow-300',
  high: 'bg-orange-100 text-orange-800 dark:bg-orange-900/40 dark:text-orange-300',
  critical: 'bg-primary-100 text-primary-800 dark:bg-primary-900/40 dark:text-primary-300',
};

export const LANGUAGES = [
  { code: 'en', label: 'English' },
  { code: 'hi', label: 'हिन्दी' },
  { code: 'kn', label: 'ಕನ್ನಡ' },
  { code: 'es', label: 'Español' },
];

export const REPORT_STATUSES = ['pending', 'verified', 'in_progress', 'resolved', 'rejected'];
