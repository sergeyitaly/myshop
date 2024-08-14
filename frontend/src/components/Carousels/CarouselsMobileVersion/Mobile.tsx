import Slider from "react-slick";
import "slick-carousel/slick/slick.css";
import "slick-carousel/slick/slick-theme.css";
import style from './style.module.scss'
import {PreviewCard} from "../../Cards/PreviewCard/PreviewCard";
import {useNavigate} from "react-router-dom";
import {
    useGetAllCollectionsQuery,
    useGetDiscountProductsQuery,
    useGetProductsByPopularityQuery,
} from "../../../api/collectionSlice";
import {Collection} from "../../../models/entities";
import {ROUTE} from "../../../constants";
import styles from "../CarouselsMobileVersion/style.module.scss";
import {PreviewLoadingCard} from "../../Cards/PreviewCard/PreviewLoagingCard";

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
                {isLoading
                    ? Array.from({ length: 3 }).map((_, index) => (
                        <div key={index} className={style.container}>
                            <PreviewLoadingCard />
                        </div>
                    ))
                    : collections.map((product) => (
                        <div key={product.id} className={style.container}>
                            <PreviewCard
                                className={style.card}
                                key={product.id}
                                photoSrc={product.photo || ''}
                                title={product.name}
                                // discount = {product.discount}
                                // price={product.price}
                                // currency={product.currency}
                                previewSrc={product.photo_thumbnail_url}
                                onClick={() => handleClickCollectionCard(product.id)}
                            />
                        </div>
                    ))}
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
                                title={product.name}
                                discount = {product.discount}
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


export function Discount () {

    const navigate = useNavigate();

    const { data: discountProductsData, isLoading: isLoadingDiscountProducts } = useGetDiscountProductsQuery();
    const discountProducts = discountProductsData?.results.filter(product => parseFloat(product.discount) > 0) || [];

    console.log('Discount products:', discountProducts);

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
        navigate(`${ROUTE.PRODUCT}${productId}`)
    }

    return (
        <div className={style.sliderContainer} >
            <p className={style.title}> Знижки </p>
            {
                discountProducts.length === 1 ? (
                    // <PreviewCard
                    //     className={style.cardNew}
                    //     key={discountProducts[0].id}
                    //     photoSrc={discountProducts[0].photo || ''}
                    //     title={discountProducts[0].name}
                    //     discount={discountProducts[0].discount}
                    //     price={discountProducts[0].price}
                    //     currency={discountProducts[0].currency}
                    //     onClick={() => handleClickProduct(discountProducts[0].id)}
                    // />
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
                                        className={styles.card}
                                        key={product.id}
                                        title={product.name}
                                        discount = {product.discount}
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

