import { Product, ProductVariantsModel } from "../../../../models/entities";
import { DropDown } from "../DropDown/DropDown";
import { ProductControl } from "../ProductControl/ProductControl";
import { useTranslation } from "react-i18next";
import styles from "./ProductInfo.module.scss";

const getTranslatedProductDescription = (
	product: any,
	language: string
): string => {
	return language === "uk"
		? product.description_uk || product.description
		: product.description_en || product.description;
};

const getTranslatedAdditionalField = (
	field: any,
	language: string
): { name: string; value: string } => {
	return {
		name:
			language === "uk"
				? field.name_uk || field.name
				: field.name_en || field.name,
		value:
			language === "uk"
				? field.value_uk || field.value
				: field.value_en || field.value,
	};
};

interface ProductInfoProps {
	product: Product;
	discountPrice: number | null;
	productVariants: ProductVariantsModel;
	onChangeColor: (color: string) => void;
	onChangeSize: (size: string) => void;
}

export const ProductInfo = ({
	product,
	discountPrice,
	productVariants,
	onChangeColor,
	onChangeSize,
}: ProductInfoProps) => {
	const { i18n, t } = useTranslation();
	const language = i18n.language;

	const translatedDescription = getTranslatedProductDescription(
		product,
		language
	);
	const translatedAdditionalFields = product.additional_fields?.map((field) =>
		getTranslatedAdditionalField(field, language)
	);

	return (
		<div className={styles.container}>
			<div className={styles.productInfo}>
				<ProductControl
					discountPrice={discountPrice}
					product={product}
					variants={productVariants}
					onChangeColor={onChangeColor}
					onChangeSize={onChangeSize}
				/>
				<div className={styles.description}>
					<h3>{t("description")}</h3>
					<p>
						{translatedDescription || i18n.t("description_missing")}
					</p>
				</div>
			</div>

			{translatedAdditionalFields &&
				translatedAdditionalFields.map(({ name, value }, index) => (
					<DropDown
						key={index}
						className={styles.applyDropdown}
						changebleParam={product.id}
						title={name}
						content={value}
					/>
				))}
		</div>
	);
};
