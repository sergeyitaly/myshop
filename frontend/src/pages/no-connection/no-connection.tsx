import { useTranslation } from "react-i18next";
import ImgError from "./img-error.png";
import styles from "./no-connection.module.scss";

export const NoConnectionPage = () => {
	const { t } = useTranslation();

	// Helper function to detect if running in an Android WebView
	const isAndroidWebView = () => {
		const userAgent = navigator.userAgent || navigator.vendor;
		return /Android/.test(userAgent) && /wv/.test(userAgent);
	};

	const handleRetry = () => {
		if (isAndroidWebView()) {
			// Send a custom event or perform a specific action for Android WebView
			if (window.AndroidInterface && window.AndroidInterface.reloadPage) {
				// Example: Call a method exposed by the Android WebView
				window.AndroidInterface.reloadPage();
			} else {
				alert(t("no_connection_android_error")); // Fallback message
			}
		} else {
			// Default behavior for web browsers
			window.location.reload();
		}
	};

	return (
		<main className={styles.main}>
			<img
				src={ImgError}
				alt={t("no_connection_alt")}
				className={styles.img}
			/>
			<h2 className={styles.message}>
				{t("no_connection_message")}
			</h2>
			<button
				className={styles.button}
				onClick={handleRetry}
			>
				{t("no_connection_retry")}
			</button>
		</main>
	);
};
