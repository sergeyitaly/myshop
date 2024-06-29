import React from "react";
import { Link } from "react-router-dom";
import Slider from "react-slick";
import style from "./style.module.scss";
import { Product } from "../../../models/entities";
import defaultPhoto from '../../../assets/default.png'
import { useGetAllProductsQuery } from "../../../api/productSlice";

const CarouselBestseller: React.FC = () => {
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

  const {data} = useGetAllProductsQuery()

  const products: Product[] = data?.results || []

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
                  src={product.photo || defaultPhoto}
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
