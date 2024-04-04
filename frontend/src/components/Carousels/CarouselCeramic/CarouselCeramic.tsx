import Slider from "react-slick";
import "slick-carousel/slick/slick.css";
import "slick-carousel/slick/slick-theme.css";
import style from './style.module.scss'
import {mockDataProducts} from "../carouselMock";


const CustomPrevArrow: React.FC<React.ButtonHTMLAttributes<HTMLButtonElement>> = (props) => {
    const { onClick } = props;
    return (
        <button className="slick-prev" onClick={onClick}>
            Prev
        </button>
    );
};

const CustomNextArrow: React.FC<React.ButtonHTMLAttributes<HTMLButtonElement>> = (props) => {
    const { onClick } = props;
    return (
        <button className="slick-next" onClick={onClick}>
            Next
        </button>
    );
};

function CarouselCeramic () {
    const settings = {
        dots: true,
        infinite: true,
        speed: 500,
        slidesToShow: 3,
        slidesToScroll: 3,
        initialSlide: 0,
        prevArrow: <CustomPrevArrow />,
        nextArrow: <CustomNextArrow />,
        arrows: false,
        responsive: [
            {
                breakpoint: 1024,
                settings: {
                    slidesToShow: 3,
                    slidesToScroll: 3,
                    infinite: true,
                    dots: true,
                }
            },
            {
                breakpoint: 600,
                settings: {
                    slidesToShow: 2,
                    slidesToScroll: 2,
                    initialSlide: 2
                }
            },
            {
                breakpoint: 480,
                settings: {
                    slidesToShow: 1,
                    slidesToScroll: 1
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
                            <img src={product.imageUrl} alt={product.name} style={{maxWidth:'100%'}}/>
                            <p className={style.name} style={{marginTop:'15px', textAlign:'center'}}>{product.name}</p>
                            <p className={style.price}>{product.price}</p>
                        </div>
                    </div>
                ))}
            </Slider>
        </div>
    );
}


export default CarouselCeramic ;
