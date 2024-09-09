import { useTranslation } from 'react-i18next';

export const useLinks = () => {
  const { t } = useTranslation();

  return [
    {
      href: '/collections',
      name: t('collections'),
    },
    {
      href: '/*',
      name: t('about_us'),
    },
    {
      href: '/contacts',
      name: t('contacts'),
    }
  ];
};
