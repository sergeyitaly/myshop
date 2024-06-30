import { PageContainer } from "../../components/PageContainer"
import styles from './OrderPage.module.scss'



export const OrderPage = () => {

    

    return (
        <main>
            <PageContainer>
                <h1 className={styles.title}>Оформити замовлення</h1>
                <section className={styles.orderSection}>
                    <div>Order page</div>
                </section>
            </PageContainer>
        </main>
    )
}