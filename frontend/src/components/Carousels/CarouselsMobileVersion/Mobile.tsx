import { useCallback } from 'react';
import Slider from "react-slick";
import "slick-carousel/slick/slick.css";
import "slick-carousel/slick/slick-theme.css";
import style from './style.module.scss'
import { PreviewCard } from "../../Cards/PreviewCard/PreviewCard";
import { useNavigate } from "react-router-dom";
import { useGetAllCollectionsQuery, useGetDiscountProductsQuery, useGetProductsByPopularityQuery } from "../../../api/collectionSlice";
import { Collection, Product } from "../../../models/entities";
import { ROUTE } from "../../../constants";
import { PreviewLoadingCard } from "../../Cards/PreviewCard/PreviewLoagingCard";
import { useTranslation } from 'react-i18next';

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

export function Popular() {
    const { t, i18n } = useTranslation();
    const navigate = useNavigate();

    const {
        data: productResponse,
        isSuccess: isSuccessProductFetching,
        isLoading: isLoadingProducts,
        error
    } = useGetProductsByPopularityQuery({ popularity: '6' });

    console.log(error);

    const products = isSuccessProductFetching ? productResponse.results : [];

    const getTranslatedProductName = (product: Product): string => {
        return i18n.language === 'uk' ? product.name_uk || product.name : product.name_en || product.name;
    };

    const handleClickProduct = (productId: number) => {
        navigate(`${ROUTE.PRODUCT}${productId}`);
    };

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
            <Slider {...settings}>
                {isLoadingProducts
                    ? Array.from({ length: 3 }).map((_, index) => (
                        <div key={index} className={style.container}>
                            <PreviewLoadingCard />
                        </div>
                    ))
                    : products.map((product) => (
                        <div key={product.id} className={style.container}>
                            <PreviewCard
                                key={product.id}
                                photoSrc={product.photo || ''}
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
        </div>
    );
}

export function Discount() {
    const { t, i18n } = useTranslation();
    const navigate = useNavigate();

    const { data: discountProductsData, isLoading: isLoadingDiscountProducts } = useGetDiscountProductsQuery();
    const discountProducts = discountProductsData?.results.filter(product => parseFloat(product.discount) > 0) || [];

    console.log('Discount products:', discountProducts);

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
            {discountProducts.length === 1 ? (
                <div></div>
            ) : (
                <Slider {...settings}>
                    {isLoadingDiscountProducts
                        ? Array.from({ length: 3 }).map((_, index) => (
                            <div key={index} className={style.container}>
                                <PreviewLoadingCard />
                            </div>
                        ))
                        : discountProducts.map((product) => (
                            <div key={product.id} className={style.container}>
                                <PreviewCard
                                    className={style.card}
                                    key={product.id}
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
