import { PageContainer } from "../../components/containers/PageContainer"
import { useAppTranslator } from "../../hooks/useAppTranslator"
import img from "../../assets/thank picture.svg";
import styles from './ThankFeedbackPage.module.scss'
import { Link } from "react-router-dom";
import { ROUTE } from "../../constants";

export const ThankFeedbackPage = () => {

    const {t} = useAppTranslator()

    return (
        <main>
			<section>
				<PageContainer className={styles.wrapper}>
					<div className={styles.container}>
						<h1 className={styles.title}>{t("thank_you")}</h1>{" "}
						<p className={styles.p}>{t("thank_you_for_feedback_message")}</p>
						<img
							className={styles.image}
							src={img}
							alt={t("thank_you_image_alt")}
						/>{" "}
						<p className={styles.text}>
							{t("contact_us")}
							<span className={styles.email}>
								{" "}
								<a href="mailto:koloryt@gmail.com">
									koloryt@gmail.com
								</a>
							</span>
						</p>
						<Link to={ROUTE.HOME} className={styles.link}>
							{t("go_home")} 
						</Link>
					</div>
				</PageContainer>
			</section>
		</main>
    )
}