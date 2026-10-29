import data from '../data/joomla.json';

export const articles = data.articles;
export const articleMenus = data.menus;
export type Article = (typeof articles)[number];

export function formatDate(value: string | null): string {
  if (!value) return 'Data non disponibile';
  // Source wall time, not converted to the build machine's timezone.
  const [year, month, day] = value.slice(0, 10).split('-');
  return `${day}/${month}/${year}`;
}
