import { ChangeEvent } from 'react'
import { useGetManyProductsByFilterQuery } from '../../api/productSlice'
import { ResultCard } from './ResultCard/ResultCard'
import { SearchInput } from './SearchInput/SearchInput'
import styles from './SearchWindow.module.scss'
import { skipToken } from '@reduxjs/toolkit/query'
import { ResultCardSkeleton } from './ResultCard/ResultCardSkeleton'
import { MapComponent } from '../MapComponent'

interface SearchWindowProps {
    value: string
    onChange: (e: ChangeEvent<HTMLInputElement>) => void
    onClickClose?: () => void
}

export const SearchWindow = ({
    value,
    onChange,
    onClickClose
}: SearchWindowProps) => {

    const {
        data: products,
        isSuccess,
        isLoading,
        isFetching
    } = useGetManyProductsByFilterQuery(value ? {search: value} : skipToken)
    
    const handleClickClose = () => {
        onClickClose && onClickClose()
    }

    return (
        <div className={styles.container}>
            <SearchInput 
                id='search'
                value={value}
                onChange={onChange}
                onClickClose={handleClickClose}
            />
            {
                isLoading ? 
                <div className={styles.resultContainer}>
                    <MapComponent
                        component={<ResultCardSkeleton/>}
                        qty={4}
                    />
                </div>
                :
                products && !!products.results.length && 
                <div className={styles.resultContainer}>
                    {
                        products.results.map(({name, photo_url}) => (
                            <ResultCard
                                src={photo_url}
                                title={name}
                                loading={isFetching}
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
        </div>
    )
}