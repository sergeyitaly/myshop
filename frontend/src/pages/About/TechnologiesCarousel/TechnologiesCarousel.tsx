import React from "react";
import { useTranslation } from "react-i18next";
import { useGetTechnologiesQuery } from "../../../api/aboutSlice";
import { AppSlider } from "../../../components/AppSlider/AppSlider";
import { NamedSection } from "../../../components/NamedSection/NamedSection";
import { TechnologyItem } from "./TechnologyItem";
import { technologySettings } from "./technologySettings";
import styles from "./Technology.module.scss";

export const TechnologiesCarousel: React.FC = () => {
	const { t } = useTranslation();

	const { data, isError, isLoading } = useGetTechnologiesQuery();
	const technologyData = data?.results || [];

	return (
		<section className={styles.wrapper}>
			<div className={styles.title}>{t("technology")}</div>

			<NamedSection title="">
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
			</NamedSection>
		</section>
	);
};
