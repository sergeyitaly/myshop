import { PageContainer } from '../../components/containers/PageContainer'
import styles from './ThankPage.module.scss'
import img from '../../assets/thank picture.svg'
import { Link } from 'react-router-dom'
import { ROUTE } from '../../constants'

export const ThankPage = () => {
    return (
        <main>
            <section>
                <PageContainer className={styles.wrapper}>
                    <div className={styles.container}>
                        <h1 className={styles.title}>Дякуємо!</h1>
                        <p className={styles.p}>
                            Дякуємо що завітали в наш онлайн магазин. Незабаром ви отримаєте повідомлення про статус вашого замовлення на електронну пошту!
                        </p>
                        <img className={styles.image} src={img} alt="Woman in computer giving heart-shaped present to man" />
                        <p className={styles.check}>Перевірте свою електронну пошту!</p>
                        <p className={styles.text}>
                            Якщо ви не отримали жодного листа зв‘яжіться з 
                            <span className={styles.email}> KOLORYT@gmail.com</span>
                        </p>
                        <Link
                            to={ROUTE.HOME}
                            className={styles.link}
                        >
                            На головну
                        </Link>
                    </div>
                </PageContainer>
            </section>
        </main>
    )
}