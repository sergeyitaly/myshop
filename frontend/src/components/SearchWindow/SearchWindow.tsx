import { ChangeEvent, useState, useEffect } from 'react';
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

// Normalize text to improve search functionality
const normalizeText = (text: string): string => {
    return text.toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '');
};

// Filter products by query, using normalized text for comparison
const filterProductsByQuery = (products: Product[], query: string) => {
    const normalizedQuery = normalizeText(query);
    return products.filter(product => {
        const nameEnMatch = product.name_en && normalizeText(product.name_en).includes(normalizedQuery);
        const nameUkMatch = product.name_uk && normalizeText(product.name_uk).includes(normalizedQuery);
        return nameEnMatch || nameUkMatch;
    });
};

// Get the most relevant product name or a fallback
const getTranslatedProductName = (product: Product): string => {
    return product.name_en || product.name_uk || product.name;
};

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
    const { t } = useTranslation();
    const [filteredProducts, setFilteredProducts] = useState<Product[]>([]);

    // Encode the queryText for the API request
    const encodedQueryText = encodeURIComponent(queryText);

    // Use the hook and destructure correctly
    const {
        data: products,
        isSuccess,
        isLoading,
        isFetching
    } = useGetManyProductsByFilterQuery(encodedQueryText ? { search: encodedQueryText } : skipToken);

    useEffect(() => {
        if (products && isSuccess) {
            console.log('Products:', products.results); // Debug log
            const results = filterProductsByQuery(products.results, queryText);
            console.log('Filtered Results:', results); // Debug log
            setFilteredProducts(results);
        }
    }, [products, queryText, isSuccess]);

    const handleClickClose = () => {
        onClickClose && onClickClose();
    };

    const handleClickProduct = (product: Product) => {
        onClickProduct && onClickProduct(product);
    };

    return (
        <MotionSearch className={styles.container}>
            <SearchInput
                id='search'
                value={value}
                onChange={(e) => {
                    onChange(e);
                }}
                onClickClose={handleClickClose}
                onSearch={() => {}}
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
                    filteredProducts.length > 0 &&
                    <div className={styles.resultContainer}>
                        {
                            filteredProducts.map((product, i) => (
                                <MotionItem
                                    key={product.id}
                                    index={i}
                                    offset={50}
                                >
                                    <ResultCard
                                        key={product.id}
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
                isSuccess && filteredProducts.length === 0 &&
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
