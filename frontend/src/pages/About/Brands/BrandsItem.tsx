import { useTranslation } from "react-i18next";
import { Brand } from "../../../models/entities";
import { AppImage } from "../../../components/AppImage/AppImage";
import { getTranslatedText } from "../translation";
import styles from "./Brands.module.scss";

interface BrandItemProps {
	brand: Brand;
}

export const BrandItem: React.FC<BrandItemProps> = ({ brand }) => {
	const { name, name_en, name_uk, photo_url, link } = brand;
	const { i18n } = useTranslation();
	const language = i18n.language;

	const translatedName = getTranslatedText(name, name_uk, name_en, language);

	return (
		<a href={link || "#"} target="_blank" rel="noopener noreferrer">
			<AppImage
				src={photo_url}
				alt={translatedName}
				className={styles.imageSize}
			/>
		</a>
	);
};
