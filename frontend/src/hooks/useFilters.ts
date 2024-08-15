import { useEffect, useState } from "react";
import { Category, Collection } from "../models/entities";
import { MainFilter } from "../models/filters";
import { formatNumber } from "../functions/formatNumber";
import { formatCurrency } from "../functions/formatCurrency";
import { useTranslation } from "react-i18next"; // Import useTranslation hook
import { Currency } from "../models/entities"; // Import Currency type

interface Tag {
    type: 'category' | 'collection' | 'price';
    value: string;
}

export const useFilters = (initialCollection?: Collection) => {
    const maxValue = 1000000;
    const minValue = 0;

    const [tempCategories, setTempCategories] = useState<Category[]>([]);
    const [tempCollections, setTempCollections] = useState<Collection[]>([]);
    const [tempPriceValues, setTempPriceValues] = useState<[number, number]>([0, 0]);

    const [activeCategories, setActiveCategories] = useState<Category[]>([]);
    const [activeCollections, setActiveCollections] = useState<Collection[]>([]);
    const [activePriceValues, setActivePriceValues] = useState<[number, number]>([minValue, maxValue]);

    const [filter, setFilter] = useState<MainFilter>({});
    const [tagList, setTagList] = useState<Tag[]>([]);

    const [sortBy, setSortBy] = useState<string>('');

    const { i18n } = useTranslation(); // Use the useTranslation hook

    // Function to get category name based on the current language
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

    // Function to get collection name based on the current language
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

    // Function to get currency format based on the current language
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

    // Create tags with translated names and currency
    const createTags = (categories: Category[] = [], collections: Collection[] = [], price: [number, number]) => {
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

        return list;
    };

    // Update filters and tags when language changes
    useEffect(() => {
        setTagList(createTags(activeCategories, activeCollections, activePriceValues));
    }, [i18n.language, activeCategories, activeCollections, activePriceValues]);

    // Update active collections when initialCollection changes
    useEffect(() => {
        if (initialCollection) {
            setActiveCollections([initialCollection]);
        }
    }, [initialCollection]);

    // Update filter and tag list based on active categories, collections, and other settings
    useEffect(() => {
        setTagList(createTags(activeCategories, activeCollections, activePriceValues));

        setTempCategories(activeCategories);
        setTempPriceValues(activePriceValues);
        setTempCollections(activeCollections);

        setFilter((state) => ({
            ...state,
            category: activeCategories.map(({ name }) => name).join(','),
            collection: activeCollections.map(({ id }) => id).join(','),
            price_min: activePriceValues[0],
            price_max: activePriceValues[1],
            ordering: sortBy
        }));
    }, [activeCategories, activePriceValues, activeCollections, sortBy]);

    // Handle category change
    const changeCategory = (category: Category) => {
        const alreadyExist = tempCategories.some(({ id }) => id === category.id);
        if (alreadyExist) {
            setTempCategories((state) => state.filter(({ id }) => id !== category.id));
        } else {
            setTempCategories((state) => [...state, category]);
        }
    };

    // Handle collection change
    const changeCollection = (collection: Collection) => {
        const alreadyExist = tempCollections.some(({ id }) => id === collection.id);
        if (alreadyExist) {
            setTempCollections((state) => state.filter(({ id }) => id !== collection.id));
        } else {
            setTempCollections((state) => [...state, collection]);
        }
    };

    // Handle price change
    const changePrice = (price: [number, number]) => {
        setTempPriceValues(price);
    };

    // Clear all filters
    const clearAllFilters = () => {
        setActiveCategories([]);
        setActivePriceValues([minValue, maxValue]);
        setActiveCollections([]);
    };

    // Apply changes to filters
    const applyChanges = () => {
        setActiveCategories(tempCategories);
        setActivePriceValues(tempPriceValues);
        setActiveCollections(tempCollections);
    };

    // Delete tag
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
    };

    // Change ordering
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
        deleteTag
    };
};
