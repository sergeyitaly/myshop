import { useState, useEffect } from 'react';
import { useGetAllProductsQuery } from '../api/productSlice';
import { Product } from '../models/entities';
import { useGetProductsByMainFilterQuery} from '../api/productSlice';
import { MainFilter } from '../models/filters'; // Import MainFilter from filters.ts

interface PaginationParams {
    search?: string;
    pageSize?: number; // Ensure pageSize is included here
}

export const usePagination = ({
    search = '',
    pageSize
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
                const { data } = await useGetAllProductsQuery({ page, search});
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
    }, [search, pageSize]);

    return {
        allProducts,
        isFetching,
        hasMorePages
    };
};
interface PaginationFilterParams {
    filter: MainFilter;
}

export const usePaginationFilter = ({ filter }: PaginationFilterParams) => {
    const [filteredProducts, setFilteredProducts] = useState<Product[]>([]);
    const [isFetching, setIsFetching] = useState<boolean>(false);
    const [hasMorePages, setHasMorePages] = useState<boolean>(true);
    const [currentPage, setCurrentPage] = useState<number>(1);

    const { data, isFetching: isLoading, isError } = useGetProductsByMainFilterQuery({
        ...filter,
        page: currentPage
    });

    useEffect(() => {
        if (data) {
            setFilteredProducts(prevProducts => [...prevProducts, ...data.results]);
            setHasMorePages(!!data.next);
            setIsFetching(false);
        }
    }, [data]);

    useEffect(() => {
        if (isLoading) {
            setIsFetching(true);
        }
    }, [isLoading]);

    const loadMore = () => {
        if (hasMorePages && !isFetching) {
            setCurrentPage(prevPage => prevPage + 1);
        }
    };

    return {
        filteredProducts,
        isFetching,
        hasMorePages,
        loadMore,
        isError
    };
};