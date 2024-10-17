import { Grid, Pagination } from "swiper/modules";
import { SwiperOptions } from "swiper/types";

export const technologybrandSettings: SwiperOptions = {
	grid: {
		rows: 1,
		fill: "row",
	},
	slidesPerView: 4,
	pagination: {
		clickable: true,
	},
	spaceBetween: 20,
	loop: true,
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
