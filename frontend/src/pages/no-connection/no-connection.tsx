import { useTranslation } from "react-i18next"; 
import ImgError from "./img-error.png";
import styles from "./no-connection.module.scss";


export const NoConnectionPage = () => {
	const { t } = useTranslation();

	return (
		<main className={styles.main}>
			<img
				src={ImgError}
				alt="No connection"
				className={styles.img}
			/>
			<h2 className={styles.message}>
				{t("no_connection_message")}
			</h2>
			<button
				className={styles.button}
				onClick={() => window.location.reload()}
			>
				{t("no_connection_retry")}
			</button>
		</main>
	);
};
