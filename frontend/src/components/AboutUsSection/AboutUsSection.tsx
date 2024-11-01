import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { useTranslation } from "react-i18next";
import i18next from "i18next";
import vase from "./vase.svg";
import styles from "./AboutUsSection.module.scss";

export const AboutUsSection = () => {
	const { t } = useTranslation();
	const [width, setWidth] = useState(window.innerWidth);
	useEffect(() => {}, [i18next.language]);

	useEffect(() => {
		const handleResize = () => {
			setWidth(window.innerWidth);
		};

		window.addEventListener("resize", handleResize);

		return () => {
			window.removeEventListener("resize", handleResize);
		};
	}, []);

	let content = t("about_us_content");

	if (width < 741) {
		content = content.slice(0, 158);
	}

	return (
		<section className={styles.section}>
			<div className={styles.content}>
				<img src={vase} alt="vase" className={styles.vase} />
				<span className={styles.blue}>KOLORYT</span>
				{content}
			</div>
			<Link to="/about" className={styles.link}>
				{t("more_about_us")}
			</Link>
		</section>
	);
};
