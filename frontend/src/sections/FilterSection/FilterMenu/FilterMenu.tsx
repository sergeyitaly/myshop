import { useTranslation } from "react-i18next"; 
import { Category, Collection } from "../../../models/entities";
import { useGetCategoriesByFilterQuery } from "../../../api/categorySlice";
import { useGetCollectionsByFilterQuery } from "../../../api/collectionSlice";
import { FilterDropDown } from "../FilterDropDown/FilterDropDown";
import { FilterItem } from "../FilterItem/FilterItem";
import { motion, Variants } from "framer-motion";
import styles from "./FilterMenu.module.scss";
import "react-range-slider-input/dist/style.css";
import { AppRangeSlider } from "../RangeSlider/RangeSlider";
import { MainButton } from "../../../components/UI/MainButton/MainButton";
import { useEffect } from "react";
import { TopLevelFilter } from "../TopLevelFilter/TopLevelFilter";
import { AppIcon } from "../../../components/SvgIconComponents/AppIcon";
import { Logo } from "../../../components/Logo/Logo";
import { useAppTranslator } from "../../../hooks/useAppTranslator";

export const modal: Variants = {
    hidden: {
        opacity: 0,
    },
    visible: {
        opacity: 1,
    }
}

interface FilterMenuProps {
    hasDiscount: boolean;
    showCollections?: boolean;
    activeCategories?: Category[];
    activeCollections?: Collection[];
    minValue: number;
    maxValue: number;
    priceValue: [number, number];
    changePrice: (price: [number, number]) => void;
    onClickHideFilters: () => void;
    onClickCategory: (category: Category) => void;
    onClickCollection: (collection: Collection) => void;
    onApply: () => void;
    onChangeSale: (value: boolean) => void
}

export const FilterMenu = ({
    hasDiscount,
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
    onApply,
    onChangeSale,
}: FilterMenuProps) => {
    const { t } = useTranslation();
    const { getCategoryName, getCollectionName } = useAppTranslator();

    const { data: categories, isSuccess: isSuccessCategories } = useGetCategoriesByFilterQuery({
        page_size: 8,
    });
    const { data: collections, isSuccess: isSuccessCollections } =
        useGetCollectionsByFilterQuery({
            page_size: 8,
        });

    useEffect(() => {
        window.document.body.style.overflow = 'hidden'

        return () => {
            window.document.body.style.overflow = 'visible'
        }
    }, [])

    const handleChangeSale = () => {
        onChangeSale(!hasDiscount)
    }

    return (
        <motion.div
            className={styles.background}
            variants={modal}
            initial="hidden"
            animate="visible"
            exit="hidden"
        >
            <motion.div
                className={styles.box}
                initial={{ x: "-100%"}}
                animate={{ x: 0 }}
                exit={{ x: "-100%"}}
                transition={{ ease: "linear" }}
            >
                <header className={styles.header}>
                    <Logo className={styles.logo}/>
                    <button onClick={onClickHideFilters}>
                        <AppIcon iconName="cross" />
                    </button>
                </header>
                <div className={styles.container}>
                    {showCollections && (
                        <FilterDropDown
                            title={t("collections")} 
                        >
                            <div className={styles.categoryList}>
                                {isSuccessCollections &&
                                    collections.results.map((collection) => {
                                        const isActive = activeCollections.some(
                                            ({ id }) => id === collection.id
                                        );

                                        return (
                                            <FilterItem
                                                key={collection.id}
                                                title={getCollectionName(collection)}
                                                isActive={isActive}
                                                onClick={() =>
                                                    onClickCollection(collection)
                                                }
                                            />
                                        );
                                    })}
                            </div>
                        </FilterDropDown>
                    )}
                    <FilterDropDown
                        title={t("category")} 
                    >
                        <div className={styles.categoryList}>
                            {isSuccessCategories &&
                                categories.results.map((category) => {
                                    const isActive = activeCategories.some(
                                        ({ id }) => id === category.id
                                    );

                                    return (
                                        <FilterItem
                                            key={category.id}
                                            title={getCategoryName(category)} 
                                            isActive={isActive}
                                            onClick={() =>
                                                onClickCategory(category)
                                            }
                                        />
                                    );
                                })}
                        </div>
                    </FilterDropDown>
                
                    <FilterDropDown
                        title={t("price")} 
                    >
                        <AppRangeSlider
                            minValue={minValue}
                            maxValue={maxValue}
                            value={priceValue}
                            changePrice={changePrice}
                        />
                    </FilterDropDown>
                    <TopLevelFilter
                        isActive = {hasDiscount}
                        title={t('discounts')}
                        onClick={ handleChangeSale }
                    />
                    
                </div>
                <div className={styles.actions}>
                    <MainButton 
                        className={styles.saveButton}
                        title={t("save")}
                        color="blue"
                        onClick = {onApply}
                    />
                </div>
            </motion.div>
        </motion.div>
    );
};
