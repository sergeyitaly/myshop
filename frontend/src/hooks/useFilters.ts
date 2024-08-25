import { useEffect, useState } from "react";
import { Category, Collection } from "../models/entities";
import { MainFilter } from "../models/filters";
import { formatNumber } from "../functions/formatNumber";
import { formatCurrency } from "../functions/formatCurrency";
import { useTranslation } from "react-i18next"; // Import useTranslation hook
import { Currency } from "../models/entities"; // Import Currency type

interface Tag {
    type: 'category' | 'collection' | 'price' | 'discount';
    value: string;
}

export const useFilters = (initialCollection?: Collection) => {
    const maxValue = 1000000;
    const minValue = 0;

    const [tempCategories, setTempCategories] = useState<Category[]>([]);
    const [tempCollections, setTempCollections] = useState<Collection[]>([]);
    const [tempPriceValues, setTempPriceValues] = useState<[number, number]>([0, 0]);
    const [hasDiscount, setHasDiscount] = useState<boolean | null>(null); // New state for has_discount

    const [activeCategories, setActiveCategories] = useState<Category[]>([]);
    const [activeCollections, setActiveCollections] = useState<Collection[]>([]);
    const [activePriceValues, setActivePriceValues] = useState<[number, number]>([minValue, maxValue]);
    
    const [filter, setFilter] = useState<MainFilter>({});
    const [tagList, setTagList] = useState<Tag[]>([]);

    const [sortBy, setSortBy] = useState<string>('');

    const { i18n } = useTranslation(); // Use the useTranslation hook

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
                return 'UAH'; // Ukrainian Hryvnia
            case 'en':
                return 'USD'; // US Dollar
            case 'fr':
                return 'EUR'; // Euro, assuming French for demonstration
            default:
                return 'USD'; // Default to US Dollar
        }
    };

    const createTags = (categories: Category[] = [], collections: Collection[] = [], price: [number, number], discount: boolean | null) => {
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
        if (price[0] !== minValue || price[1] !== maxValue) {
            list.push({
                type: 'price',
                value: `${formatNumber(price[0])} - ${formatNumber(price[1])} ${formatCurrency(currencyFormat)}`
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
        setTempCategories(activeCategories);
        setTempPriceValues(activePriceValues);
        setTempCollections(activeCollections);
    
        setFilter((state) => ({
            ...state, 
            category: activeCategories.map(({id}) => id).join(','),
            collection: activeCollections.map(({id}) => id).join(','),
            price_min: activePriceValues[0],
            price_max: activePriceValues[1],
            ordering: sortBy,
            has_discount: state.has_discount // Ensure `has_discount` remains as a boolean or undefined
        }));
    }, [activeCategories, activePriceValues, activeCollections, sortBy]);
    

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

    const changePrice = (price: [number, number]) => {
        setTempPriceValues(price);
    };

    // New function to handle discount filter change
    const changeDiscount = (discount: boolean | null) => {
        setHasDiscount(discount);
    };

    const clearAllFilters = () => {
        setActiveCategories([]);
        setActivePriceValues([minValue, maxValue]);
        setActiveCollections([]);
        setHasDiscount(null); // Reset has_discount filter
    };

    const applyChanges = () => {
        setActiveCategories(tempCategories);
        setActivePriceValues(tempPriceValues);
        setActiveCollections(tempCollections);
    };

    const deleteTag = (tag: Tag) => {
        if (tag.type === 'price') {
            setActivePriceValues([minValue, maxValue]);
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
        changeDiscount, // Include changeDiscount in the return object
    };
};
