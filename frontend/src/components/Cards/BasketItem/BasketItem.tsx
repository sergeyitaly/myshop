import { useTranslation } from "react-i18next";
import { useAppTranslator } from "../../../hooks/useAppTranslator";
import { countDiscountPrice } from "../../../functions/countDiscountPrice";
import { formatPrice } from "../../../functions/formatPrice";
import { Color, Product } from "../../../models/entities";
import { AppImage } from "../../AppImage/AppImage";
import { AvailableLable } from "../../AvailableLabel/AvailableLabel";
import { Counter } from "../../Counter/Counter";
import { Plug } from "../../Plug/Plug";
import { ProductVariants } from "../../ProductVariants/ProductVariants";
import { ValueBox } from "../../ProductVariants/ValueBox/ValueBox";
import { IconButton } from "../../UI/IconButton/IconButton";
import styles from "./BasketItem.module.scss";

interface BasketItemProps {
	product: Product;
	qty: number;
	color: Color;
	size: string;
	onClickDelete: (product: Product) => void;
	onClickName?: (product: Product) => void;
	onClickPhoto?: (product: Product) => void;
	onChangeCounter?: (product: Product, qty: number) => void;
}

export const BasketItem = ({
	product,
	color,
	size,
	qty,
	onClickDelete,
	onClickName,
	onClickPhoto,
	onChangeCounter,
}: BasketItemProps) => {
	const { t } = useTranslation();
	const { getTranslatedProductName, getTranslatedColorName } =
		useAppTranslator();

	const { photo, photo_thumbnail_url, available, price, currency, discount } =
		product;

	const handleClickDelete = () => {
		onClickDelete && onClickDelete(product);
	};

	const handleClickName = () => {
		onClickName && onClickName(product);
	};

	const handleClickPhoto = () => {
		onClickPhoto && onClickPhoto(product);
	};

	const handleChangeCounter = (value: number) => {
		onChangeCounter && onChangeCounter(product, value);
	};

	const discountPrice = product ? countDiscountPrice(price, discount) : null;

	return (
		<div className={styles.container}>
			<button className={styles.imgWrapper} onClick={handleClickPhoto}>
				<AppImage
					src={photo}
					previewSrc={photo_thumbnail_url}
					alt={getTranslatedProductName(product)}
				/>
				{discountPrice && <Plug className={styles.plug} />}
			</button>
			<div className={styles.info}>
				<div className={styles.header}>
					<h4 className={styles.title} onClick={handleClickName}>
						{getTranslatedProductName(product)}
					</h4>{" "}
					<IconButton
						className={styles.icon}
						iconName="delete"
						onClick={handleClickDelete}
					/>
				</div>
				<ProductVariants
					className={styles.characteristic}
					title={t("color")}
					value={getTranslatedColorName(product)}
				>
					<ValueBox
						className={styles.noPointer}
						value={color.color}
						color={color.color}
					/>
				</ProductVariants>
				<div className={styles.counterBox}>
					<ProductVariants
						className={styles.characteristic}
						title={t("size")}
					>
						<ValueBox
							className={styles.noPointer}
							key={size}
							value={size}
							title={size}
							isActive
						/>
					</ProductVariants>
					<Counter
						className={styles.selfTop}
						value={qty}
						onChangeCounter={handleChangeCounter}
					/>
				</div>
				<AvailableLable isAvailable={available} />
				<div className={styles.control}>
					<p>{formatPrice(price, currency)}</p>
					{discountPrice && (
						<p className={styles.discountPrice}>
							{formatPrice(discountPrice, currency)}
						</p>
					)}
				</div>
			</div>
		</div>
	);
};
