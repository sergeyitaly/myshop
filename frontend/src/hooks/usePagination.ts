import { useState, useEffect } from 'react';
import { useGetAllProductsQuery } from '../api/productSlice';
import { Product } from '../models/entities';

interface PaginationParams {
    search?: string;
}

export const usePagination = ({
    search = ''
}: PaginationParams) => {
    const [allProducts, setAllProducts] = useState<Product[]>([]);
    const [isFetching, setIsFetching] = useState<boolean>(false);
    const [hasMorePages, setHasMorePages] = useState<boolean>(true);

    useEffect(() => {
        const fetchAllPages = async () => {
            setIsFetching(true);
            let page = 1;
            let accumulatedProducts: Product[] = [];
            let shouldFetchMore = true;

            while (shouldFetchMore) {
                const { data } = await useGetAllProductsQuery({ page, search });
                if (data) {
                    accumulatedProducts = [...accumulatedProducts, ...data.results];
                    setHasMorePages(data.next !== null);
                    page++;
                    shouldFetchMore = data.next !== null;
                } else {
                    shouldFetchMore = false;
                }
            }

            setAllProducts(accumulatedProducts);
            setIsFetching(false);
        };

        fetchAllPages();
    }, [search]);

    return {
        allProducts,
        isFetching,
        hasMorePages
    };
};
