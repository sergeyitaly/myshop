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
							to="https://play.google.com/store/apps/details?id=com.koloryt"
							target="_blank"
							rel="noopener noreferrer"
							>
							<svg
								xmlns="http://www.w3.org/2000/svg"
								viewBox="0 0 512 512"
								className={styles.icon}
							>
								<path fill="#0F9D58" d="M325.3 234.3L104.6 13l280.8 161.2-60.1 60.1z" />
								<path fill="#4285F4" d="M47 0C34 6.8 25.3 19.2 25.3 35.3v441.3c0 16.1 8.7 28.5 21.7 35.3l256.6-256L47 0z" />
								<path fill="#FBBC04" d="M425.2 225.6l-58.9-34.1-65.7 64.5 65.7 64.5 60.1-34.1c18-14.3 18-46.5-1.2-60.8z" />
								<path fill="#EA4335" d="M104.6 499l280.8-161.2-60.1-60.1L104.6 499z" />
							</svg>
							Google Play
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