import { useTranslation } from 'react-i18next';

export interface SortMenuItem {
  title: string;
  name: string;
}

export const useSortList = (): SortMenuItem[] => {
  const { t } = useTranslation();

  return [
    {
      title: t('sort.price_descending'),
      name: '-discounted_price'
    },
    {
      title: t('sort.price_ascending'),
      name: 'discounted_price'
    },
    {
      title: t('sort.new_arrivals'),
      name: 'sales_count'
    },
    {
      title: t('sort.most_popular'),
      name: 'popularity'
    },
  ];
};
