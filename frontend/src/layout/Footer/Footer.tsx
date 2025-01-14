import { Link } from "react-router-dom";
import { Logo } from "../../components/Logo/Logo";
import { useTranslation } from "react-i18next";
import { LanguageDropDown } from "./LanguageDropDown/LanguageDropDown";
import { PageContainer } from "../../components/containers/PageContainer";
import VisaImg from "./visa.svg";
import styles from "./Footer.module.scss";

export const Footer = () => {
	const { t } = useTranslation();

	return (
		<footer className={styles.footer}>
			<PageContainer>
				<Logo className={styles.logo} type="short" />
				<div className={styles.content}>
					<nav className={styles.nav}>
						<p className={styles.title}>{t("contact_us")}</p>{" "}
						<Link className={styles.link} to="/contacts">
							{t("contacts")}
						</Link>
						<Link
							className={styles.link}
							to="https://www.instagram.com/"
							target="_blank"
							rel="noopener noreferrer"
						>
							Instagram
						</Link>
						<Link
							className={styles.link}
							to="https://www.facebook.com/"
							target="_blank"
							rel="noopener noreferrer"
						>
							Facebook
						</Link>
					</nav>
					<nav className={styles.nav}>
						<p className={styles.title}>{t("info")}</p>{" "}
						<Link className={styles.link} to="/about">
							{t("about_us")}
						</Link>
						<Link className={styles.link} to="/payment_delivery">
							{t("payment_delivery")}
						</Link>
						<Link className={styles.link} to="/returns_refunds">
							{t("returns_refunds")}
						</Link>
					</nav>
					<nav className={styles.nav}>
						<p>
							2024 <span className={styles.koloryt}>KOLORYT</span>
						</p>
						<Link className={styles.link} to="/privacy_policy">
							{t("privacy_policy")}
						</Link>
						<p className={styles.payment}>
							{t("payment.label")}:
							<img src={VisaImg} alt="visa icon" />
						</p>
						<LanguageDropDown />
					</nav>
				</div>
			</PageContainer>
		</footer>
	);
};
