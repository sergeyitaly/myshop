
export interface SortMenuItem  {
    title: string
    name: string
}

export const sortList: SortMenuItem[] = [
    {
        title: 'Від дорогого до дешевого',
        name: 'price'
    },
    {
        title: 'Від дешевого до дорогого',
        name: '-price'
    },
    {
        title: 'Нові надходження',
        name: 'sales_count'
    },
    {
        title: 'Найпопулярніше',
        name: 'popularity'
    },
    {
        title: 'Знижки',
        name: '-discounted_price'
    },
] 