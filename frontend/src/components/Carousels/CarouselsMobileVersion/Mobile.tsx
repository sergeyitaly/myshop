import Slider from "react-slick";
import "slick-carousel/slick/slick.css";
import "slick-carousel/slick/slick-theme.css";
import style from './style.module.scss'
import {mockDataAllCollection, mockDataDiscount, mockDataProducts} from "../carouselMock";
import {PreviewCard} from "../../Cards/PreviewCard/PreviewCard";
import React from "react";
import {useNavigate, useParams} from "react-router-dom";
import {
    useGetAllCollectionsQuery,
    useGetAllProductsFromCollectionQuery,
    useGetOneCollectionByIdQuery,
    useGetProductsByPopularityQuery,
    useGetProductsFromCollectionByProductFilterQuery
} from "../../../api/collectionSlice";
import {Collection} from "../../../models/entities";
import {ROUTE} from "../../../constants";
import {formatNumber} from "../../../functions/formatNumber";
import {formatCurrency} from "../../../functions/formatCurrency";

export function AllCollection() {

    const navigate = useNavigate()

    const {data, isLoading} = useGetAllCollectionsQuery()

    const collections: Collection[] = data?.results || []

    const handleClickCollectionCard = (id: number) => {
        navigate(ROUTE.COLLECTION + id)
    }

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
            <p className={style.title}>Всі колекції</p>
            <Slider {...settings}>
                {
                    collections.map((collection) => (
                        <div className={style.container}>
                            <PreviewCard
                                key={collection.id}
                                photoSrc={collection.photo}
                                title={collection.name}
                                subTitle={collection.category}
                                onClick={() => handleClickCollectionCard(collection.id)}
                            />
                        </div>
                    ))
                }
            </Slider>
        </div>
    );
}

export function Popular () {

    const navigate = useNavigate();

    const {
        data: productResponce,
        isSuccess: isSuccessProductFetshing,
        isLoading: isLoadingProducts,
        isError: isErrorProducts,
        error
    } = useGetProductsByPopularityQuery({ popularity: '6' });

    console.log(error);

    const products = isSuccessProductFetshing ? productResponce.results : [];

    const handleClickProduct = (productId: number) => {
        navigate(`${ROUTE.PRODUCT}${productId}`)
    }

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
            <p className={style.title}>Найпопулярніші товари</p>
            {isSuccessProductFetshing && (
                <Slider {...settings}>
                    {products.map((product) => (
                        <div className={style.container} key={product.id}>
                            <PreviewCard
                                photoSrc={product.photo || ''}
                                title={product.name}
                                subTitle={`${formatNumber(product.price)} ${formatCurrency(product.currency)}`}
                                onClick={() => handleClickProduct(product.id)}
                            />
                        </div>
                    ))}
                </Slider>
            )}
        </div>
    );
}


export function Discount () {
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
    return (
        <div className={style.sliderContainer} >
            <p className={style.title}> Знижки </p>
            <Slider {...settings}>
                {mockDataDiscount.map((product, index) => (
                    <div key={index} className={style.card}>
                        <div className={style.cardImage}>
                            {/*<img src={product.imageUrl} alt={product.name} style={{maxWidth:'100%'}}/>  */}
                            <div className={style.imageContainer}>
                                <p className={style.saleLabel}>Sale</p>
                                <img src={product.imageUrl} alt={product.name} className={style.image} />
                            </div>
                            <p className={style.name} style={{marginTop:'15px', textAlign:'center'}}>{product.name}</p>
                            <div className={style.priceContainer}>
                                <p className={style.oldPrice}>{product.price}</p>
                                <p className={style.newPrice}>{product.newPrice}</p>
                            </div>

                        </div>
                    </div>
                ))}
            </Slider>
        </div>
    );
}

