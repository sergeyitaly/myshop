import { PageContainer } from "../../components/containers/PageContainer";
import img from "../../assets/thank picture.svg";
import { Link } from "react-router-dom";
import { ROUTE } from "../../constants";
import { useMediaQuery } from "react-responsive";
import QRCode from "qrcode.react";
import { FaTelegramPlane } from "react-icons/fa";
import { useTranslation } from "react-i18next";
import styles from "./ThankPage.module.scss";

export const ThankPage = () => {
	const { t } = useTranslation();
	const isLaptop = useMediaQuery({ query: "(min-width: 1024px)" });
	const telegramLink = "https://t.me/KOLORYT_notifications_bot";

	return (
		<main>
			<section>
				<PageContainer className={styles.wrapper}>
					<div className={styles.container}>
						<h1 className={styles.title}>{t("thank_you")}</h1>{" "}
						<p className={styles.p}>{t("thank_you_message")}</p>
						<img
							className={styles.image}
							src={img}
							alt={t("thank_you_image_alt")}
						/>{" "}
						<p className={styles.check}>{t("check_email")}</p>{" "}
						<p className={styles.text}>
							{t("contact_us")}
							<span className={styles.email}>
								{" "}
								{t("emailKOLORYT")}
							</span>
						</p>
						<div className={styles.telegramContainer}>
							<FaTelegramPlane
								size={24}
								// className={styles.telegramIcon}
							/>
							<p>
								<a
									href={telegramLink}
									target="_blank"
									rel="noopener noreferrer"
								>
									<span
										className={
											styles.KOLORYT_notifications_bot
										}
									>
										{t("telegram_bot")}
									</span>
								</a>
							</p>
						</div>
						{isLaptop && (
							<div className={styles.qrCode}>
								<p>{t("scan_qr_code")}</p>
								<br />
								<QRCode value={telegramLink} size={128} />
							</div>
						)}
						<Link to={ROUTE.HOME} className={styles.link}>
							{t("go_home")} {/* Localization */}
						</Link>
					</div>
				</PageContainer>
			</section>
		</main>
	);
};
