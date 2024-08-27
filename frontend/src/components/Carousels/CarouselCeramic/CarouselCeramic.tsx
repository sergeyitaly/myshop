import { useNavigate } from "react-router-dom";
import Slider from "react-slick";
import "slick-carousel/slick/slick.css";
import "slick-carousel/slick/slick-theme.css";
import style from './style.module.scss';
import { NamedSection } from "../../NamedSection/NamedSection";
import { PreviewCard } from "../../Cards/PreviewCard/PreviewCard";
import { useGetAllProductsFromCollectionQuery } from "../../../api/collectionSlice";
import { ROUTE } from "../../../constants";
import { PreviewLoadingCard } from "../../Cards/PreviewCard/PreviewLoagingCard";
import { useTranslation } from 'react-i18next';
import { useCallback } from 'react';
import { Product } from "../../../models/entities"; // Import the Product type

function CarouselCeramic() {
    const collectionId = 3;
    const navigate = useNavigate();
    const { t, i18n } = useTranslation();

    const { data, isLoading } = useGetAllProductsFromCollectionQuery(collectionId);
    const products = data?.results || [];

    // Use the imported Product type
    const getTranslatedProductName = useCallback((product: Product): string => {
        return i18n.language === 'uk' ? product.name_uk || product.name : product.name_en || product.name;
    }, [i18n.language]);

    const handleClickProduct = (productId: number) => {
        navigate(`${ROUTE.PRODUCT}${productId}`);
    };

    const settings = {
        dots: true,
        infinite: true,
        speed: 500,
        slidesToShow: 3,
        slidesToScroll: 3,
        initialSlide: 0,
        arrows: false,
        responsive: [
            {
                breakpoint: 600,
                settings: {
                    slidesToShow: 1,
                    slidesToScroll: 1,
                    initialSlide: 0,
                    centerMode: true,
                    centerPadding: "100px",
                }
            }
        ]
    };

    return (
        <div className={style.sliderContainer}>
            <NamedSection title={t('Ceramics')}>
                <Slider {...settings}>
                    {isLoading
                        ? Array.from({ length: 3 }).map((_, index) => (
                            <div key={index} className={style.container}>
                                <PreviewLoadingCard />
                            </div>
                        ))
                        : products.map((product) => (
                            <div key={product.id} className={style.container}>
                                <PreviewCard
                                    key={product.id}
                                    photoSrc={product.photo_url}
                                    title={getTranslatedProductName(product)}
                                    price={product.price}
                                    currency={product.currency}
                                    previewSrc={product.photo_thumbnail_url}
                                    onClick={() => handleClickProduct(product.id)}
                                />
                            </div>
                        ))}
                </Slider>
            </NamedSection>
        </div>
    );
}

export default CarouselCeramic;
