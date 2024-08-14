import { PageContainer } from "../../components/containers/PageContainer"
import { TextButton } from "../../components/UI/TextButton/TextButton"
import { useGetProductsByMainFilterQuery } from "../../api/productSlice"
import { PreviewCard } from "../../components/Cards/PreviewCard/PreviewCard"
import { PreviewItemsContainer } from "../../components/containers/PreviewItemsContainer/PreviewItemsContainer"
import { FilterMenu } from "./FilterMenu/FilterMenu"
import { AnimatePresence } from "framer-motion"
import { useFilters } from "../../hooks/useFilters"
import { Tag } from "./Tag/Tag"
import { Pagination } from "../../components/UI/Pagination/Pagination"
import { Collection } from "../../models/entities"
import { SortMenu } from "./SortMenu/SortMenu"
import { sortList } from "./SortList"
import { useToggler } from "../../hooks/useToggler"
import { usePagination } from "../../hooks/usePagination"
import clsx from "clsx"
import styles from './FilterSection.module.scss'

interface FilterSectionProps {
    initialCollection?: Collection
}


export const FilterSection = ({
    initialCollection
}: FilterSectionProps) => {

    const LIMIT = 8

    const {
        openStatus: open,
        handleClose: handleCloseMenu,
        handleToggle: handleToggleMenu,
    } = useToggler()

    const {
        openStatus: openSort,
        handleOpen: handleClickSort,
        handleClose: handleClickOutsideSort
    } = useToggler()


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
        changeOrdering
    } = useFilters(initialCollection)

    const {
        data: productsResponce,
        isSuccess: isSuccessGettingProducts,
        isLoading: isLoadingProducts,
        isFetching: isFetchigProducts,
        isError: isErrorWhenFetchingProducts
    } = useGetProductsByMainFilterQuery(filter)

    console.log(filter);
    
    const {currentPage, totalPages, handleChangePage} = usePagination({
        limit: LIMIT,
        numberOfItems: productsResponce?.count
    })

   
    const handleApply = () => {
        applyChanges()
        handleCloseMenu()
    }

    
    return (
        <section className={clsx(styles.section, {
            [styles.blur]: !isLoadingProducts && isFetchigProducts
        })}>
            <PageContainer>
                <div className={styles.control}>
                    <TextButton
                        title={open ? 'Сховати' : 'Фільтри'}
                        onClick={handleToggleMenu}
                    />
                    <TextButton 
                        title="Сортувати"
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

                        const {value} = tag

                            return (
                                <Tag
                                    key={i + value}
                                    title={value}
                                    onClickClose={() => deleteTag(tag)}
                                />
                            )
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
                    isLoading = {isLoadingProducts}
                    itemsQtyWhenLoading={LIMIT}
                    isError = {isErrorWhenFetchingProducts}
                    textWhenError={'Виникла помилка :('}
                    textWhenEmpty={'Поки що відсутні продукти за таким запитом'}
                >
                    {
                        isSuccessGettingProducts &&
                        productsResponce.results.map((product) => {

                            const {id, discount, currency, price, photo_url, photo_thumbnail_url, name} = product

                            return (
                                <PreviewCard
                                    key={id}
                                    photoSrc={photo_url}
                                    previewSrc={photo_thumbnail_url}
                                    title={name}
                                    discount={discount}
                                    currency={currency}
                                    price={price}
                                />
                            )
                        })
                    }
                </PreviewItemsContainer>
                {
                    productsResponce && totalPages > 1 &&
                    <Pagination
                        className={styles.pagination}
                        totalPages={totalPages}
                        currentPage={currentPage}
                        onChange = {handleChangePage}
                    />
                }
            </PageContainer>
            <AnimatePresence>
                {
                    open &&
                    <FilterMenu
                        showCollections = {!initialCollection}
                        minValue={minValue}
                        maxValue={maxValue}
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
    )
}