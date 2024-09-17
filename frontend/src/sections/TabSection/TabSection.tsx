import { PageContainer } from "../../components/containers/PageContainer"
import { PopularProducts } from "./PopularProducts"
import { ProductsWithDiscount } from "./ProductsWithDiscount"
import { AllCollections } from "./AllCollections"
import { useState } from "react"
import { TabButton } from "./TabButton/TabButton"
import styles from './TabSection.module.scss'
import { useTranslation } from "react-i18next"

export type FilterConstantStates = 'popularity' | 'allCollections' | 'discount'

export const TabSection = () => {


    const [activeState, setActiveState] = useState<FilterConstantStates>('popularity')

    const {t} = useTranslation()

    return (
        <section className={styles.section}>
            <PageContainer>
                <div className={styles.tabContainer}>
                    <TabButton
                        className={styles.item}
                        activeState = {activeState}
                        title={t('popularProducts')}
                        name = "popularity"
                        onClick={setActiveState}
                    />
                    <TabButton
                        className={styles.item}
                        activeState={activeState}
                        title={t('all_collections')}
                        name = "allCollections"
                        onClick={setActiveState}
                    />
                    <TabButton
                        className={styles.item}
                        activeState={activeState}
                        title={t('discounts')}
                        name = "discount"
                        onClick={setActiveState}
                    />
                </div>
            </PageContainer>
            <PageContainer>
                {
                    activeState === 'popularity' && 
                        <PopularProducts/>
                }
                {
                    activeState === 'discount' && 
                        <ProductsWithDiscount/>
                }
                {
                    activeState === 'allCollections' && 
                
                        <AllCollections/>
                }
            </PageContainer>
        </section>
    )
}