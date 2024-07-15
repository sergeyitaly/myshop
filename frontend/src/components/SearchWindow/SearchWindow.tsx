import { ChangeEvent } from 'react'
import { useGetManyProductsByFilterQuery } from '../../api/productSlice'
import { ResultCard } from './ResultCard/ResultCard'
import { SearchInput } from './SearchInput/SearchInput'
import { skipToken } from '@reduxjs/toolkit/query'
import { ResultCardSkeleton } from './ResultCard/ResultCardSkeleton'
import { MapComponent } from '../MapComponent'
import { Product } from '../../models/entities'
import { motion } from 'framer-motion'
import styles from './SearchWindow.module.scss'

interface SearchWindowProps {
    value: string
    onChange: (e: ChangeEvent<HTMLInputElement>) => void
    onClickClose?: () => void
    onClickProduct?: (product: Product) => void
}

export const SearchWindow = ({
    value,
    onChange,
    onClickClose,
    onClickProduct
}: SearchWindowProps) => {

    const {
        data: products,
        isSuccess,
        isLoading,
        isFetching
    } = useGetManyProductsByFilterQuery(value ? { search: value } : skipToken)

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
        <motion.div 
            initial={{
                x: '-50%',
                top: '-100%',
            }}
            animate={{
                top: '100%'
            }}
            exit={{
                top: '-100%',
            }}
            className={styles.container}
        >
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
                        products.results.map((product) => (
                            <ResultCard
                                key={product.id}
                                src={product.photo_url}
                                title={product.name}
                                loading={isFetching}
                                onClick={() => handleClickProduct(product)}
                            />
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
        </motion.div>
    )
}
