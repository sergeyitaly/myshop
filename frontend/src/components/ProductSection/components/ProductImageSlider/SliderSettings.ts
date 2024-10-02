import { Settings } from "react-slick";
import styles from "./ProductImageSlider.module.scss";
import "./active-dots.css";

export const settings: Settings = {
	dots: true,
	dotsClass: styles.dots,
	arrows: false,
	infinite: false, // Set to false for non-infinite scrolling
	speed: 500,
	slidesToShow: 1,
	slidesToScroll: 1,
};
