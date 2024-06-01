import React from "react";
import { Link } from "react-router-dom";
import Slider from "react-slick";
import style from "./style.module.scss";

interface Product {
  id: string;
  name: string;
  price: number | string;
  photo: string;
}

interface CarouselBestsellerProps {
  products: Product[];
}

const CarouselBestseller: React.FC<CarouselBestsellerProps> = ({
  products,
}) => {
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
        },
      },
    ],
  };

  return (
    <div className={style.sliderContainer}>
      <p className={style.title}>Бестселери</p>
      <Slider {...settings}>
        {products.map((product) => (
          <Link
            to={`/product/${product.id}`}
            key={product.id}
            className={style.card}
          >
            <div className={style.card}>
              <div className={style.cardImage}>
                <img
                  src={product.photo}
                  alt={product.name}
                  className={style.image}
                  loading="lazy"
                />
                <p className={style.name}>{product.name}</p>
                <p className={style.price}>{product.price}</p>
              </div>
            </div>
          </Link>
        ))}
      </Slider>
    </div>
  );
};

export default CarouselBestseller;
