import { useTranslation } from "react-i18next";
import clsx from "clsx";
import style from "./AvailableLable.module.scss";

interface AvailableLableProps {
	isAvailable: boolean;
	className?: string;
}

export const AvailableLable = ({
	isAvailable,
	className,
}: AvailableLableProps) => {
	const { t } = useTranslation();

	return (
		<div
			className={clsx(
				style.label,
				{ [style.available]: isAvailable },
				className
			)}
		>
			{isAvailable ? t("available") : t("unavailable")}
		</div>
	);
};
