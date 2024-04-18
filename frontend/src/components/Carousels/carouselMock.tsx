import image from './img/Rectangle 106.svg'
import image2 from './img/1 (2).svg'
import image3 from './img/2.svg'
import image4 from './img/4.svg'
import image5 from './img/Keramic.svg';
import image6 from './img/Glas.svg';
import image11 from '../../assets/collection/Rectangle 40.svg';
import image12 from '../../assets/collection/Rectangle 41.svg'
import image13 from '../../assets/collection/Rectangle 42.svg'
import image14 from '../../assets/collection/Rectangle 43.svg'
import image15 from '../../assets/collection/Rectangle 44.svg'
import image16 from '../../assets/collection/Rectangle 36.svg';
import image17 from '../../assets/collection/Rectangle 37.svg'
import image18 from '../../assets/collection/Rectangle 38.svg'
import image19 from '../../assets/collection/Rectangle 39.svg'
import image20 from '../../assets/ethno/Rectangle 45.svg'
import image21 from '../../assets/ethno/Rectangle 46.svg'
import image22 from '../../assets/ethno/Rectangle 47.svg'
import image23 from '../../assets/ethno/Rectangle 48.svg'
import image24 from '../../assets/ethno/Rectangle 49.svg'
import image25 from '../../assets/ethno/Rectangle 62.svg'

interface Product {
    name: string;
    price: string;
    imageUrl: string;
    newPrice?: string;
    category?: string;
}

export const mockDataProducts: Product[] = [
    {
        name: 'Цукерниця чорна',
        price: '9700,00 грн',
        imageUrl: image
    },
    {
        name: 'Набір з 2 тарілок',
        price: '3000,00 грн',
        imageUrl: image2
    },
    {
        name: 'Керамічний глек',
        price: '2400,00 грн',
        imageUrl: image3
    },
    {
        name: '111111111',
        price: '500,00 грн',
        imageUrl: image4
    },
    {
        name: '222222222',
        price: '2000,00 грн',
        imageUrl: image2
    },
    {
        name: '333333333',
        price: '400,00 грн',
        imageUrl: image3
    },
    {
        name: '444444444',
        price: '6600,00 грн',
        imageUrl: image4
    },
    {
        name: '55555555',
        price: '6600,00 грн',
        imageUrl: image4
    },
    {
        name: 'Керамічний глек',
        price: '2400,00 грн',
        imageUrl: image3
    },
];


export const mockDataPopular: Product[] = [
    {
        name: 'Цукерниця чорна',
        price: '9700 грн',
        imageUrl: image
    },
    {
        name: 'Набір з 2 тарілок',
        price: '3000 грн',
        imageUrl: image2
    },
    {
        name: 'Керамічний глек',
        price: '2400 грн',
        imageUrl: image3
    },
    {
        name: '111111111',
        price: '500 грн',
        imageUrl: image4
    },
    {
        name: '222222222',
        price: '2000 грн',
        imageUrl: image2
    },
    {
        name: '333333333',
        price: '400 грн',
        imageUrl: image3
    },
    {
        name: '444444444',
        price: '6600 грн',
        imageUrl: image4
    },
];


export const mockDataCategories = [
    {
        name: 'Кераміка',
        imageUrl: image5
    },
    {
        name: 'Скло',
        imageUrl: image6
    },
];


export const mockDataAllCollection: Product[] = [
    {
        name: 'Колекція  “Вода”',
        imageUrl: image16,
        price:'',
        category:'скло'
    },
    {
        name: 'Колекція  “Етно-шик”',
        imageUrl: image17,
        price:'',
        category:'аксесуари'
    },
    {
        name: 'Колекція  “ Керамічний фольклор”',
        imageUrl: image18,
        price:'',
        category:'кераміка'
    },
    {
        name: 'Колекція “Великдень”',
        imageUrl: image19,
        price:'',
        category:''
    },
    {
        name: 'Колекція “Дракон””',
        imageUrl: image11,
        price:'',
        category:''
    },
    {
        name: 'Колекція шовкових хусток',
        imageUrl: image12,
        price:'',
        category:''
    },
    {
        name: 'Каблучки',
        imageUrl: image13,
        price:'',
        category:''
    },
    {
        name: 'Сережки',
        imageUrl: image14,
        price:'',
        category:''
    },
    {
        name: 'Підвіски',
        imageUrl: image15,
        price:'',
        category:''
    }
]

