import style from "../../../components/Carousels/CarouselCeramic/style.module.scss";
import {mockDataProducts} from "../../../components/Carousels/carouselMock";
import Slider from "react-slick";
import "slick-carousel/slick/slick.css";
import "slick-carousel/slick/slick-theme.css";

function CarouselBestseller () {
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
                breakpoint: 700,
                settings: {
                    slidesToShow: 2,
                    slidesToScroll: 2,
                    initialSlide: 0,
                }
            }
        ]
    };
    return (
        <div className={style.sliderContainer}>
            <p className={style.title}>Бестселери</p>
            <Slider {...settings}>
                {mockDataProducts.map((product, index) => (
                    <div key={index} className={style.card}>
                        <div className={style.cardImage}>
                            <img src={product.imageUrl} alt={product.name} className={style.image}/>
                            <p className={style.name} >{product.name}</p>
                            <p className={style.price}>{product.price}</p>
                        </div>
                    </div>
                ))}
            </Slider>
        </div>
    );
}


export default CarouselBestseller ;
