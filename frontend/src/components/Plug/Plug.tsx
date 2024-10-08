import clsx from "clsx";
import { useTranslation } from "react-i18next";
import style from "./Plug.module.scss";

interface PlugProps {
	className?: string;
	title?: string;
}

export const Plug = ({ className }: PlugProps) => {
	const { t } = useTranslation();
	return <div className={clsx(style.plug, className)}>{t("sale")}</div>;
};
