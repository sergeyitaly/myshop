import React from "react";
import Slider from "react-slick";
import "slick-carousel/slick/slick.css";
import "slick-carousel/slick/slick-theme.css";
import { useGetTechnologiesQuery } from "../../../api/aboutSlice";
import { TechnologyItem } from "./TechnologyItem";
import { useTranslation } from "react-i18next";
import styles from "./Technology.module.scss";
import { PreviewLoadingCard } from "../../../components/Cards/PreviewCard/PreviewLoagingCard";

export const TechnologiesCarousel: React.FC = () => {
	const { data, isError, isLoading } = useGetTechnologiesQuery();
	const { t } = useTranslation();

	const settings = {
		dots: true,
		infinite: true,
		speed: 500,
		slidesToShow: 4,
		slidesToScroll: 3,
		arrows: false,
	};

	const technologyData = data?.results || [];

	return (
		<div className={styles.container}>
			<div className={styles.title}>{t("technology")}</div>
			{isError ? (
				<p>{t("products.error")}</p>
			) : (
				<Slider {...settings}>
					{isLoading ? (
						Array.from({ length: 4 }).map((_, index) => (
							<div key={index} className={styles.content}>
								<PreviewLoadingCard />
							</div>
						))
					) : technologyData.length > 0 ? (
						technologyData.map((technology, index) => (
							<div key={index}>
								<TechnologyItem technology={technology} />
							</div>
						))
					) : (
						<p>{t("empty_technology")}</p>
					)}
				</Slider>
			)}
		</div>
	);
};
