import { useEffect, useRef } from "react";
import { useBasket } from "../../hooks/useBasket";
import useClickOutside from "../../hooks/useClickOutside";
import { MainButton } from "../UI/MainButton/MainButton";
import { AppIcon } from "../SvgIconComponents/AppIcon";
import { EmptyBasket } from "./components/EmptyBasket/EmptyBasket";
import clsx from "clsx";
import { useNavigate } from "react-router-dom";
import { ROUTE } from "../../constants";
import { formatNumber } from "../../functions/formatNumber";
import { BasketItem } from "../Cards/BasketItem/BasketItem";
import { AnimatePresence, motion } from "framer-motion";
import { box, item, modal } from "./motion.setings";
import { Product } from "../../models/entities";
import { useTranslation } from "react-i18next";
import styles from "./Basket.module.scss";

export const Basket = (): JSX.Element => {
	const { t } = useTranslation();
	const navigate = useNavigate();

	const {
		openStatus,
		basketItems,
		totalPrice,
		isEmptyBasket,
		productQty,
		closeBasket,
		deleteFromBasket,
		changeCounter,
	} = useBasket();

	const basketBox = useRef<HTMLDivElement | null>(null);

	useClickOutside(basketBox, closeBasket);

	useEffect(() => {
		document.body.style.overflow = openStatus ? "hidden" : "visible";

		return () => {
			document.body.style.overflow = "visible";
		};
	}, [openStatus]);

	const handleClickBlueButton = () => {
		closeBasket();
		if (isEmptyBasket) {
			return navigate(ROUTE.HOME);
		}
		navigate(ROUTE.ORDER);
	};

	const handleClickName = (product: Product) => {
		navigate(`${ROUTE.PRODUCT}${product.id_name}`);
		closeBasket();
	};

	return (
		<AnimatePresence>
			{openStatus && (
				<motion.div
					className={styles.container}
					variants={modal}
					initial="hidden"
					animate="visible"
					exit="hidden"
				>
					<motion.div
						ref={basketBox}
						className={styles.box}
						variants={box}
					>
						<header
							className={clsx(styles.header, {
								[styles.endline]: isEmptyBasket,
							})}
						>
							<h4 className={styles.titleContainer}>
								<span className={styles.title}>
									{t("basket_title")}
								</span>
								<span
									className={styles.counter}
								>{`(${productQty})`}</span>
							</h4>
							<button onClick={closeBasket}>
								<AppIcon iconName="cross" />
							</button>
						</header>

						<div
							className={clsx(styles.content, {
								[styles.center]: isEmptyBasket,
							})}
						>
							{!isEmptyBasket ? (
								basketItems.map((basketItem) => {
									const { product, qty, productId } =
										basketItem;
									return (
										product && (
											<motion.div
												key={productId}
												variants={item}
												layout
											>
												<BasketItem
													product={product}
													qty={qty}
													stock={product.stock}
													color={{
														color:
															product.color_value ||
															"",
														name:
															product.color_name ||
															"",
													}}
													size={product.size || ""}
													onClickDelete={
														deleteFromBasket
													}
													onClickName={
														handleClickName
													}
													onChangeCounter={
														changeCounter
													}
													onClickPhoto={
														handleClickName
													}
												/>
											</motion.div>
										)
									);
								})
							) : (
								<EmptyBasket />
							)}
						</div>

						{!isEmptyBasket && (
							<div className={styles.totalPrice}>
								<span>{t("total_price")}</span>
								<span>
									{formatNumber(totalPrice)} {t("currency")}
								</span>
							</div>
						)}

						<div className={styles.actions}>
							<MainButton
								title={
									isEmptyBasket
										? t("return_to_home")
										: t("proceed_to_checkout")
								}
								color="blue"
								onClick={handleClickBlueButton}
							/>
							<MainButton
								title={t("continue_shopping")}
								onClick={closeBasket}
								className={clsx(styles.noBorder)}
							/>
						</div>
					</motion.div>
				</motion.div>
			)}
		</AnimatePresence>
	);
};
