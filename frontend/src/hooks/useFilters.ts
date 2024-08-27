import { useEffect, useState } from "react";
import { Category, Collection, Currency } from "../models/entities";
import { MainFilter } from "../models/filters";
import { formatNumber } from "../functions/formatNumber";
import { formatCurrency } from "../functions/formatCurrency";
import { useTranslation } from "react-i18next";

interface Tag {
    type: 'category' | 'collection' | 'price' | 'discount';
    value: string;
}

interface PriceRange {
    min: number;
    max: number;
}


export const useFilters = (initialCollection?: Collection ) => {
    const maxValue = 1000000;
    const minValue = 0;

    const [minMaxPrice, setMinMaxPrice] = useState<[number, number]>([minValue, maxValue])

    const [tempCategories, setTempCategories] = useState<Category[]>([]);
    const [tempCollections, setTempCollections] = useState<Collection[]>([]);
    const [tempPriceValues, setTempPriceValues] = useState<PriceRange>({ min: minValue, max: maxValue });
    const [hasDiscount, setHasDiscount] = useState<boolean | null>(null);

    const [activeCategories, setActiveCategories] = useState<Category[]>([]);
    const [activeCollections, setActiveCollections] = useState<Collection[]>([]);
    const [activePriceValues, setActivePriceValues] = useState<PriceRange>({ min: minValue, max: maxValue });


    
    const [filter, setFilter] = useState<MainFilter>({});
    const [tagList, setTagList] = useState<Tag[]>([]);
    const [sortBy, setSortBy] = useState<string>('');

    const { i18n } = useTranslation();

    const getCategoryName = (category: Category): string => {
        switch (i18n.language) {
            case 'uk':
                return category.name_uk || category.name || '';
            case 'en':
                return category.name_en || category.name || '';
            default:
                return category.name_en || category.name || '';
        }
    };

    const getCollectionName = (collection: Collection): string => {
        switch (i18n.language) {
            case 'uk':
                return collection.name_uk || collection.name || '';
            case 'en':
                return collection.name_en || collection.name || '';
            default:
                return collection.name_en || collection.name || '';
        }
    };

    const getCurrencyFormat = (): Currency => {
        switch (i18n.language) {
            case 'uk':
                return 'UAH';
            case 'en':
                return 'USD';
            case 'fr':
                return 'EUR';
            default:
                return 'USD';
        }
    };

    const createTags = (categories: Category[] = [], collections: Collection[] = [], price: PriceRange, discount: boolean | null) => {
        console.log(tempPriceValues);
        
        let list: Tag[] = [];
        let categoryTags: Tag[] = categories.map((category) => ({
            type: 'category',
            value: getCategoryName(category)
        }));
        let collectionTags: Tag[] = initialCollection ? [] : collections.map((collection) => ({
            type: 'collection',
            value: getCollectionName(collection)
        }));

        list = [...categoryTags, ...collectionTags];

        const currencyFormat = getCurrencyFormat();
        if (price.min !== minMaxPrice[0] || price.max !== minMaxPrice[1]) {
            list.push({
                type: 'price',
                value: `${formatNumber(price.min)} - ${formatNumber(price.max)} ${formatCurrency(currencyFormat)}`
            });
        }

        if (discount !== null) {
            list.push({
                type: 'discount',
                value: discount ? 'Discounted' : 'No Discount'
            });
        }

        return list;
    };

    useEffect(() => {
        setTagList(createTags(activeCategories, activeCollections, activePriceValues, hasDiscount));
    }, [i18n.language, activeCategories, activeCollections, activePriceValues, hasDiscount]);

    useEffect(() => {
        if (initialCollection) {
            setActiveCollections([initialCollection]);
        }
    }, [initialCollection]);

    useEffect(() => {
        setTagList(createTags(activeCategories, activeCollections, activePriceValues, hasDiscount));

        // Set filters based on active states, excluding default values
        setFilter((state) => ({
            ...state,
            category: activeCategories.map(({ id }) => id).join(','),
            collection: activeCollections.map(({ id }) => id).join(','),
            price_min: activePriceValues.min !== minValue ? activePriceValues.min : undefined,
            price_max: activePriceValues.max !== maxValue ? activePriceValues.max : undefined,
            ordering: sortBy,
            has_discount: hasDiscount !== null ? hasDiscount : undefined
        }));
    }, [activeCategories, activePriceValues, activeCollections, sortBy, hasDiscount]);

    const changeCategory = (category: Category) => {
        const alreadyExist = tempCategories.some(({ id }) => id === category.id);
        if (alreadyExist) {
            setTempCategories((state) => state.filter(({ id }) => id !== category.id));
        } else {
            setTempCategories((state) => [...state, category]);
        }
    };

    const changeCollection = (collection: Collection) => {
        const alreadyExist = tempCollections.some(({ id }) => id === collection.id);
        if (alreadyExist) {
            setTempCollections((state) => state.filter(({ id }) => id !== collection.id));
        } else {
            setTempCollections((state) => [...state, collection]);
        }
    };

    const changePrice = (price: PriceRange) => {
        setTempPriceValues(price);
    };

    const changeDiscount = (discount: boolean | null) => {
        setHasDiscount(discount);
    };

    const clearAllFilters = () => {
        setActiveCategories([]);
        setActivePriceValues({ min: minValue, max: maxValue });
        setActiveCollections([]);
        setTempCategories([]);
        setTempCollections([]);
        setHasDiscount(null);
    };

    const applyChanges = () => {
        setActiveCategories(tempCategories);
        setActivePriceValues(tempPriceValues);
        setActiveCollections(tempCollections);
    };

    const deleteTag = (tag: Tag) => {
        if (tag.type === 'price') {
            setActivePriceValues({ min: minValue, max: maxValue });
        }
        if (tag.type === 'category') {
            setActiveCategories(activeCategories.filter((category) => getCategoryName(category) !== tag.value));
        }
        if (tag.type === 'collection') {
            setActiveCollections(activeCollections.filter((collection) => getCollectionName(collection) !== tag.value));
        }
        if (tag.type === 'discount') {
            setHasDiscount(null);
        }
    };

    const changeOrdering = (ordering: string) => {
        setSortBy(ordering);
    };

    return {
        minPrice: minMaxPrice[0],
        maxPrice: minMaxPrice[1],
        tempCategories,
        tempPriceValues,
        tempCollections,
        activeCollections,
        activeCategories,
        price: activePriceValues,
        minValue,
        maxValue,
        filter,
        tagList,
        changeOrdering,
        changeCategory,
        changeCollection,
        changePrice,
        clearAllFilters,
        applyChanges,
        deleteTag,
        changeDiscount,
        setMinMaxPrice
    };
};
