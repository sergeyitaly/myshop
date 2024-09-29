import { useTranslation } from "react-i18next"; 
import { Link as RouterLink } from "react-router-dom"; 
import Img404 from "./404 error.png";
import styles from "./not-found.module.scss";

export const NotFound = () => {
	const { t } = useTranslation(); 

	return (
		<main className={styles.main}>
			<img className={styles.img} src={Img404} alt="404" />
			<h2 className={styles.message}>{t("not_found_message")}</h2>
			<RouterLink to="/" className={styles.link}>
				{t("return_to_home")}
			</RouterLink>
		</main>
	);
};