export const mockDataDiscount: Product[]= [

    {
        name: 'Сова',
        price: '4200 грн',
        newPrice:'3500 грн',
        imageUrl: image4
    },
    {
        name: 'Цукерниця чорна',
        price: '8700 грн',
        newPrice:'5000 грн',
        imageUrl: image
    },
    {
        name: 'Набір з 2 тарілок',
        price: '2400 грн',
        newPrice:'2000 грн',
        imageUrl: image3
    },
    {
        name: '444444444',
        price: '6600 грн',
        newPrice:'5000 грн',
        imageUrl: image4
    },
    {
        name: 'Набір з 2 чашок',
        price: '3000,00 грн',
        imageUrl: image2,
        newPrice:'1500 грн',

    },
];


export const fullData = {
    collections: [
        {
            id: "1",
            name: "Колекція “Вода”",
            imageUrl: image16,
            category: "скло",
            items: []
        },
        {
            id: "2",
            name: "Колекція “Етно-шик”",
            imageUrl: image17,
            category: "аксесуари",
            items: [
                {
                    name: "Кольє Інвіда",
                    price: "10 500,00 грн",
                    imageUrl: image20
                },
                {
                    name: "Кольє Інвіда",
                    price: "3000,00 грн",
                    imageUrl: image21
                },
                {
                    name: "Підвіска Хрест Криж",
                    price: "2400,00 грн",
                    imageUrl: image22
                },
                {
                    name: "Каблучка Queen",
                    price: "7300,00 грн",
                    imageUrl: image23
                },
                {
                    name: "Шовкова хустинка",
                    price: "3300,00 грн",
                    imageUrl: image24
                },
                {
                    name: "Підсвічники",
                    price: "5000,00 грн",
                    imageUrl: image25
                }
            ]
        },
        {
            id: "3",
            name: "Колекція “ Керамічний фольклор”",
            imageUrl: image18,
            category: "кераміка",
            items: [
                {
                    name: 'Цукерниця чорна',
                    price: '9700,00 грн',
                    imageUrl: image
                },
                {
                    name: 'Набір з 2 тарілок',
                    price: '3000,00 грн',
                    imageUrl: image2
                },
                {
                    name: 'Керамічний глек',
                    price: '2400,00 грн',
                    imageUrl: image3
                },
                {
                    name: '111111111',
                    price: '500,00 грн',
                    imageUrl: image4
                },
                {
                    name: '222222222',
                    price: '2000,00 грн',
                    imageUrl: image2
                },
                {
                    name: '333333333',
                    price: '400,00 грн',
                    imageUrl: image3
                },
                {
                    name: '444444444',
                    price: '6600,00 грн',
                    imageUrl: image4
                },
                {
                    name: '55555555',
                    price: '6600,00 грн',
                    imageUrl: image4
                }
            ]
        },
        {
            id: "4",
            name: "Колекція “Великдень”",
            imageUrl: image19,
            category: "",
            items: []
        },
        {
            id: "5",
            name: "Колекція “Дракон””",
            imageUrl: image11,
            category: "",
            items: []
        },
        {
            id: "6",
            name: "Колекція шовкових хусток",
            imageUrl: image12,
            category: "",
            items: []
        },
        {
            id: "7",
            name: "Каблучки",
            imageUrl: image13,
            category: "",
            items: []
        },
        {
            id: "8",
            name: "Сережки",
            imageUrl: image14,
            category: "",
            items: []
        },
        {
            id: "9",
            name: "Підвіски",
            imageUrl: image15,
            category: "",
            items: []
        }
    ]
}
