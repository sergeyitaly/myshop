import { Technology } from "../../../models/entities";
import { AppImage } from "../../../components/AppImage/AppImage";
import { useAppTranslator } from "../../../hooks/useAppTranslator";
import styles from "./Technology.module.scss";

interface TechnologyProps {
	technology: Technology;
}

export const TechnologyItem: React.FC<TechnologyProps> = ({ technology }) => {
	const { getTranslatedTechnologyName } = useAppTranslator();

	const { link, photo_url } = technology;

	return (
		<div className={styles.container}>
			<a href={link || "#"} target="_blank" rel="noopener noreferrer">
				<AppImage
					src={photo_url}
					alt={getTranslatedTechnologyName(technology)}
					className={styles.imageSize}
				/>
			</a>
		</div>
	);
};
