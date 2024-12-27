import { useTranslation } from "react-i18next";
import ImgError from "./img-error.png";
import styles from "./no-connection.module.scss";

export const NoConnectionPage = () => {
  const { t } = useTranslation();

  const handleRetry = () => {
	if ((window as any).Android && typeof (window as any).Android.reloadWebView === "function") {
	  (window as any).Android.reloadWebView(); // Trigger the Android reloadWebView method
	} else {
	  window.location.reload();
	}
  };
  

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
        onClick={handleRetry}
      >
        {t("no_connection_retry")}
      </button>
    </main>
  );
};
