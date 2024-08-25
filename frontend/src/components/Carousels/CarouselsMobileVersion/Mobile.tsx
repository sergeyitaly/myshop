import { useCallback } from 'react';
import Slider from "react-slick";
import "slick-carousel/slick/slick.css";
import "slick-carousel/slick/slick-theme.css";
import style from './style.module.scss'
import { PreviewCard } from "../../Cards/PreviewCard/PreviewCard";
import { useNavigate } from "react-router-dom";
import { useGetAllCollectionsQuery } from "../../../api/collectionSlice";
import { useGetManyProductsByFilterQuery } from '../../../api/productSlice'; // Adjust the import path if needed
import { Collection, Product } from "../../../models/entities";
import { ROUTE } from "../../../constants";
import { PreviewLoadingCard } from "../../Cards/PreviewCard/PreviewLoagingCard";
import { useTranslation } from 'react-i18next';
import { useGetFilterDataQuery } from '../../../api/filterApiSlice';
import { useEffect, useState } from 'react';

export function AllCollection() {
    const { t, i18n } = useTranslation();
    const navigate = useNavigate();

    const { data, isLoading } = useGetAllCollectionsQuery();
    const collections: Collection[] = data?.results || [];

    const getTranslatedCollectionName = useCallback((collection?: Collection): string => {
        if (!collection) return '';
        return i18n.language === 'uk' ? collection.name_uk || collection.name : collection.name_en || collection.name;
    }, [i18n.language]);

    const handleClickCollectionCard = (id: number) => {
        navigate(ROUTE.COLLECTION + id);
    };

    const settings = {
        dots: true,
        infinite: true,
        speed: 500,
        slidesToShow: 1,
        slidesToScroll: 1,
        initialSlide: 0,
        arrows: false,
    };

    return (
        <div className={style.sliderContainer}>
            <p className={style.title}>{t('allCollections')}</p>
            <Slider {...settings}>
                {isLoading
                    ? Array.from({ length: 3 }).map((_, index) => (
                        <div key={index} className={style.container}>
                            <PreviewLoadingCard />
                        </div>
                    ))
                    : collections.map((collection) => (
                        <div key={collection.id} className={style.container}>
                            <PreviewCard
                                className={style.card}
                                photoSrc={collection.photo || ''}
                                title={getTranslatedCollectionName(collection)}
                                previewSrc={collection.photo_thumbnail_url}
                                onClick={() => handleClickCollectionCard(collection.id)}
                            />
                        </div>
                    ))}
            </Slider>
        </div>
    );
}

const popularityFilter = {
    popularity: '3', // Adjust this to the correct format as required by your API
};

export function Popular() {
    const { t, i18n } = useTranslation();
    const navigate = useNavigate();

    // Fetch products with the filter applied
    const {
        data: productResponse,
        isSuccess: isSuccessProductFetching,
        isLoading: isLoadingProducts,
        error
    } = useGetManyProductsByFilterQuery(popularityFilter);

    // State to hold products
    const [filteredProducts, setFilteredProducts] = useState<Product[]>([]);

    // Log error if exists
    useEffect(() => {
        if (error) {
            console.error('Error fetching products:', error);
        }
    }, [error]);

    useEffect(() => {
        if (isSuccessProductFetching && productResponse?.results) {
            // Assume productResponse.results contains the products
            setFilteredProducts(productResponse.results);
        }
    }, [isSuccessProductFetching, productResponse]);

    // Function to get translated product name based on language
    const getTranslatedProductName = useCallback((product: Product): string => {
        return i18n.language === 'uk' ? product.name_uk || product.name : product.name_en || product.name;
    }, [i18n.language]);

    // Handle product click event
    const handleClickProduct = (productId: number) => {
        navigate(`/product/${productId}`); // Update route if needed
    };

    // Slider settings
    const settings = {
        infinite: true,
        slidesToShow: 2,
        rows: 2,
        speed: 500,
        dots: true,
        arrows: false
    };

    return (
        <div className={style.sliderContainer}>
            <p className={style.title}>{t('popularProducts')}</p>
            {isLoadingProducts
                ? Array.from({ length: 3 }).map((_, index) => (
                    <div key={index} className={style.container}>
                        <PreviewLoadingCard />
                    </div>
                ))
                : filteredProducts.length === 0
                    ? <div>{t('no_popular_products')}</div>
                    : (
                        <Slider {...settings}>
                            {filteredProducts.map((product) => (
                                <div key={product.id} className={style.container}>
                                    <PreviewCard
                                        photoSrc={product.photo}
                                        title={getTranslatedProductName(product)}
                                        discount={product.discount}
                                        price={product.price}
                                        currency={product.currency}
                                        previewSrc={product.photo_thumbnail_url}
                                        onClick={() => handleClickProduct(product.id)}
                                    />
                                </div>
                            ))}
                        </Slider>
                    )
            }
        </div>
    );
}

interface DiscountFilter {
    has_discount: boolean;
}

export function Discount() {
    const { t, i18n } = useTranslation();
    const navigate = useNavigate();
    const [filterStatus, setFilterStatus] = useState<'loading' | 'failed' | 'success'>('loading');
    const [filterError, setFilterError] = useState<string | null>(null);

    // Use the filter query to fetch discount products
    const { data, error, isLoading } = useGetFilterDataQuery({ has_discount: true } as DiscountFilter);

    useEffect(() => {
        if (isLoading) {
            setFilterStatus('loading');
        } else if (error) {
            setFilterStatus('failed');
            setFilterError('An error occurred while fetching discount products.');
            console.error('Fetch error:', error);
        } else {
            setFilterStatus('success');
        }
    }, [isLoading, error]);
    const discountProducts: Product[] = data?.results || []; // Default to an empty array if undefined
    const getTranslatedProductName = (product: Product): string => {
        return i18n.language === 'uk' ? product.name_uk || product.name : product.name_en || product.name;
    };

    const settings = {
        dots: true,
        infinite: true,
        speed: 500,
        slidesToShow: 1,
        slidesToScroll: 1,
        initialSlide: 0,
        centerMode: true,
        centerPadding: "25%",
        arrows: false,
    };

    const handleClickProduct = (productId: number) => {
        navigate(`${ROUTE.PRODUCT}${productId}`);
    };

    return (
        <div className={style.sliderContainer}>
            <p className={style.title}>{t('discounts')}</p>
            {filterStatus === 'loading' ? (
                Array.from({ length: 3 }).map((_, index) => (
                    <div key={index} className={style.container}>
                        <PreviewLoadingCard />
                    </div>
                ))
            ) : filterStatus === 'failed' ? (
                <div>{filterError}</div>
            ) : discountProducts.length === 0 ? (
                <div>{t('no_discount_products')}</div>
            ) : (
                <Slider {...settings}>
                    {discountProducts.map((product) => (
                        <div key={product.id} className={style.container}>
                            <PreviewCard
                                className={style.card}
                                title={getTranslatedProductName(product)}
                                discount={product.discount}
                                price={product.price}
                                currency={product.currency}
                                photoSrc={product.photo_url}
                                previewSrc={product.photo_thumbnail_url}
                                onClick={() => handleClickProduct(product.id)}
                            />
                        </div>
                    ))}
                </Slider>
            )}
        </div>
    );
}