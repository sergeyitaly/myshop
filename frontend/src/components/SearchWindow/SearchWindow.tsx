import { ChangeEvent } from 'react';
import { useGetManyProductsByFilterQuery } from '../../api/productSlice';
import { ResultCard } from './ResultCard/ResultCard';
import { SearchInput } from './SearchInput/SearchInput';
import { skipToken } from '@reduxjs/toolkit/query';
import { ResultCardSkeleton } from './ResultCard/ResultCardSkeleton';
import { MapComponent } from '../MapComponent';
import { Product } from '../../models/entities';
import styles from './SearchWindow.module.scss';
import { MotionItem } from '../MotionComponents/MotionItem';
import { MotionSearch } from '../MotionComponents/MotionSearch';
import { useTranslation } from 'react-i18next';
import { useCallback } from 'react';
import { useDebounce } from '../../hooks/useDebounce';


interface SearchWindowProps {
    value: string;
    queryText: string;
    onChange: (e: ChangeEvent<HTMLInputElement>) => void;
    onClickClose?: () => void;
    onClickProduct?: (product: Product) => void;
}

export const SearchWindow = ({
    value,
    queryText,
    onChange,
    onClickClose,
    onClickProduct
}: SearchWindowProps) => {
    const { t, i18n } = useTranslation();
    const debouncedQuery = useDebounce(queryText, 20);

    const {
        data: products,
        isSuccess,
        isLoading,
        isFetching
    } = useGetManyProductsByFilterQuery(debouncedQuery ? { search: debouncedQuery } : skipToken);

    const handleClickClose = () => {
        onClickClose && onClickClose();
    };

    const handleClickProduct = (product: Product) => {
        onClickProduct && onClickProduct(product);
    };

    const handleSearch = (query: string) => {
        // Handle the search query here if needed
        console.log('Search query:', query);
    };
        
      const getTranslatedProductName = useCallback((product: Product | undefined): string => {
        return i18n.language === 'uk'
          ? product?.name_uk || product?.name || ''
          : product?.name_en || product?.name || '';
      }, [i18n.language]);

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
                products && products.results.length > 0 &&
                <div className={styles.resultContainer}>
                    {
                        products.results.map((product, i) => (
                            <MotionItem
//                                key={product.id}
                                key={`${product.id}_${i}`}  // Ensure uniqueness

                                index={i}
                                offset={50}
                            >
                                <ResultCard
                                    src={product.photo}
                                    title={getTranslatedProductName(product)}
                                    loading={isFetching}
                                    onClick={() => handleClickProduct(product)}
                                />
                            </MotionItem>
                        ))
                    }
                </div>
            }
            {
                isSuccess && products && products.results.length === 0 &&
                <>
                {isFetching ? (
                    <p className={styles.noResults}>{t('searching')}</p>
                ) : (
                    <p className={styles.noResults}>{t('No results')}</p>
                )}
                </>
            }
        </MotionSearch>
    );
};
