import { Grid, Pagination } from "swiper/modules";
import { SwiperOptions } from "swiper/types";

export const technologySettings: SwiperOptions = {
	grid: {
		rows: 1,
		fill: "row",
	},
	slidesPerView: 4,
	pagination: {
		clickable: true,
	},
	spaceBetween: 20,
	modules: [Grid, Pagination],
	breakpoints: {
		740: {
			grid: {
				rows: 1,
			},
			slidesPerView: 4,
		},
	},
};
