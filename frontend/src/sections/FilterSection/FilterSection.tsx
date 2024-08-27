import { useCallback, useEffect, useState } from "react";
import { PageContainer } from "../../components/containers/PageContainer";
import styles from './FilterSection.module.scss';
import { TextButton } from "../../components/UI/TextButton/TextButton";
import { PreviewCard } from "../../components/Cards/PreviewCard/PreviewCard";
import { PreviewItemsContainer } from "../../components/containers/PreviewItemsContainer/PreviewItemsContainer";
import { FilterMenu } from "./FilterMenu/FilterMenu";
import { AnimatePresence } from "framer-motion";
import { useFilters } from "../../hooks/useFilters";
import { Tag } from "./Tag/Tag";
import { Pagination } from "../../components/UI/Pagination/Pagination";
import { Collection, Product, Category, PriceRange } from '../../models/entities';
import clsx from "clsx";
import { useTranslation } from 'react-i18next';
import { SortMenu } from "./SortMenu/SortMenu";
import { useToggler } from "../../hooks/useToggler";
import { useNavigate } from "react-router-dom";
import { ROUTE } from "../../constants";
import { useSortList } from "./SortList";
import { useGetProductsByMainFilterQuery } from "../../api/productSlice";
import { useDebounce } from 'use-debounce';

interface FilterSectionProps {
    initialCollection?: Collection;
}

export const FilterSection = ({
    initialCollection
}: FilterSectionProps) => {

    const navigate = useNavigate()

    const [currentPage, setCurrentPage] = useState<number>(1);
    
    const {
        activeCategories,
        activeCollections,
        tempCategories,
        tempCollections,
        tagList,
        filter,
        deleteTag,
        applyChanges,
        changeCategory,
        changeCollection,
        changePrice,
        clearAllFilters,
        changeOrdering,
    } = useFilters(initialCollection);

    const [debouncedFilter] = useDebounce(filter, 500); // Debounce filter changes

    const { t, i18n } = useTranslation();

    const {
        openStatus: open,
        handleOpen: handleOpenMenu,
        handleClose: handleCloseMenu
    } = useToggler();

    const {
        openStatus: openSort,
        handleClose: handleClickOutsideSort,
        handleOpen: handleClickSort
    } = useToggler();

    const isFilterEmpty = !Object.keys(filter).length;
    const pageSize = 8;

    // Use debounced filter for API query
    const { data: productsData, isFetching, isError } = useGetProductsByMainFilterQuery({
        ...debouncedFilter,
        page: currentPage,
        page_size: pageSize
    });

    const filteredProducts = productsData?.results || [];
    const totalPages = Math.ceil((productsData?.count || 0) / pageSize);

    useEffect(() => {
        // Reset page to 1 if filters change
        if (!isFilterEmpty) {
            setCurrentPage(1);
        }
    }, [filter, isFilterEmpty]);

    const handleChangePage = useCallback((page: number) => {
        setCurrentPage(page);
    }, []);

    const handleApply = useCallback(() => {
        applyChanges();
        handleCloseMenu();
    }, [applyChanges, handleCloseMenu]);

    const sortList = useSortList();

    const getTranslatedCollectionName = useCallback((collection?: Collection): string => {
        return i18n.language === 'uk'
            ? collection?.name_uk || collection?.name || ''
            : collection?.name_en || collection?.name || '';
    }, [i18n.language]);

    const getTranslatedCategoryName = useCallback((category?: Category): string => {
        return i18n.language === 'uk'
            ? category?.name_uk || category?.name || ''
            : category?.name_en || category?.name || '';
    }, [i18n.language]);

    const getTranslatedProductName = useCallback((product: Product): string => {
        return i18n.language === 'uk'
            ? product.name_uk || product.name
            : product.name_en || product.name;
    }, [i18n.language]);


    console.log(tempCollections);
    

    return (
        <section className={clsx(styles.section, {
            [styles.blur]: isFetching
        })}>
            <PageContainer>
                <div className={styles.control}>
                    {open ? <span /> : <TextButton title={open ? t('filters.hide') : t('filters.show')} onClick={handleOpenMenu} />}
                    <TextButton title={t('sort.title')} onClick={handleClickSort} />
                    {openSort && (
                        <SortMenu
                            className={styles.sortMenu}
                            menuList={sortList}
                            onClickOutside={handleClickOutsideSort}
                            onClickMenu={(item) => changeOrdering(item.name)}
                        />
                    )}
                </div>
                <div className={styles.tagContainer}>
                    {tagList.map((tag, i) => {
                        const { value } = tag;
                        return (
                            <Tag
                                key={i + value}
                                title={value}
                                onClickClose={() => deleteTag(tag)}
                            />
                        );
                    })}
                    {!!tagList.length && (
                        <button className={styles.clearButton} onClick={clearAllFilters}>
                            {t('filters.clear')}
                        </button>
                    )}
                </div>
                <PreviewItemsContainer
                    isLoading={isFetching}
                    itemsQtyWhenLoading={filteredProducts.length}
                    isError={isError}
                    textWhenError={t('products.error')}
                    textWhenEmpty={t('products.empty')}
                >
                    {filteredProducts.map((product) => {
                        const { id, discount, currency, price, photo_url, photo_thumbnail_url } = product;
                        return (
                            <PreviewCard
                                key={id}
                                subTitle={`${getTranslatedCollectionName(product.collection)}${product.collection?.category ? ' / ' : ''}${getTranslatedCategoryName(product.collection?.category)}`}
                                photoSrc={photo_url}
                                previewSrc={photo_thumbnail_url}
                                title={getTranslatedProductName(product)}
                                discount={discount}
                                currency={currency}
                                price={price}
                                onClick={() => navigate(`${ROUTE.PRODUCT}${id}`)}
                            />
                        );
                    })}
                </PreviewItemsContainer>
                {totalPages > 1 && (
                    <Pagination
                        className={styles.pagination}
                        totalPages={totalPages}
                        currentPage={currentPage}
                        onChange={handleChangePage}
                    />
                )}
            </PageContainer>
            <AnimatePresence>
                {open && (
                    <FilterMenu
                        showCollections={!initialCollection}
                        minValue={filter.price_min || 0}
                        maxValue={filter.price_max || 0}
                        priceValue={[filter.price_min || 0, filter.price_max || 0]} // Ensure defaults
                        activeCategories={tempCategories}
                        activeCollections={tempCollections}
                        changePrice={(price: [number, number]) => {
                            const priceRange: PriceRange = { min: price[0], max: price[1] };
                            changePrice(priceRange); // Call changePrice with PriceRange
                        }}
                        onClickHideFilters={handleCloseMenu}
                        onClickCategory={changeCategory}
                        onClickCollection={changeCollection}
                        onApply={handleApply} // Ensure this prop is passed
                    />
                )}
            </AnimatePresence>
        </section>
    );
};
