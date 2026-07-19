/** Applies the Redux `theme` value to the <html> element's class list for Tailwind's dark: variant. */
import { useEffect } from 'react';
import { useSelector } from 'react-redux';

export default function useDarkMode() {
  const theme = useSelector((s) => s.ui.theme);

  useEffect(() => {
    const root = document.documentElement;
    if (theme === 'dark') root.classList.add('dark');
    else root.classList.remove('dark');
  }, [theme]);

  return theme;
}
