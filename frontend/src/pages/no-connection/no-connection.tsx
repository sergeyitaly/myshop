import { useTranslation } from "react-i18next"; 
import Img404 from "./404 error.png";


export const NoConnectionPage = () => {
	const { t } = useTranslation();

	return (
		<main>
			<img src={Img404} alt="404" />
			<h2>{t("no_connection_message")}</h2>
			<button
				onClick={() => window.location.reload()}
			>
				{t("no_connection_retry")}
			</button>
		</main>
	);
};
