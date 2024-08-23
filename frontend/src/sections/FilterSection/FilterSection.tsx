import { PageContainer } from "../../components/containers/PageContainer";
import styles from './FilterSection.module.scss';
import { TextButton } from "../../components/UI/TextButton/TextButton";
import { useGetProductsByMainFilterQuery } from "../../api/productSlice";
import { PreviewCard } from "../../components/Cards/PreviewCard/PreviewCard";
import { PreviewItemsContainer } from "../../components/containers/PreviewItemsContainer/PreviewItemsContainer";
import { FilterMenu } from "./FilterMenu/FilterMenu";
import { AnimatePresence } from "framer-motion";
import { useFilters } from "../../hooks/useFilters";
import { Tag } from "./Tag/Tag";
import { Pagination } from "../../components/UI/Pagination/Pagination";
import { Collection, Product, Category } from '../../models/entities';
import clsx from "clsx";
import { useTranslation } from 'react-i18next';
import { SortMenu } from "./SortMenu/SortMenu";
import { useToggler } from "../../hooks/useToggler";
import { useEffect, useState, useCallback } from "react";
import { useNavigate } from "react-router-dom";
import { ROUTE } from "../../constants";
import { useSortList } from "./SortList";

interface FilterSectionProps {
    initialCollection?: Collection;
}

export const FilterSection = ({
    initialCollection
}: FilterSectionProps) => {
    const LIMIT = 100;

    const navigate = useNavigate();
    const [currentPage, setCurrentPage] = useState<number>(1);
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

    const {
        tagList,
        tempCategories,
        tempPriceValues,
        tempCollections,
        filter,
        minValue,
        maxValue,
        deleteTag,
        applyChanges,
        changeCategory,
        changeCollection,
        changePrice,
        clearAllFilters,
        changeOrdering,
    } = useFilters(initialCollection);

    const {
        data: productsResponse,
        isSuccess: isSuccessGettingProducts,
        isLoading: isLoadingProducts,
        isFetching: isFetchingProducts,
        isError: isErrorWhenFetchingProducts
    } = useGetProductsByMainFilterQuery({...filter, page: currentPage, page_size: LIMIT});

    let totalPages = 0;
    
    useEffect(() => {
        productsResponse &&
        changePrice([productsResponse.price_min, productsResponse.price_max]);
    }, [productsResponse]);
    
    if (productsResponse) {
        totalPages = Math.ceil(productsResponse.count / LIMIT);
    }

    const handleChangePage = (page: number) => {
        setCurrentPage(page);
    };

    const handleApply = () => {
        applyChanges();
        handleCloseMenu();
    };

    const sortList = useSortList();

    // Function to get translated collection name
    const getTranslatedCollectionName = useCallback((collection?: Collection): string => {
        if (!collection) return '';
        return i18n.language === 'uk' ? collection.name_uk || collection.name : collection.name_en || collection.name;
    }, [i18n.language]);

    // Function to get translated category name
    const getTranslatedCategoryName = useCallback((category?: Category): string => {
        if (!category) return '';
        return i18n.language === 'uk'
            ? category?.name_uk || category?.name || ''
            : category?.name_en || category?.name || '';
    }, [i18n.language]);

    // Function to get translated product name
    const getTranslatedProductName = (product: Product): string => {
        return i18n.language === 'uk' ? product.name_uk || product.name : product.name_en || product.name;
    };

    return (
        <section className={clsx(styles.section, {
            [styles.blur]: isFetchingProducts
        })}>
            <PageContainer>
                <div className={styles.control}>
                    {
                        open ?
                            <span />
                            :
                            <TextButton
                                title={open ? t('filters.hide') : t('filters.show')}
                                onClick={handleOpenMenu}
                            />
                    }
                    <TextButton
                        title={t('sort.title')}
                        onClick={handleClickSort}
                    />
                    {
                        openSort &&
                        <SortMenu
                            className={styles.sortMenu}
                            menuList={sortList}
                            onClickOutside={handleClickOutsideSort}
                            onClickMenu={(item) => changeOrdering(item.name)}
                        />
                    }
                </div>
                <div className={styles.tagContainer}>
                    {
                        tagList.map((tag, i) => {
                            const { value } = tag;

                            return (
                                <Tag
                                    key={i + value}
                                    title={value}
                                    onClickClose={() => deleteTag(tag)}
                                />
                            );
                        })
                    }
                    {
                        !!tagList.length &&
                        <button
                            className={styles.clearButton}
                            onClick={clearAllFilters}
                        >
                            {t('filters.clear')}
                        </button>
                    }
                </div>
                <PreviewItemsContainer
                    isLoading={isLoadingProducts}
                    itemsQtyWhenLoading={LIMIT}
                    isError={isErrorWhenFetchingProducts}
                    textWhenError={t('products.error')}
                    textWhenEmpty={t('products.empty')}
                >
                    {
                        isSuccessGettingProducts &&
                        productsResponse.results.map((product) => {
                            const { id, discount, currency, price, photo_url, photo_thumbnail_url } = product;

                            return (
                                <PreviewCard
                                    key={id}
                                    subTitle={`${getTranslatedCollectionName(product.collection)}${
                                        product.collection?.category ? ' / ' : ''
                                    }${getTranslatedCategoryName(product.collection?.category)}`}
                                    photoSrc={photo_url}
                                    previewSrc={photo_thumbnail_url}
                                    title={getTranslatedProductName(product)}
                                    discount={discount}
                                    currency={currency}
                                    price={price}
                                    onClick={() => navigate(`${ROUTE.PRODUCT}${id}`)}
                                />

                            );
                        })
                    }
                </PreviewItemsContainer>
                {
                    productsResponse && totalPages > 1 &&
                    <Pagination
                        className={styles.pagination}
                        totalPages={totalPages}
                        currentPage={currentPage}
                        onChange={handleChangePage}
                    />
                }
            </PageContainer>
            <AnimatePresence>
                {
                    open &&
                    <FilterMenu
                        showCollections={!initialCollection}
                        minValue={productsResponse?.price_min || minValue}
                        maxValue={productsResponse?.price_max || maxValue}
                        priceValue={tempPriceValues}
                        activeCategories={tempCategories}
                        activeCollections={tempCollections}
                        changePrice={changePrice}
                        onClickHideFilters={handleCloseMenu}
                        onClickCategory={changeCategory}
                        onClickCollection={changeCollection}
                        onApply={handleApply}
                    />
                }
            </AnimatePresence>
        </section>
    );
};
