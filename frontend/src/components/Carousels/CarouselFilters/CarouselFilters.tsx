import { useState } from "react";
import Slider from "react-slick";
import "slick-carousel/slick/slick.css";
import "slick-carousel/slick/slick-theme.css";
import style from './style.module.scss'
import {mockDataAllCollection, mockDataDiscount, mockDataPopular} from "../carouselMock";

function CarouselFilters() {
    const [selectedFilter, setSelectedFilter] = useState("popular");

    const handleFilterChange = (filter: string) => {
        setSelectedFilter(filter);
    };

    let mockData;
    switch (selectedFilter) {
        case "popular":
            mockData = mockDataPopular;
            break;
        case "allCollection":
            mockData = mockDataAllCollection;
            break;
        case "discount":
            mockData = mockDataDiscount;
            break;
        default:
            mockData = mockDataPopular;
    }

    const settings = {
        dots: true,
        infinite: true,
        speed: 500,
        slidesToShow: 4,
        slidesToScroll: 4,
        initialSlide: 0,
        arrows: false,

    };

    return (
        <div className={style.sliderContainer} >
            <div className={style.filters}>
                <p className={selectedFilter === 'popular' ? style.selected : ''} style={{cursor:'pointer'}} onClick={() => handleFilterChange("popular")}>Найпопулярніші товари</p>
                <p className={selectedFilter === 'allCollection' ? style.selected : ''} style={{cursor:'pointer'}} onClick={() => handleFilterChange("allCollection")}>Всі колекції</p>
                <p className={selectedFilter === 'discount' ? style.selected : ''} style={{cursor:'pointer'}} onClick={() => handleFilterChange("discount")}>Знижки</p>
            </div>
            <Slider {...settings}>
                {mockData.map((product, index) => (
                    <div key={index} className={style.card}>
                        <div className={style.imageContainer}>
                            {selectedFilter === 'discount' && <p className={style.saleLabel}>Sale</p>}
                            <img src={product.imageUrl} alt={product.name} className={style.image} />
                        </div>
                        <p className={style.name}>{product.name}</p>
                        <div className={style.priceContainer}>
                            <p className={style.price + (selectedFilter === 'discount' ? ' ' + style.strikethrough : '')}>{product.price}</p>
                            {product.newPrice && <p className={style.newPrice}>{product.newPrice}</p>}
                        </div>
                        {product.category && <p className={style.category}>{product.category}</p>}
                    </div>
                ))}
            </Slider>
        </div>
    );
}

export default CarouselFilters;

