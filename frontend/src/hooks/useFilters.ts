import { useEffect, useState } from "react"
import { Category, Collection } from "../models/entities"
import { MainFilter } from "../models/filters"
import { formatNumber } from "../functions/formatNumber"
import { formatCurrency } from "../functions/formatCurrency"


interface Tag {
    type: 'category' | 'collection' | 'price'
    value: string
}




export const useFilters = (initialCollection?: Collection) => {

    const maxValue = 1000000
    const minValue = 0

    const [tempCategories, setTempCategories] = useState<Category[]>([])
    const [tempCollections, setTempCollections] = useState<Collection[]>([])
    const [tempPriceValues, setTempPriceValues] = useState<[number, number]>([0, 0])

    const [activeCategories, setActiveCategories] = useState<Category[]>([])
    const [activeCollections, setActiveCollections] = useState<Collection[]>([])
    const [activePriceValues, setActivePriceValues] = useState<[number, number]>([minValue, maxValue]);

    const [filter, setFilter] = useState<MainFilter>({})
    const [tagList, setTagList] = useState<Tag[]>([])
    
    const [sortBy, setSortBy] = useState<string>('')
    

    const createTags = (categories: Category[] = [], collections: Collection[] = [], price: [number, number]) => {
        let list: Tag[] = []
        let categoryTags: Tag[]  = categories.map(({name}) => (
            {
                type: 'category',
                value: name
            }
        ))
        let collectionTags: Tag[] =initialCollection ? [] : collections.map(({name}) => ({
            type: 'collection',
            value: name
        }))

        list = [...categoryTags, ...collectionTags]
    
        if (price[0] !== minValue || price[1] !== maxValue){
            list.push({
                type: 'price',
                value: `${formatNumber(price[0])} - ${formatNumber(price[1])} ${formatCurrency('UAH')}`
            })
        }
        
       
        return list
    }

    console.log(initialCollection);
    

    useEffect(() => {
        initialCollection && 
        setActiveCollections([initialCollection])
    }, [initialCollection])

    useEffect(() => {

        setTagList(createTags(activeCategories, activeCollections, activePriceValues))

        setTempCategories(activeCategories)
        setTempPriceValues(activePriceValues)
        setTempCollections(activeCollections)

        setFilter((state) => ({
            ...state, 
            category: activeCategories.map(({id}) => id).join(','),
            collection: activeCollections.map(({id}) => id).join(','),
            price_min: activePriceValues[0],
            price_max: activePriceValues[1],
            ordering: sortBy
        }))

    }, [activeCategories, activePriceValues, activeCollections, sortBy])


    const changeCategory = (category: Category) => {
        const alreadyExist = tempCategories.some(({id}) => id === category.id)
        if(alreadyExist) 
        return setTempCategories((state) => state.filter(({id}) => id !== category.id))
        setTempCategories((state) => [...state, category])
    }

    const changeCollection = (collection: Collection) => {
        const alreadyExist = tempCollections.some(({id}) => id === collection.id)
        if(alreadyExist) 
        return setTempCollections((state) => state.filter(({id}) => id !== collection.id))
        setTempCollections((state) => [...state, collection])
    } 

    const changePrice = (price: [number, number]) => {
        setTempPriceValues(price)
    }

    
    const clearAllFilters = () => {
        setActiveCategories([])
        setActivePriceValues([minValue, maxValue])
        setActiveCollections([])
    }    

    
    const applyChanges = () => {
        setActiveCategories(tempCategories)
        setActivePriceValues(tempPriceValues)
        setActiveCollections(tempCollections)
    }

    const deleteTag = (tag: Tag) => {
        if (tag.type === 'price'){
            setActivePriceValues([minValue, maxValue])
        }
        if(tag.type === 'category'){
            setActiveCategories(activeCategories.filter((category) => category.name !== tag.value ))
        }
        if(tag.type === 'collection'){
            setActiveCollections(activeCollections.filter((collection) => collection.name !== tag.value ))
        }
    }

    const changeOrdering = (ordering: string) => {
        setSortBy(ordering)
    }

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
    }
}