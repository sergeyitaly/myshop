import { PageContainer } from '../../../components/containers/PageContainer';
import styles from './style.module.scss';
import img from '../../../assets/thank picture.svg';
import { Link } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import {ROUTE} from "../../../constants";

export const ThankYouPage = () => {
    const { t } = useTranslation();

    return (
        <main>
            <section>
                <PageContainer className={styles.wrapper}>
                    <div className={styles.container}>
                        <h1 className={styles.title}>{t('thank_you')}</h1>
                        <p className={styles.p}>
                            <div>{t('thank_you_text_part1')}<br/></div>
                            <div>{t('thank_you_text_part2')}<br/></div>
                            <div>{t('thank_you_text_part2.1')}</div>

                        </p>
                        <img className={styles.image} src={img} alt={t('thank_you_image_alt')} />
                        <p className={styles.p}>
                            {t('thank_you_text_part3')}
                        </p>
                        <Link
                            to={ROUTE.HOME}
                            className={styles.link}
                        >
                            {t('go_home')}
                        </Link>
                    </div>
                </PageContainer>
            </section>
        </main>
    );
}
