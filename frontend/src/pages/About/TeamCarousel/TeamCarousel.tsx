import React from "react";
import Slider from "react-slick";
import "slick-carousel/slick/slick.css";
import "slick-carousel/slick/slick-theme.css";
import { useGetTeamMembersQuery } from "../../../api/aboutSlice";
import { TeamItem } from "./TeamItem";
import { useTranslation } from "react-i18next";
import styles from "./TeamCarousel.module.scss";
import { PreviewLoadingCard } from "../../../components/Cards/PreviewCard/PreviewLoagingCard";

export const TeamCarousel: React.FC = () => {
	const { data, isError, isLoading } = useGetTeamMembersQuery();
	const { t } = useTranslation();

	const settings = {
		dots: true,
		infinite: true,
		speed: 500,
		slidesToShow: 3,
		slidesToScroll: 2,
		arrows: false,
		responsive: [
			{
				breakpoint: 1366,
				settings: {
					slidesToShow: 2,
					slidesToScroll: 1,
				},
			},
			{
				breakpoint: 1280,
				settings: {
					slidesToShow: 2,
					slidesToScroll: 1,
				},
			},
			{
				breakpoint: 600,
				settings: {
					slidesToShow: 2,
					slidesToScroll: 1,
				},
			}
		],
	};

	const teamData = data?.results || [];

	return (
		<div className={styles.container}>
			<div className={styles.title}>{t("our_team")}</div>
			{isError ? (
				<p>{t("products.error")}</p>
			) : (
				<Slider {...settings}>
					{isLoading ? (
						Array.from({ length: 3 }).map((_, index) => (
							<div key={index} className={styles.sliderItem}>
								<PreviewLoadingCard />
							</div>
						))
					) : teamData.length > 0 ? (
						teamData.map((member, index) => (
							<div key={index} className={styles.sliderItem}>
								<TeamItem member={member} />
							</div>
						))
					) : (
						<p>{t("empty_team")}</p>
					)}
				</Slider>
			)}
		</div>
	);
};
