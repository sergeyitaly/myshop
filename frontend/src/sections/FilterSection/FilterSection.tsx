import { useState } from "react"
import { PageContainer } from "../../components/containers/PageContainer"
import styles from './FilterSection.module.scss'
import { TextButton } from "../../components/UI/TextButton/TextButton"
import { useGetProductsByMainFilterQuery } from "../../api/productSlice"
import { PreviewCard } from "../../components/Cards/PreviewCard/PreviewCard"
import { PreviewItemsContainer } from "../../components/containers/PreviewItemsContainer/PreviewItemsContainer"
import { FilterMenu } from "./FilterMenu/FilterMenu"
import { AnimatePresence } from "framer-motion"
import { useFilters } from "../../hooks/useFilters"
import { Tag } from "./Tag/Tag"
import { Pagination } from "../../components/UI/Pagination/Pagination"


export const FilterSection = () => {

    const LIMIT = 8

    const [open, setOpen] = useState<boolean>(false)
    const [currentPage, setCurrentPage] = useState<number>(1)

    const {tagList, tempCategories, tempPriceValues, filter, minValue, maxValue, deleteTag, applyChanges, changeCategory, changePrice, clearAllFilters} = useFilters()

    console.log(tagList);
    
    const {
        data: productsResponce,
        isSuccess: isSuccessGettingProducts,
        isLoading: isLoadingProducts,
        isFetching: isFetchigProducts,
        isError: isErrorWhenFetchingProducts
    } = useGetProductsByMainFilterQuery(filter)

    
    let totalPages = 0

  if(productsResponce){
    totalPages = Math.ceil(productsResponce.count / LIMIT)
  }


    const handleOpenMenu = () => {
        setOpen(true)
    }
    const handleCloseMenu = () => {
        setOpen(false)
    }

    const handleChangePage = (page: number ) => {
        setCurrentPage(page)
      }
    

    
    return (
        <section className={styles.section}>
            {
                isLoadingProducts && <p>Loading...</p>
            }
            {isFetchigProducts && <p>Fetching...</p>}
            <PageContainer>
                <div className={styles.control}>
                    {
                        open ?
                        <span/>
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
                        tagList.map((tag) => {

                        const {id, value} = tag

                            return (
                                <Tag
                                    key={id}
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

                            const {id, collection, discount, currency, price, photo_url, photo_thumbnail_url, name} = product

                            return (
                                <PreviewCard
                                    key={id}
                                    subTitle={collection}
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
                        minValue={minValue}
                        maxValue={maxValue}
                        priceValue={tempPriceValues}
                        activeCategories={tempCategories}
                        changePrice={changePrice}
                        onClickHideFilters={handleCloseMenu}
                        onClickCategory={changeCategory}
                        onApply={applyChanges}
                    />
                }
            </AnimatePresence>
        </section>
    )
}