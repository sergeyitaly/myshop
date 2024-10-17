import { Brand } from "../../../models/entities";
import { AppImage } from "../../../components/AppImage/AppImage";
import { useAppTranslator } from "../../../hooks/useAppTranslator";
import styles from "./Brands.module.scss";

interface BrandItemProps {
	brand: Brand;
}

export const BrandItem: React.FC<BrandItemProps> = ({ brand }) => {
	const { photo_url, link } = brand;

	const { getTranslatedBrandName } = useAppTranslator();

	return (
		<a href={link || "#"} target="_blank" rel="noopener noreferrer">
			<AppImage
				src={photo_url}
				alt={getTranslatedBrandName(brand)}
				className={styles.imageSize}
			/>
		</a>
	);
};
