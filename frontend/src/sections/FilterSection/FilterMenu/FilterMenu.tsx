import { useTranslation } from "react-i18next"; // Import the useTranslation hook
import { Category, Collection } from "../../../models/entities";
import { useGetCategoriesByFilterQuery } from "../../../api/categorySlice";
import { useGetCollectionsByFilterQuery } from "../../../api/collectionSlice";
import { TextButton } from "../../../components/UI/TextButton/TextButton";
import { FilterDropDown } from "../FilterDropDown/FilterDropDown";
import { FilterItem } from "../FilterItem/FilterItem";
import { motion } from "framer-motion";
import styles from "./FilterMenu.module.scss";
import "react-range-slider-input/dist/style.css";
import { AppRangeSlider } from "../RangeSlider/RangeSlider";
import { MainButton } from "../../../components/UI/MainButton/MainButton";
import { useEffect } from "react";
import { TopLevelFilter } from "../TopLevelFilter/TopLevelFilter";

interface FilterMenuProps {
    hasDiscount: boolean;
    initialTopPosition: number
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
    initialTopPosition,
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
    const { i18n, t } = useTranslation(); // Initialize translation hook

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

    // Function to get translated category name
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

    // Function to get translated collection name
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

    const handleChangeSale = () => {
        onChangeSale(!hasDiscount)
    }

    return (
        <motion.div
            className={styles.wrapper}
            initial={{ x: "-100%"}}
            animate={{ x: 0 }}
            exit={{ x: "-100%"}}
            transition={{ ease: "linear" }}
            style={{top: initialTopPosition}}
        >
            <header className={styles.header}>
                <TextButton
                    className={styles.button}
                    title={t("hide")} // Localized text
                    onClick={onClickHideFilters}
                />
            </header>
            <div className={styles.container}>
                {showCollections && (
                    <FilterDropDown
                        title={t("collections")} // Localized text
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
                                            title={getCollectionName(collection)} // Use the function to get the collection name
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
                    title={t("category")} // Localized text
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
                                        title={getCategoryName(category)} // Use the function to get the category name
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
                    title={t("price")} // Localized text
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
                <MainButton 
                    className={styles.saveButton}
                    title={t("save")}
                    color="blue"
                    onClick = {onApply}
                />
            </div>
        </motion.div>
    );
};
