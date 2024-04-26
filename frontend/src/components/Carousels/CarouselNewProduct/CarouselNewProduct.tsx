import Slider from "react-slick";
import "slick-carousel/slick/slick.css";
import "slick-carousel/slick/slick-theme.css";
import style from './style.module.scss'
import {mockDataCategories} from "../carouselMock";

function CarouselNewProduct () {

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
            <p className={style.title}> Нові надходження </p>
            <Slider {...settings}>
                {mockDataCategories.map((product, index) => (
                    <div key={index} className={style.card}>
                        <div className={style.cardImage}>
                            <img src={product.imageUrl} alt={product.name} style={{maxWidth:'100%'}}/>
                            <p className={style.name}>{product.name}</p>
                        </div>
                    </div>
                ))}
            </Slider>
        </div>
    );
}


export default CarouselNewProduct;
