import { useGetAllCategoriesQuery } from "../../../api/categorySlice"
import { TextButton } from "../../../components/UI/TextButton/TextButton"
import { FilterDropDown } from "../FilterDropDown/FilterDropDown"
import { FilterItem } from "../FilterItem/FilterItem"
import {motion} from 'framer-motion'
import styles from './FilterMenu.module.scss'
import { Category } from "../../../models/entities"
import 'react-range-slider-input/dist/style.css';
import { AppRangeSlider } from "../RangeSlider/RangeSlider"


interface FilterMenuProps {
    activeCategories: Category[]
    minValue: number
    maxValue: number
    priceValue: [number, number]
    changePrice: (price: [number, number]) => void
    onClickHideFilters: () => void
    onClickCategory: (category: Category) => void
    onApply: () => void 
}


export const FilterMenu = ({
    activeCategories,
    minValue,
    maxValue,
    priceValue,
    changePrice,
    onClickHideFilters,
    onClickCategory,
    onApply
}: FilterMenuProps) => {

    const {data: categories, isSuccess} = useGetAllCategoriesQuery()

   

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