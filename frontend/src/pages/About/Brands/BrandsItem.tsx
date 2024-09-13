import React, { useCallback } from "react";
import { useTranslation } from "react-i18next";
import { Brand } from "../../../models/entities";
import styles from "./Brands.module.scss";
import default_photo from "../../../assets/default.png";

interface BrandItemProps {
	brand: Brand;
}

export const BrandItem: React.FC<BrandItemProps> = ({ brand }) => {
	const { name, name_en, name_uk, photo_thumbnail_url, link } = brand;
	const { i18n } = useTranslation();
	const language = i18n.language;
	const imageUrl = photo_thumbnail_url || default_photo;

	const getTranslatedName = useCallback(() => {
		return language === "uk" ? name_uk || name : name_en || name;
	}, [language, name, name_uk, name_en]);

	const translatedName = getTranslatedName();

	return (
		<a href={link || "#"} target="_blank" rel="noopener noreferrer">
			<img className={styles.img} src={imageUrl} alt={translatedName} />
		</a>
	);
};
