import { Grid, Pagination } from "swiper/modules";
import { SwiperOptions } from "swiper/types";

export const teamSettings: SwiperOptions = {
	grid: {
		rows: 1,
		fill: "row",
	},
	slidesPerView: 3,
	pagination: {
		clickable: true,
	},
	spaceBetween: 10,
	modules: [Grid, Pagination],

	breakpoints: {
		1024: {
			slidesPerView: 3,
		},
		740: {
			slidesPerView: 2,
		},
		0: {
			slidesPerView: 2,
		},
	},
};
