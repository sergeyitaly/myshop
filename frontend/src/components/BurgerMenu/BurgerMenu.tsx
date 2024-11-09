import { useRef, useState } from "react";
import { Link } from "react-router-dom";
import useBlockScroll from "../../hooks/useBlockScroll";
import useClickOutside from "../../hooks/useClickOutside";
import { useTranslation } from "react-i18next";
import styles from "./BurgerMenu.module.scss";

export const BurgerMenu = () => {
	const { t } = useTranslation();

	const [isOpen, setIsOpen] = useState<boolean>(false);
	const ref = useRef<HTMLDivElement>(null);

	useBlockScroll(isOpen);
	useClickOutside(ref, () => setIsOpen(false));

	const links = [
		{ name: t("collections"), href: "/collections" },
		{ name: t("new_arrivals"), href: "/new-arrivals" },
		{ name: t("all_collections"), href: "/all-collections" },
		{ name: t("discounts"), href: "/discounts" },
		{ name: t("about_us"), href: "/about" },
		{ name: t("contacts"), href: "/contacts" },
	];

	return (
		<div className={styles.burger_container}>
			<button
				className={[styles.burger, isOpen && styles.button_open].join(
					" "
				)}
				onClick={() => setIsOpen((prev) => !prev)}
			>
				<div className={styles.bar1}></div>
				<div className={styles.bar2}></div>
				<div className={styles.bar3}></div>
			</button>

			<nav
				ref={ref}
				className={[styles.menu, isOpen && styles.menu_open].join(" ")}
			>
				<div className={styles.logo_container}>
					<button
						className={[
							styles.burger,
							isOpen && styles.button_open,
						].join(" ")}
						onClick={() => setIsOpen((prev) => !prev)}
					>
						<div className={styles.bar1}></div>
						<div className={styles.bar2}></div>
						<div className={styles.bar3}></div>
					</button>
				</div>

				{links.map(({ href, name }) => (
					<Link
						key={name}
						className={styles.link}
						to={href}
						onClick={() => setIsOpen(false)}
					>
						{name}
					</Link>
				))}
			</nav>
		</div>
	);
};
