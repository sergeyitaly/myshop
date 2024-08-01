import React, { useState } from "react";
import Slider from "react-slick";
import "slick-carousel/slick/slick.css";
import "slick-carousel/slick/slick-theme.css";
import style from './style.module.scss'
import {mockDataAllCollection, mockDataDiscount, mockDataPopular} from "../carouselMock";
import {useNavigate, useParams} from "react-router-dom";
import {
    useGetAllCollectionsQuery,
    useGetAllProductsFromCollectionQuery, useGetDiscountProductsQuery,
    useGetOneCollectionByIdQuery, useGetProductsByPopularityQuery
} from "../../../api/collectionSlice";
import {Collection} from "../../../models/entities";
import {ROUTE} from "../../../constants";
import {PreviewCard} from "../../Cards/PreviewCard/PreviewCard";
import {formatNumber} from "../../../functions/formatNumber";
import {formatCurrency} from "../../../functions/formatCurrency";

function CarouselFilters() {

    const [selectedFilter, setSelectedFilter] = useState("popular");

    const handleFilterChange = (filter: string) => {
        setSelectedFilter(filter);
    };
    ``

    const settings = {
        dots: true,
        infinite: true,
        speed: 500,
        slidesToShow: 4,
        slidesToScroll: 4,
        initialSlide: 0,
        arrows: false,

    };

    const navigate = useNavigate();

    const { data: collectionsData, isLoading: isLoadingCollections } = useGetAllCollectionsQuery();
    const { data: popularProductsData, isLoading: isLoadingPopularProducts } = useGetProductsByPopularityQuery({ popularity: '6' });
    const { data: discountProductsData, isLoading: isLoadingDiscountProducts } = useGetDiscountProductsQuery();

    const collections = collectionsData?.results || [];
    const popularProducts = popularProductsData?.results || [];
    const discountProducts = discountProductsData?.results || [];

    console.log(discountProducts)

    let displayedData;
    switch (selectedFilter) {
        case "popular":
            displayedData = popularProducts;
            break;
        case "allCollection":
            displayedData = collections;
            break;
        case "discount":
            displayedData = discountProducts;
            break;
        default:
            displayedData = popularProducts;
    }

    const handleClickItem = (id: number) => {
        const route = selectedFilter === 'allCollection' ? ROUTE.COLLECTION + id : ROUTE.PRODUCT + id;
        navigate(route);
    };


    return (
        <div className={style.sliderContainer} >
            <div className={style.filters}>
                <p className={selectedFilter === 'popular' ? style.selected : ''} style={{cursor:'pointer'}} onClick={() => handleFilterChange("popular")}>Найпопулярніші товари</p>
                <p className={selectedFilter === 'allCollection' ? style.selected : ''} style={{cursor:'pointer'}} onClick={() => handleFilterChange("allCollection")}>Всі колекції</p>
                <p className={selectedFilter === 'discount' ? style.selected : ''} style={{cursor:'pointer'}} onClick={() => handleFilterChange("discount")}>Знижки</p>
            </div>
            <Slider {...settings}>
                {displayedData.map((item) => (
                    <div key={item.id} className={style.card}>
                        <PreviewCard
                            key={item.id}
                            photoSrc={item.photo || ''}
                            title={item.name}
                            subTitle={
                                item.discountPercent
                                    ? <>
                                        <span className={style.oldPrice}>{formatNumber(item.price)} {formatCurrency(item.currency)}</span>
                                        <span className={style.newPrice}>{formatNumber(item.price * (1 - item.discountPercent / 100))} {formatCurrency(item.currency)}</span>
                                    </>
                                    : `${formatNumber(item.price)} ${formatCurrency(item.currency)}`
                            }
                            onClick={() => handleClickItem(item.id)}
                        />
                    </div>
                ))}
            </Slider>
        </div>
    );
}

export default CarouselFilters;

