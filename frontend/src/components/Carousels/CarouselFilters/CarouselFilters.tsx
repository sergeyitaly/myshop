import Slider from "react-slick";
import "slick-carousel/slick/slick.css";
import "slick-carousel/slick/slick-theme.css";
import style from './style.module.scss'
import {useNavigate} from "react-router-dom";
import {
    useGetAllCollectionsQuery,
    useGetDiscountProductsQuery,
    useGetProductsByPopularityQuery
} from "../../../api/collectionSlice";
import {ROUTE} from "../../../constants";
import {PreviewCard} from "../../Cards/PreviewCard/PreviewCard";
import {PreviewLoadingCard} from "../../Cards/PreviewCard/PreviewLoagingCard";
import styles from '../CarouselFilters/style.module.scss'
import {useState} from "react";

interface Product {
    id: number;
    photo: string | null;
    photo_thumbnail_url: string | null;
    name: string;
    discount: string;
    price: string;
    currency: string;
}

interface Collection {
    id: number;
    photo: string | null;
    photo_thumbnail_url: string | null;
    name: string;
}

type DisplayedItem = Product | Collection;

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
    const { data: popularProductsData } = useGetProductsByPopularityQuery({ popularity: '6' });
    const { data: discountProductsData } = useGetDiscountProductsQuery();

    const collections: Collection[] = collectionsData?.results || [];
    const popularProducts: Product[] = popularProductsData?.results.filter(product => parseFloat(product.discount) === 0) || [];
    const discountProducts: Product[] = discountProductsData?.results.filter(product => parseFloat(product.discount) > 0) || [];

    let displayedData: DisplayedItem[];
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
        <div className={styles.sliderContainer} >
            <div className={style.filters}>
                <p className={selectedFilter === 'popular' ? style.selected : ''} style={{cursor:'pointer'}} onClick={() => handleFilterChange("popular")}>Найпопулярніші товари</p>
                <p className={selectedFilter === 'allCollection' ? style.selected : ''} style={{cursor:'pointer'}} onClick={() => handleFilterChange("allCollection")}>Всі колекції</p>
                <p className={selectedFilter === 'discount' ? style.selected : ''} style={{cursor:'pointer'}} onClick={() => handleFilterChange("discount")}>Знижки</p>
            </div>
            {
                selectedFilter === "discount" && discountProducts.length === 1 ? (
                    <PreviewCard
                        className={style.cardNew}
                        key={discountProducts[0].id}
                        photoSrc={discountProducts[0].photo || ''}
                        title={discountProducts[0].name}
                        discount={discountProducts[0].discount}
                        price={discountProducts[0].price}
                        // currency={discountProducts[0].currency}
                        previewSrc={discountProducts[0].photo_thumbnail_url}
                        onClick={() => handleClickItem(discountProducts[0].id)}
                    />
                ) : (
                    <Slider {...settings}>
                        {isLoadingCollections
                            ? Array.from({ length: 3 }).map((_, index) => (
                                <div key={index} className={style.card}>
                                    <PreviewLoadingCard />
                                </div>
                            ))
                            : displayedData.map((product) => (
                                <div key={product.id} className={style.card}>
                                    {/*<PreviewCard*/}
                                    {/*    key={product.id}*/}
                                    {/*    photoSrc={product.photo || ''}*/}
                                    {/*    title={product.name}*/}
                                    {/*    discount = {product.discount}*/}
                                    {/*    price={product.price}*/}
                                    {/*    currency={product.currency}*/}
                                    {/*    previewSrc={product.photo_thumbnail_url}*/}
                                    {/*    onClick={() => handleClickItem(product.id)}*/}
                                    {/*/>*/}
                                </div>
                            ))}
                    </Slider>
                )
            }
        </div>
    );
}

export default CarouselFilters;

