import { useTranslation } from "react-i18next";
import styles from "./no-connection.module.scss";

export const NoConnectionPage = () => {
	const { t } = useTranslation();
	const isAndroidWebView = () => {
		const userAgent = navigator.userAgent || "";
		return /Android/.test(userAgent) && /wv/.test(userAgent) && !/Chrome\/[.0-9]* Mobile/.test(userAgent);
	};
	const handleRetry = async () => {
		if (!navigator.onLine) {
			alert(t("no_connection_offline_alert"));
			return;
		}
		if (isAndroidWebView()) {
			if (window.AndroidInterface && window.AndroidInterface.reloadPage) {
				window.AndroidInterface.reloadPage();
			} else {
				alert(t("no_connection_android_error"));
			}
		} else {
			try {
				if ("caches" in window) {
					const cacheKeys = await caches.keys();
					await Promise.all(cacheKeys.map((key) => caches.delete(key)));
					console.log("Caches cleared successfully");
				}
			} catch (error) {
				console.error("Error clearing cache:", error);
			}
			window.location.reload();
		}
	};

	const ImgError = navigator.onLine
		? new URL("./img-error.png", import.meta.url).href
		: null;

	return (
		<main className={styles.main}>
			<img
				src={ImgError || "./img-error.png"}
				alt={t("no_connection_alt")}
				className={styles.img}
			/>
			<h2 className={styles.message}>{t("no_connection_message")}</h2>
			<button className={styles.button} onClick={handleRetry}>
				{t("no_connection_retry")}
			</button>
		</main>
	);
};