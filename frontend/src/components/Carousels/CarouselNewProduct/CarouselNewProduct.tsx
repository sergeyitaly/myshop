import Slider from "react-slick";
import "slick-carousel/slick/slick.css";
import "slick-carousel/slick/slick-theme.css";
import style from './style.module.scss'
import {mockDataCategories} from "../carouselMock";
import {useNavigate} from "react-router-dom";
import {useGetAllCollectionsQuery} from "../../../api/collectionSlice";
import {Collection} from "../../../models/entities";
import {ROUTE} from "../../../constants";
import {PreviewCard} from "../../Cards/PreviewCard/PreviewCard";
import React from "react";
import {NamedSection} from "../../NamedSection/NamedSection";
import {PreviewItemsContainer} from "../../containers/PreviewItemsContainer/PreviewItemsContainer";

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

    // Перемешиваем коллекции
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
        <>
            {/*<div className={style.sliderContainer}>*/}
                <NamedSection title="Кераміка" >
                    <PreviewItemsContainer
                        isLoading={isLoading}
                        // isError={isErrorProducts}
                        // textWhenEmpty="No products available"
                        // textWhenError="Error loading products"
                    >
                        <Slider {...settings}>
                            {
                                shuffledCollections.map((collection) => (
                                    // <div key={collection.id} className={style.cardWrapper}>
                                        <PreviewCard
                                            key={collection.id}
                                            photoSrc={collection.photo}
                                            title={collection.name}
                                            subTitle={collection.category}
                                            onClick={() => handleClickCollectionCard(collection.id)}
                                        />
                                    // </div>
                                ))
                            }
                        </Slider>
                    </PreviewItemsContainer>
                </NamedSection>
            {/*</div>*/}
        </>

    );
}


export default CarouselNewProduct;
