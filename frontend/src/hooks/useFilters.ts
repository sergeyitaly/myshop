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
    const [tempHasDiscount, setTempHasDiscount] = useState<boolean>(false)
    
    const [activeCategories, setActiveCategories] = useState<Category[]>([]);
    const [activeCollections, setActiveCollections] = useState<Collection[]>([]);
    const [activePriceValues, setActivePriceValues] = useState<PriceRange>({ min: minValue, max: maxValue });
    const [activeHasDiscount, setActiveHasDiscount] = useState<boolean>(false);
    
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

        if (discount) {
            list.push({
                type: 'discount',
                value: 'Discounted' 
            });
        }
        return list;
    };

    useEffect(() => {
        setTagList(createTags(activeCategories, activeCollections, activePriceValues, activeHasDiscount));
    }, [i18n.language, activeCategories, activeCollections, activePriceValues, activeHasDiscount]);

    useEffect(() => {
        if (initialCollection) {
            setActiveCollections([initialCollection]);
        }
    }, [initialCollection]);

    useEffect(() => {
        // setTagList(createTags(activeCategories, activeCollections, activePriceValues, activeHasDiscount));

        // Set filters based on active states, excluding default values
        const newFilter: MainFilter = {
            ...filter,
            category: activeCategories.map(({ id }) => id).join(','),
            collection: activeCollections.map(({ id }) => id).join(','),
            price_min: activePriceValues.min !== minValue ? activePriceValues.min : undefined,
            price_max: activePriceValues.max !== maxValue ? activePriceValues.max : undefined,
            ordering: sortBy,
            has_discount: activeHasDiscount 
        }

        if(!activeHasDiscount) delete newFilter.has_discount

        setFilter(newFilter);
    }, [activeCategories, activePriceValues, activeCollections, sortBy, activeHasDiscount]);

    useEffect(() => {

        setTempCategories(activeCategories)
        setTempCollections(activeCollections)
        setTempPriceValues(activePriceValues)
        setTempHasDiscount(activeHasDiscount)

    }, [activeCategories, activePriceValues, activeCollections, activeHasDiscount])

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

    const changeDiscount = (discount: boolean) => {
        setTempHasDiscount(discount);
    };

    const clearAllFilters = () => {
        setActiveCategories([]);
        setActivePriceValues({ min: minMaxPrice[0], max: minMaxPrice[1] });
        setActiveCollections([]);
        setTempCategories([]);
        setTempCollections([]);
        setTempHasDiscount(false);
        setActiveHasDiscount(false)
    };

    const applyChanges = () => {
        setActiveCategories(tempCategories);
        setActivePriceValues(tempPriceValues);
        setActiveCollections(tempCollections);
        setActiveHasDiscount(tempHasDiscount)
    };

    const deleteTag = (tag: Tag) => {
        if (tag.type === 'price') {
            setActivePriceValues({ min: minMaxPrice[0], max: minMaxPrice[1] });
        }
        if (tag.type === 'category') {
            setActiveCategories(activeCategories.filter((category) => getCategoryName(category) !== tag.value));
        }
        if (tag.type === 'collection') {
            setActiveCollections(activeCollections.filter((collection) => getCollectionName(collection) !== tag.value));
        }
        if (tag.type === 'discount') {
            setActiveHasDiscount(false);
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
        tempHasDiscount,
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
