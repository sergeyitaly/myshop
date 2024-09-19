import React from "react";
import { useTranslation } from "react-i18next";
import { useGetTechnologiesQuery } from "../../../api/aboutSlice";
import { AppSlider } from "../../../components/AppSlider/AppSlider";
import { TechnologyItem } from "./TechnologyItem";
import { technologySettings } from "./technologySettings";
import styles from "./Technology.module.scss";

export const TechnologiesCarousel: React.FC = () => {
	const { t } = useTranslation();

	const { data, isError, isLoading } = useGetTechnologiesQuery();
	const technologyData = data?.results || [];

	return (
		<div className={styles.container}>
			<div className={styles.title}>{t("technology")}</div>

			{isError ? (
				<p>{t("empty_technology")}</p>
			) : (
				<div className={styles.sliderContainer}>
					<AppSlider
						isLoading={isLoading}
						sliderSettings={technologySettings}
					>
						{technologyData.map((technology, index) => (
							<TechnologyItem
								key={index}
								technology={technology}
							/>
						))}
					</AppSlider>
				</div>
			)}
		</div>
	);
};
