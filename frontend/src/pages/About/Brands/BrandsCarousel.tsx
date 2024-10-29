import React from "react";
import { useTranslation } from "react-i18next";
import { useGetBrandsQuery } from "../../../api/aboutSlice";
import { AppSlider } from "../../../components/AppSlider/AppSlider";
import { NamedSection } from "../../../components/NamedSection/NamedSection";
import { BrandItem } from "./BrandsItem";
import { technologybrandSettings } from "../TechnologiesCarousel/technologybrandSettings";
import styles from "./Brands.module.scss";

export const BrandsCarousel: React.FC = () => {
	const { t } = useTranslation();

	const { data, isError, isLoading } = useGetBrandsQuery();
	const brandData = data?.results || [];

	return (
		<section className={styles.wrapper}>
			<div className={styles.title}>{t("brands")}</div>

			<NamedSection title="">
				{isError ? (
					<p>{t("empty_brands")}</p>
				) : (
					<div className={styles.sliderContainer}>
						<AppSlider
							isLoading={isLoading}
							sliderSettings={technologybrandSettings}
						>
							{brandData.map((brand, index) => (
								<BrandItem key={index} brand={brand} />
							))}
						</AppSlider>
					</div>
				)}
			</NamedSection>
		</section>
	);
};
