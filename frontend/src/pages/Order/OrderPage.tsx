import { PageContainer } from "../../components/containers/PageContainer"
import { OrderPreview } from "./OrderPreview/OrderPreview"
import styles from './OrderPage.module.scss'
import { OrderForm } from "../../components/Forms/OrderForm/OrderForm"
import {useTranslation} from "react-i18next";



export const OrderPage = () => {

    const { t } = useTranslation();

    return (
        <main>
            <PageContainer>
                <h1 className={styles.title}>{t('order_place')}</h1>
                <section className={styles.orderSection}>
                    <OrderForm className={styles.formContainer}/>
                    <OrderPreview className={styles.preview}/>
                </section>
            </PageContainer>
        </main>
    )
}