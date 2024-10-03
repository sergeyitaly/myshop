import { useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { Product, ProductVariantsModel } from "../../../../models/entities";
import { AvailableLable } from "../../../AvailableLabel/AvailableLabel";
import { Counter } from "../../../Counter/Counter";
import { MainButton } from "../../../UI/MainButton/MainButton";
import { ValueBox } from "../../../ProductVariants/ValueBox/ValueBox";
import { ProductVariants } from "../../../ProductVariants/ProductVariants";
import { useBasket } from "../../../../hooks/useBasket";
import { useCounter } from "../../../../hooks/useCounter";
import { formatPrice } from "../../../../functions/formatPrice";
import { ROUTE } from "../../../../constants";
import { useTranslation } from "react-i18next";
import style from "./ProductControl.module.scss";

const getTranslatedProductName = (product: any, language: string): string => {
	return language === "uk"
		? product.name_uk || product.name
		: product.name_en || product.name;
};

const getTranslatedColorName = (product: any, language: string): string => {
	return language === "uk"
		? product.color_name_uk || product.color_name || ""
		: product.color_name_en || product.color_name || "";
};

interface ProductControlProps {
	discountPrice?: number | null;
	product: Product;
	variants: ProductVariantsModel;
	onChangeColor?: (color: string) => void;
	onChangeSize?: (size: string) => void;
	colors?: string[];
}

export const ProductControl = ({
	discountPrice,
	product,
	variants,
	onChangeColor,
	onChangeSize,
}: ProductControlProps) => {
	const { t, i18n } = useTranslation();
	const language = i18n.language;

	const { available, price, currency, color_value } = product;
	const { colors, sizes } = variants;
	console.log("colors");

	const { qty, setCounter } = useCounter(1);

	useEffect(() => {
		setCounter(1);
	}, [product.id]);

	const { addToBasket, openBasket } = useBasket();
	const navigate = useNavigate();

	const handleAddToBasket = () => {
		addToBasket(product, qty);
		openBasket();
	};

	const handleClickBuyNow = () => {
		addToBasket(product, qty);
		navigate(ROUTE.ORDER);
	};

	return (
		<div className={style.container}>
			<h2 className={style.title}>
				{getTranslatedProductName(product, language)}
			</h2>
			<div className={style.price}>
				{formatPrice(discountPrice ? discountPrice : price, currency)}
				{discountPrice && (
					<span className={style.discount}>
						{formatPrice(price, currency)}
					</span>
				)}
			</div>
			<AvailableLable
				className={style.available}
				isAvailable={available}
			/>
			<ProductVariants
				className={style.color}
				title={t("color")}
				value={getTranslatedColorName(product, language)}
			>
				{colors.map(({ color }) => (
					<ValueBox
						key={color}
						value={color}
						isActive={color === color_value}
						color={color}
						onClick={onChangeColor}
					/>
				))}
			</ProductVariants>
			<div className={style.sizeArea}>
				<ProductVariants title={t("size")}>
					{sizes.map((size) => (
						<ValueBox
							key={size}
							isActive={size === product.size}
							value={size}
							title={size}
							onClick={onChangeSize}
						/>
					))}
				</ProductVariants>
				<Counter
					className={style.counter}
					value={qty}
					onChangeCounter={setCounter}
				/>
			</div>
			<MainButton
				className={style.add}
				title={t("add_to_basket")}
				onClick={handleAddToBasket}
			/>
			<MainButton
				className={style.buy}
				color="blue"
				title={t("buy_now")}
				onClick={handleClickBuyNow}
			/>
		</div>
	);
};
