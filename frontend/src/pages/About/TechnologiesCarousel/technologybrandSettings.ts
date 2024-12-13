import { Autoplay, Grid, Pagination } from "swiper/modules";
import { SwiperOptions } from "swiper/types";

export const technologybrandSettings: SwiperOptions = {
	grid: {
		rows: 1,
		fill: "row",
	},
	slidesPerView: 4,
	slidesPerGroup: 4,
	pagination: {
		clickable: true,
	},
	spaceBetween: 20,
	speed: 1200,

	modules: [Grid, Pagination, Autoplay],
	breakpoints: {
		740: {
			grid: {
				rows: 1,
			},
			slidesPerView: 4,
			slidesPerGroup: 4,
		},
	},
};
