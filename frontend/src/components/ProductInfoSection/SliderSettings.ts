import { Settings } from "react-slick";
import styles from './ProductInfoSection.module.scss'
import './active-dots.css'



export const settings: Settings = {
    dots: true,
    dotsClass: styles.dots,
    arrows: false,
    infinite: true,
    speed: 500,
    slidesToShow: 1,
    slidesToScroll: 1,
  };