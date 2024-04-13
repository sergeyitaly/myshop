import Slider from "react-slick";
import "slick-carousel/slick/slick.css";
import "slick-carousel/slick/slick-theme.css";
import style from './style.module.scss'
import {mockDataProducts} from "../carouselMock";

function CarouselCeramic () {
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
        <div className={style.sliderContainer}>
            <p className={style.title}>Керамічний фольклор</p>
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


export default CarouselCeramic ;
