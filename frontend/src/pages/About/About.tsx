import React from "react";
import { useTranslation } from "react-i18next";
import { TeamCarousel } from "./TeamCarousel/TeamCarousel";
import { TechnologiesCarousel } from "./TechnologiesCarousel/TechnologiesCarousel";
import { Brands } from "./Brands/Brands";
import { NamedSection } from "../../components/NamedSection/NamedSection";
import img1 from "../../assets/about/about_img1.svg";
import img2 from "../../assets/about/about_img2.svg";
import img3 from "../../assets/about/about_img3.svg";
import styles from "../About/About.module.scss";

export const About: React.FC = () => {
	const { t } = useTranslation();
	const projectName = <span className={styles.projectName}>KOLORYT</span>;

	return (
		<section>
			<div className={styles.wrapper}>
				<NamedSection title={t("about_us")}></NamedSection>

				<div className={styles.border} />

				<NamedSection title="">
					<div className={`${styles.container} ${styles.content1}`}>
						<img src={img1} alt="About" className={styles.img} />
						<div className={styles.text}>
							{projectName}
							{t("about_us_content")}
						</div>
					</div>
				</NamedSection>

				<div className={styles.border} />

				<div className={styles.border} />

				<NamedSection title="">
					<div className={`${styles.container} ${styles.content2}`}>
						<div className={styles.text}>
							{t("about_us_idea_part_1")}
							{projectName}
							{t("about_us_idea_part_2")}
						</div>
						<img src={img2} alt="About" className={styles.img} />
					</div>
				</NamedSection>

				<div className={styles.border} />

				<TeamCarousel />

				<TechnologiesCarousel />

				<div className={styles.border} />

				<NamedSection title="">
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
				</NamedSection>

				<div className={styles.border} />

				<Brands />
			</div>
		</section>
	);
};
