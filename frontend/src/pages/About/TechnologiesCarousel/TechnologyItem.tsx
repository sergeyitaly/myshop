import { Technology } from "../../../models/entities";
import { useTranslation } from "react-i18next";
import { AppImage } from "../../../components/AppImage/AppImage";
import { getTranslatedText } from "../translation";
import styles from "./Technology.module.scss";

interface TechnologyProps {
	technology: Technology;
}

export const TechnologyItem: React.FC<TechnologyProps> = ({ technology }) => {
	const { i18n } = useTranslation();
	const language = i18n.language;

	const { name, name_uk, name_en, link, photo_url } = technology;

	const translatedName = getTranslatedText(name, name_uk, name_en, language);

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
