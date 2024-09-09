import { PageContainer } from '../../../components/containers/PageContainer';
import styles from './style.module.scss';
import img from '../../../assets/thank picture.svg';
import { Link } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import {ROUTE} from "../../../constants"; // Import useTranslation

export const ThankYouPage = () => {
    const { t } = useTranslation(); // Use useTranslation hook

    return (
        <main>
            <section>
                <PageContainer className={styles.wrapper}>
                    <div className={styles.container}>
                        <h1 className={styles.title}>Дякуємо!</h1> {/* Localization */}
                        <p className={styles.p}>
                            Ваш запит було успішно надіслано, і ми скоро зв'яжемося з вами. Зазвичай ми відповідаємо
                            протягом 24 годин. Дякуємо, що обрали нас!
                        </p>
                        <img className={styles.image} src={img} alt={t('thank_you_image_alt')} /> {/* Localization */}
                        <p className={styles.p}>
                            Ми завжди раді допомогти!
                        </p>
                        {/*<p className={styles.check}>{t('check_email')}</p> /!* Localization *!/*/}
                        {/*<p className={styles.text}>*/}
                        {/*    {t('contact_us')} */}
                        {/*    <span className={styles.email}> {t('emailKOLORYT')}</span>*/}
                        {/*</p>*/}
                        {/*<div className={styles.telegramContainer}>*/}
                        {/*    <FaTelegramPlane size={24}*/}
                        {/*                     // className={styles.telegramIcon}*/}
                        {/*    />*/}
                        {/*    <p>*/}
                        {/*        <a href={telegramLink} target="_blank" rel="noopener noreferrer">*/}
                        {/*            <span className={styles.KOLORYT_notifications_bot}>{t('telegram_bot')}</span>*/}
                        {/*        </a>*/}
                        {/*    </p>*/}
                        {/*</div>*/}
                        {/*{isLaptop && (*/}
                        {/*    <div className={styles.qrCode}>*/}
                        {/*        <p>{t('scan_qr_code')}</p>*/}
                        {/*        <br/>*/}
                        {/*        <QRCode value={telegramLink} size={128} />*/}
                        {/*    </div>*/}
                        {/*)}*/}
                        <Link
                            to={ROUTE.HOME}
                            className={styles.link}
                        >
                            {t('go_home')} {/* Localization */}
                        </Link>
                    </div>
                </PageContainer>
            </section>
        </main>
    );
}
