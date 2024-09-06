import React from "react";
import { Link } from "react-router-dom";
import { useTranslation } from "react-i18next";
import img1 from "./about_img1.png";
import img2 from "./about_img2.png";
import img3 from "./about_img3.png";
import styles from "../About/About.module.scss";

export const About: React.FC = () => {
	const { t } = useTranslation();
	const projectName = <span className={styles.blueText}>KOLORYT</span>;

	return (
		<section className={styles.wrapper}>
			<div className={styles.linkContainer}>
				<Link to="/about" className={styles.link}>
					{t("about_us")}
				</Link>
			</div>

			<div className={`${styles.container} ${styles.content1}`}>
				<img src={img1} alt="About" className={styles.img} />
				<div className={styles.text}>
					{projectName}
					{t("about_us_content")}
				</div>
			</div>

			<div className={`${styles.container} ${styles.content2}`}>
				<div className={styles.text}>
					{t("about_us_idea_part_1")}
					{projectName}
					{t("about_us_idea_part_2")}
				</div>
				<img src={img2} alt="About" className={styles.img} />
			</div>

			<div className={`${styles.container} ${styles.content3}`}>
				<img src={img3} alt="About" className={styles.img} />
				<div className={styles.text}>
					{t("about_us_culture_part_1")}
					{projectName}
					{t("about_us_culture_part_2")}
					{projectName}
					{t("about_us_culture_part_3")}
				</div>
			</div>
		</section>
	);
};
