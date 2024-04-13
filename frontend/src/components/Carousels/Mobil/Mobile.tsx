import Slider from "react-slick";
import "slick-carousel/slick/slick.css";
import "slick-carousel/slick/slick-theme.css";
import style from './style.module.scss'
import {mockDataAllCollection, mockDataDiscount, mockDataProducts} from "../carouselMock";

export function AllCollection() {
    const settings = {
        dots: true,
        infinite: true,
        speed: 500,
        slidesToShow: 3,
        slidesToScroll: 3,
        initialSlide: 0,
        arrows: false,
    };
    return (
        <div className={style.sliderContainer}>
            <p className={style.title}>Всі колекції</p>
            <Slider {...settings}>
                {mockDataAllCollection.map((product, index) => (
                    <div key={index} className={style.card}>
                        <div className={style.cardImage}>
                            <img src={product.imageUrl} alt={product.name} style={{maxWidth:'100%'}}/>
                            <p className={style.name}>{product.name}</p>
                            <p className={style.category}>{product.category}</p>
                        </div>
                    </div>
                ))}
            </Slider>
        </div>
    );
}


export function Popular () {
    const settings = {
        infinite: true,
        // slidesToShow: 2, // Показываем по 2 слайда в видимой области
        slidesPerRow: 2, // Показываем по 2 слайда в каждом ряду
        rows: 2, // Делим слайды на 2 ряда
        speed: 500,
    };
    return (
        <div className={style.sliderContainer}>
            <p className={style.title}>Найпопулярніші товари</p>
            <Slider {...settings}>
                {mockDataProducts.map((product, index) => (
                    <div key={index} className={style.cardRow}>
                        <div className={style.cardImage}>
                            <img src={product.imageUrl} alt={product.name} className={style.image}/>
                            <p className={style.name}>{product.name}</p>
                            <p className={style.price}>{product.price}</p>
                        </div>
                    </div>
                ))}
            </Slider>
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
        <div className={style.sliderContainer} style={{marginTop:'-30px'}}>
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

