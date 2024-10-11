import { object, string, array } from "yup";
import { TFunction } from "i18next";

export const getOrderValidSchema = (t: TFunction) =>
	object({
		name: string()
			.required(t("field_required"))
			.matches(/^[A-Za-zА-Яа-яІіЇїЄєҐґ\s-]+$/, t("error_name")),
		surname: string()
			.required(t("field_required"))
			.matches(/^[A-Za-zА-Яа-яІіЇїЄєҐґ\s-]+$/, t("error_surname")),
		email: string().required(t("field_required")).email(t("error_email")),
		phone: string()
			.required(t("field_required"))
			.matches(/^\+380\d{9}$/, t("error_phone")),
		order_items: array().min(1, t("min_order")),
	});
