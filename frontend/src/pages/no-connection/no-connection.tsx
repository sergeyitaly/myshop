import { useTranslation } from "react-i18next";
import styles from "./no-connection.module.scss";


export const NoConnectionPage = () => {
	const { t } = useTranslation();

	const ImgError = new URL("./img-error.png", import.meta.url).href;

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