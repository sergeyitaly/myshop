import React from "react";
import {useNavigate, useParams} from "react-router-dom";
import Slider from "react-slick";
import "slick-carousel/slick/slick.css";
import "slick-carousel/slick/slick-theme.css";
import style from './style.module.scss'
import {mockDataProducts} from "../carouselMock";
import {NamedSection} from "../../NamedSection/NamedSection";
import {PreviewCard} from "../../Cards/PreviewCard/PreviewCard";
import {
    useGetAllCollectionsQuery,
    useGetAllProductsFromCollectionQuery,
    useGetOneCollectionByIdQuery
} from "../../../api/collectionSlice";
import {Collection} from "../../../models/entities";
import {ROUTE} from "../../../constants";
import {PreviewItemsContainer} from "../../containers/PreviewItemsContainer/PreviewItemsContainer";
import {skipToken} from "@reduxjs/toolkit/query";
import {formatNumber} from "../../../functions/formatNumber";
import {formatCurrency} from "../../../functions/formatCurrency";

function CarouselCeramic () {

    const { id } = useParams<{ id: string }>();
    const collectionId = 3;
    const navigate = useNavigate()

    const {
        data:collection,
        isSuccess,
        isLoading: isLoadingCollection
    } = useGetOneCollectionByIdQuery( collectionId )

    const {
        data: productResponce,
        isSuccess: isSuccessProductFetshing,
        isLoading: isLoadingProducts,
        isError: isErrorProducts,
        error
    } = useGetAllProductsFromCollectionQuery( collectionId )

    console.log(error);


    const products = isSuccessProductFetshing ? productResponce.results : []

    const handleClickProduct = (productId: number) => {
        navigate(`${ROUTE.PRODUCT}${productId}`)
    }

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
        <>
            <NamedSection title="Кераміка" >
                <PreviewItemsContainer
                    isLoading={isLoadingProducts}
                    isError={isErrorProducts}
                    textWhenEmpty="No products available"
                    textWhenError="Error loading products"
                >
                    <Slider {...settings}>
                        {products.map((product) => (
                            <div key={product.id} className={style.container}>
                                <PreviewCard
                                    key={product.id}
                                    photoSrc={product.photo || ''}
                                    title={product.name}
                                    subTitle={`${formatNumber(product.price)} ${formatCurrency(product.currency)}`}
                                    onClick={() => handleClickProduct(product.id)}
                                />
                            </div>
                        ))}
                    </Slider>
                </PreviewItemsContainer>
            </NamedSection>
        </>

    );
}


export default CarouselCeramic ;
