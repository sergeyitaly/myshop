import React, { useCallback } from "react";
import { Technology } from "../../../models/entities";
import { useTranslation } from "react-i18next";
import { AppImage } from "../../../components/AppImage/AppImage";
import styles from "./Technology.module.scss";

interface TechnologyProps {
	technology: Technology;
}

export const TechnologyItem: React.FC<TechnologyProps> = ({ technology }) => {
	const { i18n } = useTranslation();
	const language = i18n.language;

	const { name, name_uk, name_en, link, photo_url } = technology;

	const getTranslatedName = useCallback(() => {
		return language === "uk" ? name_uk || name : name_en || name;
	}, [language, name, name_uk, name_en]);

	const translatedName = getTranslatedName();

	return (
		<div className={styles.imageWrapper}>
			<a href={link || "#"} target="_blank" rel="noopener noreferrer">
				<AppImage
					src={photo_url}
					alt={translatedName}
					className={styles.imageSize}
				/>
			</a>
		</div>
	);
};
