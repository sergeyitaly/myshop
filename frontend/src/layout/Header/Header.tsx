import { BurgerMenu } from "../../components/BurgerMenu/BurgerMenu";
import { Logo } from "../../components/Logo/Logo";
import { Navigation } from "../../components/Navigation/Navigation";
import { useBasket } from "../../hooks/useBasket";
import { IconButton } from "../../components/UI/IconButton/IconButton";
import { PageContainer } from "../../components/containers/PageContainer";
import { SearchWindow } from "../../components/SearchWindow/SearchWindow";
import { useSearch } from "../../hooks/useSearch";
import { useLocation, useNavigate } from "react-router-dom";
import { ROUTE } from "../../constants";
import { Product } from "../../models/entities";
import { AnimatePresence } from "framer-motion";
import clsx from "clsx";
import styles from "./Header.module.scss";

interface HeaderProps {
	basketLoadingStatus: boolean;
}

export const Header = ({ basketLoadingStatus }: HeaderProps) => {
	const { openBasket, productQty } = useBasket();

	const {
		open,
		value,
		debounceValue,
		toggleSearchBar,
		handleChange,
		closeSearchBar,
	} = useSearch();
	const navigate = useNavigate();
	const location = useLocation(); 
	const headerClassName =
		location.pathname === "/sendcontacts"
			? `${styles.header} ${styles.noBorder}`
			: styles.header;

	const handleClickProduct = (product: Product) => {
		navigate(`${ROUTE.PRODUCT}${product.id_name}`);
		closeSearchBar();
	};
	

	return (
		<header
			className={clsx(headerClassName, {
				[styles.noLine]: location.pathname === "/thank" || location.pathname ==="/thank_for_feedback",
			})}
		>
			<PageContainer className={styles.container}>
				<BurgerMenu />
				<Logo className={styles.logo} />
				<Navigation />
				<div className={styles.control}>
					<IconButton
						className={styles.headerButton}
						iconName="search"
						onClick={toggleSearchBar}
					/>
					<IconButton
						disabled={basketLoadingStatus}
						className={styles.headerButton}
						iconName="cart"
						badgeValue={productQty}
						onClick={openBasket}
					/>
				</div>
			</PageContainer>
			<AnimatePresence>
				{open && (
					<SearchWindow
						value={value}
						queryText={debounceValue}
						onChange={handleChange}
						onClickClose={closeSearchBar}
						onClickProduct={handleClickProduct}
					/>
				)}
			</AnimatePresence>
		</header>
	);
};

export default Header;
