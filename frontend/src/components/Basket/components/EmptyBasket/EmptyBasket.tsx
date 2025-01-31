import { AppIcon } from "../../../SvgIconComponents/AppIcon";
import { useTranslation } from "react-i18next";
import styles from "./EmptyBasket.module.scss";

export const EmptyBasket = () => {
	const { t } = useTranslation();

	return (
		<div className={styles.container}>
			<AppIcon iconName="vase" />
			<p>{t("empty_cart")}</p>
		</div>
	);
};
