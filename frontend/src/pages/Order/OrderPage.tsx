import { PageContainer } from "../../components/PageContainer"
import { OrderPreview } from "./OrderPreview/OrderPreview"
import styles from './OrderPage.module.scss'
import { OrderForm } from "../../components/Forms/OrderForm/OrderForm"


export const OrderPage = () => {
    return (
        <main>
            <PageContainer>
                <h1 className={styles.title}>Оформити замовлення</h1>
                <section className={styles.orderSection}>
                    <OrderForm className={styles.formContainer}/>
                    <OrderPreview className={styles.preview}/>
                </section>
            </PageContainer>
        </main>
    )
}