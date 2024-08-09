import { useEffect, useState } from "react"
import { Category } from "../models/entities"
import { MainFilter } from "../models/filters"
import { nanoid } from "@reduxjs/toolkit"
import { formatNumber } from "../functions/formatNumber"
import { formatCurrency } from "../functions/formatCurrency"


interface Tag {
    type: 'category' | 'price'
    id: string
    value: string
}


export const useFilters = () => {

    const maxValue = 1000000
    const minValue = 0

    const [tempCategories, setTempCategories] = useState<Category[]>([])
    const [tempPriceValues, setTempPriceValues] = useState<[number, number]>([0, 0])
    const [activeCategories, setActiveCategories] = useState<Category[]>([])
    const [activePriceValues, setActivePriceValues] = useState<[number, number]>([minValue, maxValue]);
    const [filter, setFilter] = useState<MainFilter>({ordering: 'price'})
    const [tagList, setTagList] = useState<Tag[]>([])

    const createTags = (categories: Category[], price: [number, number]) => {
        let list: Tag[]  = categories.map(({name}) => {
                const id = nanoid()
                return {
                    type: 'category',
                    id: id,
                    value: name
                }
            })
        if (price[0] !== minValue || price[1] !== maxValue){
            list.push({
                id: nanoid(),
                type: 'price',
                value: `${formatNumber(price[0])} - ${formatNumber(price[1])} ${formatCurrency('UAH')}`
            })
        }
       
        return list
    }

    useEffect(() => {

        setTagList(createTags(activeCategories, activePriceValues))

        setTempCategories(activeCategories)
        setTempPriceValues(activePriceValues)

        setFilter((state) => ({
            ...state, 
            category: activeCategories.map(({name}) => name).join(','),
            price_min: activePriceValues[0],
            price_max: activePriceValues[1]
        }))

    }, [activeCategories, activePriceValues])



    const changeCategory = (category: Category) => {
        const alreadyExist = activeCategories.some(({id}) => id === category.id)
        if(alreadyExist) 
        return setTempCategories((state) => state.filter(({id}) => id !== category.id))
        setTempCategories((state) => [...state, category])
    }

    const changePrice = (price: [number, number]) => {
        setTempPriceValues(price)
    }

    
    const clearAllFilters = () => {
        setActiveCategories([])
        setActivePriceValues([minValue, maxValue])
    }    

    
    const applyChanges = () => {
        setActiveCategories(tempCategories)
        setActivePriceValues(tempPriceValues)
    }

    const deleteTag = (tag: Tag) => {
        if (tag.type === 'price'){
            setActivePriceValues([minValue, maxValue])
        }
        if(tag.type === 'category'){
            setActiveCategories(activeCategories.filter((category) => category.name !== tag.value ))
        }
    }

    return {
        tempCategories,
        tempPriceValues,
        activeCategories,
        price: activePriceValues,
        minValue,
        maxValue,
        filter,
        tagList,
        changeCategory,
        changePrice,
        clearAllFilters,
        applyChanges,
        deleteTag
    }
}