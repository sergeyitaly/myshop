import { useTranslation } from "react-i18next"; 
import ImgError from "./connection-error.png";


export const NoConnectionPage = () => {
	const { t } = useTranslation();

	return (
		<main>
			<img src={ImgError} alt="No connection" />
			<h2>{t("no_connection_message")}</h2>
			<button
				onClick={() => window.location.reload()}
			>
				{t("no_connection_retry")}
			</button>
		</main>
	);
};
