import { ChangeEvent } from 'react'
import { useGetManyProductsByFilterQuery } from '../../api/productSlice'
import { ResultCard } from './ResultCard/ResultCard'
import { SearchInput } from './SearchInput/SearchInput'
import { skipToken } from '@reduxjs/toolkit/query'
import { ResultCardSkeleton } from './ResultCard/ResultCardSkeleton'
import { MapComponent } from '../MapComponent'
import { Product } from '../../models/entities'
import styles from './SearchWindow.module.scss'
import { MotionItem } from '../MotionComponents/MotionItem'
import { MotionSearch } from '../MotionComponents/MotionSearch'

interface SearchWindowProps {
    value: string
    queryText: string
    onChange: (e: ChangeEvent<HTMLInputElement>) => void
    onClickClose?: () => void
    onClickProduct?: (product: Product) => void
}

export const SearchWindow = ({
    value,
    queryText,
    onChange,
    onClickClose,
    onClickProduct
}: SearchWindowProps) => {

    const {
        data: products,
        isSuccess,
        isLoading,
        isFetching
    } = useGetManyProductsByFilterQuery(queryText ? { search: queryText } : skipToken)

    const handleClickClose = () => {
        onClickClose && onClickClose()
    }

    const handleClickProduct = (product: Product) => {
        onClickProduct && onClickProduct(product)
    }

    const handleSearch = (query: string) => {
        // Handle the search query here if needed
        console.log('Search query:', query)
    }

    return (
        <MotionSearch className={styles.container}>
            <SearchInput 
                id='search'
                value={value}
                onChange={onChange}
                onClickClose={handleClickClose}
                onSearch={handleSearch}  // Add the onSearch prop here
            />
            {
                isLoading ? 
                <div className={styles.resultContainer}>
                    <MapComponent
                        component={<ResultCardSkeleton />}
                        qty={4}
                    />
                </div>
                :
                products && !!products.results.length && 
                <div className={styles.resultContainer}>
                    {
                        products.results.map((product, i) => (
                            <MotionItem
                                key={product.id}
                                index={i}
                                offset={50}
                            >
                                <ResultCard
                                    key={product.id}
                                    src={product.photo_url}
                                    title={product.name}
                                    loading={isFetching}
                                    onClick={() => handleClickProduct(product)}
                                />
                            </MotionItem>
                        ))
                    }
                </div>
            }
            {
                isSuccess && !products.results.length && 
                <>
                    {
                        isFetching ?
                        <p className={styles.noResults}>Шукаю...</p>
                        :
                        <p className={styles.noResults}>Пошук не дав результату</p>
                    }
                </>
            }
        </MotionSearch>
    )
}
