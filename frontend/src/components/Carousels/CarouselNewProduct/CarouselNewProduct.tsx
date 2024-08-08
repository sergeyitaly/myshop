import Slider from "react-slick";
import "slick-carousel/slick/slick.css";
import "slick-carousel/slick/slick-theme.css";
import {mockDataCategories} from "../carouselMock";
import {useNavigate} from "react-router-dom";
import {useGetAllCollectionsQuery} from "../../../api/collectionSlice";
import {Collection} from "../../../models/entities";
import {ROUTE} from "../../../constants";
import {PreviewCard} from "../../Cards/PreviewCard/PreviewCard";
import React from "react";
import {NamedSection} from "../../NamedSection/NamedSection";
import {PreviewItemsContainer} from "../../containers/PreviewItemsContainer/PreviewItemsContainer";
import style from "../CarouselNewProduct/style.module.scss";
import {PreviewLoadingCard} from "../../Cards/PreviewCard/PreviewLoagingCard";

function CarouselNewProduct () {
    const navigate = useNavigate()

    const {data, isLoading} = useGetAllCollectionsQuery()

    const collections: Collection[] = data?.results || []

    const handleClickCollectionCard = (id: number) => {
        navigate(ROUTE.COLLECTION + id)
    }

    const shuffleArray = (array: any[]) => {
        return array.sort(() => Math.random() - 0.5);
    };

    const shuffledCollections = shuffleArray([...collections]);

    const totalCards = mockDataCategories.length;
    let dotsValue = true;

    if (totalCards <= 2) {
        dotsValue = false;
    }

    const settings = {
        dots: dotsValue,
        infinite: true,
        speed: 500,
        slidesToShow: 2,
        slidesToScroll: 2,
        initialSlide: 0,
        arrows: false,
        responsive: [
            {
                breakpoint: 600,
                settings: {
                    dots: true,
                    slidesToShow: 1,
                    slidesToScroll: 1,
                    initialSlide: 0,
                }
            }
        ]
    };
    return (
        <div className={style.sliderContainer}>
            <NamedSection title="Нові надходження" >
                <Slider {...settings}>
                    {isLoading
                        ? Array.from({ length: 3 }).map((_, index) => (
                            <div key={index} className={style.card}>
                                <PreviewLoadingCard />
                            </div>
                        ))
                        : shuffledCollections.map((product) => (
                                <PreviewCard
                                    className={style.card}
                                    key={product.id}
                                    photoSrc={product.photo || ''}
                                    title={product.name}
                                    onClick={() => handleClickCollectionCard(product.id)}
                                />
                        ))}
                </Slider>
            </NamedSection>
        </div>

    );
}


export default CarouselNewProduct;
