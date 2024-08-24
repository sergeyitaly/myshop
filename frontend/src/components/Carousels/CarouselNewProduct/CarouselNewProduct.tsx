import Slider from "react-slick";
import "slick-carousel/slick/slick.css";
import "slick-carousel/slick/slick-theme.css";
import { mockDataCategories } from "../carouselMock";
import { useGetAllCollectionsQuery } from "../../../api/collectionSlice";
import { Collection } from "../../../models/entities";
import { ROUTE } from "../../../constants";
import { PreviewCard } from "../../Cards/PreviewCard/PreviewCard";
import { NamedSection } from "../../NamedSection/NamedSection";
import style from "../CarouselNewProduct/style.module.scss";
import { PreviewLoadingCard } from "../../Cards/PreviewCard/PreviewLoagingCard";
import { useNavigate } from "react-router-dom";
import { useTranslation } from 'react-i18next'; // Import the useTranslation hook


// Function to get translated collection name
const getTranslatedCollectionName = (collection: any, language: string): string => {
    return language === 'uk' ? collection.name_uk || collection.name : collection.name_en || collection.name;
};

function CarouselNewProduct() {
    const navigate = useNavigate();
    const { t, i18n } = useTranslation(); // Initialize translation hook

    const { data, isLoading } = useGetAllCollectionsQuery();

    const collections: Collection[] = data?.results || [];

    const handleClickCollectionCard = (id: number) => {
        navigate(ROUTE.COLLECTION + id);
    };

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
            <NamedSection title={t('new_arrivals')}> {/* Translate section title */}
                <Slider {...settings}>
                    {isLoading
                        ? Array.from({ length: 3 }).map((_, index) => (
                            <div key={index} className={style.card}>
                                <PreviewLoadingCard />
                            </div>
                        ))
                        : shuffledCollections.map((collection) => (
                            <PreviewCard
                                className={style.card}
                                key={collection.id}
                                title={getTranslatedCollectionName(collection, i18n.language)} // Translate collection name
                                discount={collection.discount}
                                price={collection.price}
                                currency={collection.currency}
                                photoSrc={collection.photo_url}
                                previewSrc={collection.photo_thumbnail_url}
                                onClick={() => handleClickCollectionCard(collection.id)}
                            />
                        ))}
                </Slider>
            </NamedSection>
        </div>
    );
}

export default CarouselNewProduct;
