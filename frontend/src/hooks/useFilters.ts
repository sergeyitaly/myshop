import { useEffect, useState } from "react";
import { Category, Collection } from "../models/entities";
import { MainFilter } from "../models/filters";
import { formatNumber } from "../functions/formatNumber";
import { formatCurrency } from "../functions/formatCurrency";
import { useAppTranslator } from "./useAppTranslator";

interface Tag {
    type: 'category' | 'collection' | 'price' | 'discount';
    value: string;
}

interface PriceRange {
    min: number;
    max: number;
}


export const useFilters = (initialCollection?: Collection ) => {

    const [fullRangeOfPrice, setFullRangeOfPrice] = useState<[number, number]>([0, 0])

console.log('fullRangeOfPrice', fullRangeOfPrice);

    const [tempCategories, setTempCategories] = useState<Category[]>([]);
    const [tempCollections, setTempCollections] = useState<Collection[]>([]);
    const [tempPriceValues, setTempPriceValues] = useState<PriceRange>({ min: fullRangeOfPrice[0], max: fullRangeOfPrice[1]});
    const [tempHasDiscount, setTempHasDiscount] = useState<boolean>(false)
    
    const [activeCategories, setActiveCategories] = useState<Category[]>([]);
    const [activeCollections, setActiveCollections] = useState<Collection[]>([]);
    const [activePriceValues, setActivePriceValues] = useState<PriceRange>({ min: fullRangeOfPrice[0], max: fullRangeOfPrice[1] });
    const [activeHasDiscount, setActiveHasDiscount] = useState<boolean>(false);
    
    const [filter, setFilter] = useState<MainFilter>({});
    const [tagList, setTagList] = useState<Tag[]>([]);
    const [sortBy, setSortBy] = useState<string>('');

    const {
        i18n,
        getCategoryName,
        getCollectionName,
    } = useAppTranslator()


    const createTags = (categories: Category[] = [], collections: Collection[] = [], price: PriceRange, discount: boolean | null) => {
        
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

        if ((!!price.min && price.min > fullRangeOfPrice[0]) || (!!price.max && price.max < fullRangeOfPrice[1])) {
            list.push({
                type: 'price',
                value: `${formatNumber(price.min)} - ${formatNumber(price.max)} ${formatCurrency('UAH')}`
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
       
        setTempPriceValues({min: fullRangeOfPrice[0], max: fullRangeOfPrice[1]})
        // setActivePriceValues({min: fullRangeOfPrice[0], max: fullRangeOfPrice[1]})
    }, [fullRangeOfPrice[0], fullRangeOfPrice[1]])

    useEffect(() => {
        setTagList(createTags(activeCategories, activeCollections, activePriceValues, activeHasDiscount));
    }, [i18n.language, activeCategories, activeCollections, activePriceValues, activeHasDiscount]);

    useEffect(() => {
        if (initialCollection) {
            setActiveCollections([initialCollection]);
        }
    }, [initialCollection]);

    useEffect(() => {
        // Set filters based on active states, excluding default values
        console.log('activeCategories', activeCategories);
        console.log('activeCollections', activeCollections);
        console.log('activePriceValues', activePriceValues);

        const newFilter: MainFilter = {
            ...filter,
            category: activeCategories.length ? activeCategories.map(({ id }) => id).join(',') : undefined,
            collection: activeCollections.length ? activeCollections.map(({ id }) => id).join(',') : undefined,
            price_min: activePriceValues.min || undefined,
            price_max: activePriceValues.max || undefined,
            ordering: sortBy || undefined,
            has_discount: activeHasDiscount || undefined
        }

        if(activePriceValues.min === fullRangeOfPrice[0]) delete newFilter.price_min
        if(activePriceValues.max === fullRangeOfPrice[1]) delete newFilter.price_max 

        // if(!activeHasDiscount) delete newFilter.has_discount
        // if(!fullRangeOfPrice[0]) delete newFilter.price_min
        // if(!fullRangeOfPrice[1]) delete newFilter.price_max

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
        setActivePriceValues({ min: fullRangeOfPrice[0], max: fullRangeOfPrice[1] });
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
            // setActivePriceValues({ min: fullRangeOfPrice[0], max: fullRangeOfPrice[1] });
            setActivePriceValues({ min: 0, max: 0 });
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
        fullRangeOfPrice,
        tempCategories,
        tempPriceValues,
        tempCollections,
        activeCollections,
        activeCategories,
        price: activePriceValues,
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
        setFullRangeOfPrice,
    };
};
