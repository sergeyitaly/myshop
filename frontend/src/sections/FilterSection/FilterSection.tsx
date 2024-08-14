import { useState } from "react";
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
import { Collection, Product } from '../../models/entities';
import clsx from "clsx";
import { useTranslation } from 'react-i18next';

interface FilterSectionProps {
    initialCollection?: Collection;
}

// Function to get translated product name
const getTranslatedProductName = (product: Product, language: string): string => {
    return language === 'uk' ? product.name_uk || product.name : product.name_en || product.name;
};

// Function to get translated collection name
const getTranslatedCollectionName = (collection: Collection | undefined, language: string): string => {
    if (!collection) return ''; // Handle the case when collection is undefined
    return language === 'uk' ? collection.name_uk || collection.name : collection.name_en || collection.name;
};

export const FilterSection = ({
    initialCollection
}: FilterSectionProps) => {

    const LIMIT = 8;
    const [open, setOpen] = useState<boolean>(false);
    const [currentPage, setCurrentPage] = useState<number>(1);

    const { i18n } = useTranslation();

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
    } = useFilters(initialCollection);

    const {
        data: productsResponse,
        isSuccess: isSuccessGettingProducts,
        isLoading: isLoadingProducts,
        isFetching: isFetchingProducts,
        isError: isErrorWhenFetchingProducts
    } = useGetProductsByMainFilterQuery(filter);

    let totalPages = 0;

    if (productsResponse) {
        totalPages = Math.ceil(productsResponse.count / LIMIT);
    }

    const handleOpenMenu = () => {
        setOpen(true);
    };

    const handleCloseMenu = () => {
        setOpen(false);
    };

    const handleChangePage = (page: number) => {
        setCurrentPage(page);
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
                                title={open ? 'Сховати' : 'Фільтри'}
                                onClick={handleOpenMenu}
                            />
                    }
                    <TextButton
                        title="Сортувати"
                    />
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
                        >Очистити фільтри</button>
                    }
                </div>
                <PreviewItemsContainer
                    isLoading={isLoadingProducts}
                    itemsQtyWhenLoading={LIMIT}
                    isError={isErrorWhenFetchingProducts}
                    textWhenError={'Виникла помилка :('}
                    textWhenEmpty={'Поки що відсутні продукти за таким запитом'}
                >
                    {
                        isSuccessGettingProducts &&
                        productsResponse.results.map((product) => {
                            const { id, collection, discount, currency, price, photo_url, photo_thumbnail_url } = product;

                            return (
                                <PreviewCard
                                    key={id}
                                    subTitle={collection ? getTranslatedCollectionName(collection, i18n.language) : ''}
                                    photoSrc={photo_url}
                                    previewSrc={photo_thumbnail_url}
                                    title={getTranslatedProductName(product, i18n.language)}
                                    discount={discount}
                                    currency={currency}
                                    price={price}
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
                        minValue={minValue}
                        maxValue={maxValue}
                        priceValue={tempPriceValues}
                        activeCategories={tempCategories}
                        activeCollections={tempCollections}
                        changePrice={changePrice}
                        onClickHideFilters={handleCloseMenu}
                        onClickCategory={changeCategory}
                        onClickCollection={changeCollection}
                        onApply={applyChanges}
                    />
                }
            </AnimatePresence>
        </section>
    );
};
