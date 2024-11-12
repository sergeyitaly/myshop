import { Autoplay, Grid, Pagination } from "swiper/modules";
import { SwiperOptions } from "swiper/types";

export const teamSettings: SwiperOptions = {
	grid: {
		rows: 1,
		fill: "row",
	},
	slidesPerView: 3,
	slidesPerGroup: 3,
	pagination: {
		clickable: true,
	},
	spaceBetween: 20,
	speed: 1000,
	modules: [Grid, Pagination, Autoplay],

	breakpoints: {
		1024: {
			slidesPerView: 3,
		},
		740: {
			slidesPerView: 3,
		},
		500: {
			slidesPerView: 3,
		},
		0: {
			slidesPerView: 2,
		},
	},
};
