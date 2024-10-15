import { PageContainer } from "../../components/containers/PageContainer";
import styles from './FilterSection.module.scss';
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
import { useToggler } from "../../hooks/useToggler";
import { useEffect, useState, useCallback } from "react";
import { useNavigate } from "react-router-dom";
import { ROUTE } from "../../constants";
import { FilterControlBar } from "./FilterControlBar/FilterControlBar";

interface FilterSectionProps {
    initialCollection?: Collection;
}

export const FilterSection = ({
    initialCollection
}: FilterSectionProps) => {
    const LIMIT = 8;
    const navigate = useNavigate();
    const [currentPage, setCurrentPage] = useState<number>(1);
    const { t, i18n } = useTranslation();
    const [topPosition, setTopPosition] = useState<number>(0)

    const {
        openStatus: open,
        handleOpen: handleOpenMenu,
        handleClose: handleCloseMenu
    } = useToggler();


    const {
        tagList,
        tempCategories,
        tempPriceValues,
        tempCollections,
        filter,
        fullRangeOfPrice,
        tempHasDiscount,
        deleteTag,
        applyChanges,
        changeCategory,
        changeCollection,
        changePrice,
        clearAllFilters,
        changeOrdering,
        changeDiscount,
        setFullRangeOfPrice,
    } = useFilters(initialCollection);

    const {
        data: productsResponse,
        isSuccess: isSuccessGettingProducts,
        isLoading: isLoadingProducts,
        isFetching: isFetchingProducts,
        isError: isErrorWhenFetchingProducts,
    } = useGetProductsByMainFilterQuery({...filter, page: currentPage, page_size: LIMIT});

    let totalPages = 0;

    useEffect(() => {
        if (productsResponse) {
            setFullRangeOfPrice([productsResponse.overall_price_min, productsResponse.overall_price_max])
        }
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

    const handleInitRect = (rect?: DOMRect) => {
        if(rect){
            setTopPosition(rect.top)
        }
    }


    const getTranslatedCategoryName = useCallback((category?: Category): string => {
        if (!category) return '';
        return i18n.language === 'uk'
            ? category?.name_uk || category?.name || ''
            : category?.name_en || category?.name || '';
    }, [i18n.language]);
    
    const getTranslatedCollectionName = useCallback((collection?: Collection): string => {
        if (!collection) return '';
        return i18n.language === 'uk' ? collection.name_uk || collection.name : collection.name_en || collection.name;
    }, [i18n.language]);

    const getTranslatedProductName = (product: Product): string => {
        return i18n.language === 'uk' ? product.name_uk || product.name : product.name_en || product.name;
    };

    
    return (
        <section className={clsx(styles.section, {
            [styles.blur]: isFetchingProducts
        })}>
            <PageContainer>
                <FilterControlBar
                    isOpenFilterMenu = {open}
                    changeOrdering={changeOrdering}
                    onClickOpenFilterMenu={handleOpenMenu}
                    onInitRect={handleInitRect}
                />
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
                            const { id, id_name, discount, currency, price, photo_url, photo_thumbnail_url } = product;

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
                                    onClick={() => navigate(`${ROUTE.PRODUCT}${id_name}`)}
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
                        hasDiscount = {tempHasDiscount}
                        initialTopPosition={topPosition}
                        showCollections={!initialCollection}
                        minValue={fullRangeOfPrice[0]}
                        maxValue={fullRangeOfPrice[1]}
                        priceValue={[tempPriceValues.min, tempPriceValues.max]} // Convert to tuple
                        activeCategories={tempCategories}
                        activeCollections={tempCollections}
                        changePrice={(priceRange: [number, number]) => changePrice({ min: priceRange[0], max: priceRange[1] })} // Convert tuple to object
                        onClickHideFilters={handleCloseMenu}
                        onClickCategory={changeCategory}
                        onClickCollection={changeCollection}
                        onApply={handleApply}
                        onChangeSale={changeDiscount}
                    />
                }
            </AnimatePresence>
        </section>
    );
};
