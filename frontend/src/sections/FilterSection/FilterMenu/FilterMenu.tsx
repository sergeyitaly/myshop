import { useGetAllCategoriesQuery } from "../../../api/categorySlice"
import { TextButton } from "../../../components/UI/TextButton/TextButton"
import { FilterDropDown } from "../FilterDropDown/FilterDropDown"
import { FilterItem } from "../FilterItem/FilterItem"
import {motion} from 'framer-motion'
import styles from './FilterMenu.module.scss'
import { Category, Collection } from "../../../models/entities"
import 'react-range-slider-input/dist/style.css';
import { AppRangeSlider } from "../RangeSlider/RangeSlider"
import { useGetCollectionsByFilterQuery } from "../../../api/collectionSlice"


interface FilterMenuProps {
    showCollections?: boolean
    activeCategories?: Category[]
    activeCollections?: Collection[]
    minValue: number
    maxValue: number
    priceValue: [number, number]
    changePrice: (price: [number, number]) => void
    onClickHideFilters: () => void
    onClickCategory: (category: Category) => void
    onClickCollection: (collection: Collection) => void
    onApply: () => void 
}


export const FilterMenu = ({
    showCollections,
    activeCategories = [],
    activeCollections = [],
    minValue,
    maxValue,
    priceValue,
    changePrice,
    onClickHideFilters,
    onClickCollection,
    onClickCategory,
    onApply
}: FilterMenuProps) => {

    const {data: categories, isSuccess} = useGetAllCategoriesQuery()
    const {data: collections, isSuccess: isSuccessGettingCollections} = useGetCollectionsByFilterQuery({
        page_size: 100
    })

   

    return (
        <motion.div 
            className={styles.wrapper}
            initial = {{x: '-100%'}}
            animate = {
                {
                    x: 0
                }
            }
            exit={{x: '-100%'}}
            transition={{ease: 'linear'}}
        >
            <header className={styles.header}>
                <TextButton
                    className={styles.button}
                    title={'Сховати'}
                    onClick={onClickHideFilters}
                />
            </header>
            <div className={styles.container}>
                {
                    showCollections &&
                <FilterDropDown
                    title="Колекції"
                > 
                    <div className={styles.categoryList}>
                        {
                            isSuccessGettingCollections &&
                            collections.results.map((collection) => {

                                const isActive = activeCollections.some(({id}) => id === collection.id)

                                return (
                                    <FilterItem
                                        key={collection.id}
                                        title={collection.name}
                                        isActive = {isActive}
                                        onClick = {() => onClickCollection(collection)}
                                    />
                                )    
                            })
                        }
                    </div>
                </FilterDropDown>
                }
                <FilterDropDown
                    title="Категорія"
                > 
                    <div className={styles.categoryList}>
                        {
                            isSuccess &&
                            categories.results.map((category) => {

                                const isActive = activeCategories.some(({id}) => id === category.id)

                                return (
                                    <FilterItem
                                        key={category.id}
                                        title={category.name}
                                        isActive = {isActive}
                                        onClick = {() => onClickCategory(category)}
                                    />
                                )    
                            })
                        }
                    </div>
                </FilterDropDown>
                <FilterDropDown
                    title="Ціна"
                >
                    <AppRangeSlider
                        minValue={minValue}
                        maxValue={maxValue}
                        value={priceValue}
                        changePrice={changePrice}
                    />
                </FilterDropDown>
                <button
                    onClick = {onApply}
                >
                    Застосувати
                </button>
            </div>
        </motion.div>
    )
}