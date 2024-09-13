import React, { useCallback } from "react";
import { Technology } from "../../../models/entities";
import { useTranslation } from "react-i18next";
import styles from "./Technology.module.scss";
import default_photo from "../../../assets/default.png";

interface TechnologyProps {
	technology: Technology;
}

export const TechnologyItem: React.FC<TechnologyProps> = ({ technology }) => {
	const { i18n } = useTranslation();
	const language = i18n.language;

	const { name, name_uk, name_en, link, photo_thumbnail_url } = technology;

	const getTranslatedName = useCallback(() => {
		return language === "uk" ? name_uk || name : name_en || name;
	}, [language, name, name_uk, name_en]);

	const translatedName = getTranslatedName();

	return (
		<div>
			<a href={link || "#"} target="_blank" rel="noopener noreferrer">
				<img
					src={photo_thumbnail_url || default_photo}
					alt={translatedName}
					className={styles.content}
				/>
			</a>
		</div>
	);
};
