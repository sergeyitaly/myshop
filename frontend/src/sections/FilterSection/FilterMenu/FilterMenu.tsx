import { useTranslation } from "react-i18next"; // Import the useTranslation hook
import { Category, Collection } from "../../../models/entities";
import { useGetAllCategoriesQuery } from "../../../api/categorySlice";
import { TextButton } from "../../../components/UI/TextButton/TextButton";
import { FilterDropDown } from "../FilterDropDown/FilterDropDown";
import { FilterItem } from "../FilterItem/FilterItem";
import { motion } from "framer-motion";
import styles from "./FilterMenu.module.scss";
import "react-range-slider-input/dist/style.css";
import { AppRangeSlider } from "../RangeSlider/RangeSlider";
import { MainButton } from "../../../components/UI/MainButton/MainButton";

interface FilterMenuProps {
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
}

export const FilterMenu = ({
    activeCategories = [],
    minValue,
    maxValue,
    priceValue,
    changePrice,
    onClickHideFilters,
    onClickCategory,
    onApply,
}: FilterMenuProps) => {
    const { i18n, t } = useTranslation(); // Initialize translation hook

    const { data: categories, isSuccess: isSuccessCategories } = useGetAllCategoriesQuery();

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

    return (
        <motion.div
            className={styles.wrapper}
            initial={{ x: "-100%" }}
            animate={{ x: 0 }}
            exit={{ x: "-100%" }}
            transition={{ ease: "linear" }}
        >
            <header className={styles.header}>
                <TextButton
                    className={styles.button}
                    title={t("hide")} // Localized text
                    onClick={onClickHideFilters}
                />
            </header>
            <div className={styles.container}>

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
                <MainButton 
                    className={styles.saveButton}
                    title="Зберегти"
                    color="blue"
                    onClick = {onApply}
                />
            </div>
        </motion.div>
    );
};
