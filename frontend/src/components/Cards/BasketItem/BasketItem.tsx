import { useTranslation } from "react-i18next";
import { useAppTranslator } from "../../../hooks/useAppTranslator";
import { countDiscountPrice } from "../../../functions/countDiscountPrice";
import { formatPrice } from "../../../functions/formatPrice";
import { Color, Product } from "../../../models/entities";
import { AppImage } from "../../AppImage/AppImage";
import { Counter } from "../../Counter/Counter";
import { Plug } from "../../Plug/Plug";
import { ProductVariants } from "../../ProductVariants/ProductVariants";
import { IconButton } from "../../UI/IconButton/IconButton";
import styles from "./BasketItem.module.scss";

interface BasketItemProps {
	product: Product;
	qty: number;
	color: Color;
	size: string;
	stock: number;
	onClickDelete: (product: Product) => void;
	onClickName?: (product: Product) => void;
	onClickPhoto?: (product: Product) => void;
	onChangeCounter?: (product: Product, qty: number) => void;
}

export const BasketItem = ({
	product,
	size,
	qty,
	stock,
	onClickDelete,
	onClickName,
	onClickPhoto,
	onChangeCounter,
}: BasketItemProps) => {
	const { t } = useTranslation();
	const { getTranslatedProductName, getTranslatedColorName } =
		useAppTranslator();

	const { photo, photo_thumbnail_url, price, currency, discount } =
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
			<div className={styles.info} style={{justifyContent:"justifyContent"}}>
				<div className={styles.header}>
					<h4 className={styles.title} onClick={handleClickName} style={{fontSize:"17px", marginBottom:'7px',
						width:"90%"}}>
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
				</ProductVariants>

				<div className={styles.counterBox}>
					<div>
						<div className={styles.sizeLabel}>{t("size")}:&nbsp;</div>
						<span>{size}</span>
					</div>
						<div style={{ fontSize: '0.75rem' }}>
							<Counter
								className={styles.selfTop}
								value={qty}
								stock={stock}
								onChangeCounter={handleChangeCounter}
							/>
						</div>
				</div>
				<div className={styles.control}>
					
					{discountPrice ? (
						<>
							<p className={styles.discountPrice}>
								{formatPrice(price, currency)}
							</p>
							<p>{formatPrice(discountPrice, currency)}</p>
						</>
					)
					:
					<p>{formatPrice(price, currency)}</p>
				}
				</div>
			</div>
		</div>
	);
};