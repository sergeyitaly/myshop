import { Product } from "../../../models/entities";
import { Counter } from "../../Counter/Counter";
import { formatPrice } from "../../../functions/formatPrice";
import { AppImage } from "../../AppImage/AppImage";
import { Plug } from "../../Plug/Plug";
import { countDiscountPrice } from "../../../functions/countDiscountPrice";
import { useTranslation } from "react-i18next";
import { useAppTranslator } from "../../../hooks/useAppTranslator";
import styles from "./OrderItemCard.module.scss";

interface OrderItemCardProps {
	product: Product;
	qty: number;
	stock: number;
	language: string;
	onClickDelete?: (product: Product) => void;
	onChangeCounter?: (value: number) => void;
	onClickName?: (product: Product) => void;
	onClickPhoto?: (product: Product) => void;
}

export const OrderItemCard = ({
	product,
	qty,
	onClickDelete,
	onChangeCounter,
	onClickName,
	onClickPhoto,
}: OrderItemCardProps) => {
	const { t } = useTranslation();

	const { getTranslatedProductName } = useAppTranslator();

	const { photo, price, currency, photo_thumbnail_url } = product;

	const handleClickDelete = () => {
		onClickDelete && onClickDelete(product);
	};

	const handleClickName = () => {
		onClickName && onClickName(product);
	};

	const handleClickPhoto = () => {
		onClickPhoto && onClickPhoto(product);
	};

	const discountPrice = product
		? countDiscountPrice(product.price, product.discount)
		: null;

	return (
		<div className={styles.card}>
			<button className={styles.imageBox} onClick={handleClickPhoto}>
				<AppImage
					src={photo}
					previewSrc={photo_thumbnail_url}
					alt={getTranslatedProductName(product)}
				/>
				{discountPrice && <Plug className={styles.plug} />}
			</button>
			<div className={styles.info}>
				<div className={styles.title} onClick={handleClickName}>
					{getTranslatedProductName(product)}
				</div>
				<div>
					<p className={styles.price}>
						{formatPrice(price, currency)}
					</p>
					{discountPrice && (
						<p className={styles.discountPrice}>
							{formatPrice(discountPrice, currency)}
						</p>
					)}
				</div>

				<div className={styles.control}>
					<Counter
						className={styles.counter}
						value={qty}
						stock={product.stock}
						onChangeCounter={onChangeCounter}
					/>
					<button
						className={styles.deleteButton}
						onClick={handleClickDelete}
					>
						{t("delete")}
					</button>
				</div>
			</div>
		</div>
	);
};
