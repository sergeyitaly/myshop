import { useState, useCallback } from 'react';
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
import { Product } from "../../../models/entities";

function CarouselCeramic() {
    const collectionId = 3;
    const navigate = useNavigate();
    const { t, i18n } = useTranslation();

    // State to manage pagination
    const [page, setPage] = useState(1);
    const limit = 6;  // Number of items per page

    // Fetch paginated products
    const { data, isLoading } = useGetAllProductsFromCollectionQuery(collectionId);
    const products = data?.results || [];

    const getTranslatedProductName = useCallback((product: Product): string => {
        return i18n.language === 'uk' ? product.name_uk || product.name : product.name_en || product.name;
    }, [i18n.language]);

    const handleClickProduct = (productId: number) => {
        navigate(`${ROUTE.PRODUCT}${productId}`);
    };

    const handleNextPage = () => {
        if (data?.next) {
            setPage(page + 1);
        }
    };

    const handlePreviousPage = () => {
        if (page > 1) {
            setPage(page - 1);
        }
    };

    const settings = {
        dots: true,
        infinite: false,  // Turn off infinite scroll for pagination
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

                {/* Pagination Controls */}
                <div className={style.paginationControls}>
                    <button onClick={handlePreviousPage} disabled={page === 1}>Previous</button>
                    <button onClick={handleNextPage} disabled={!data?.next}>Next</button>
                </div>
            </NamedSection>
        </div>
    );
}

export default CarouselCeramic;
