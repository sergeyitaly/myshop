import { PageContainer } from "../../components/containers/PageContainer"
import { PopularProducts } from "./PopularProducts"
import { ProductsWithDiscount } from "./ProductsWithDiscount"
import { AllCollections } from "./AllCollections"
import { useState } from "react"
import { TabButton } from "./TabButton/TabButton"
import styles from './TabSection.module.scss'

export type FilterConstantStates = 'popularity' | 'allCollections' | 'discount'

export const TabSection = () => {


    const [activeState, setActiveState] = useState<FilterConstantStates>('popularity')

    return (
        <section>
            <PageContainer className={styles.tabContainer}>
                    <TabButton
                        activeState = {activeState}
                        title="Найпопулярніші товари"
                        name = "popularity"
                        onClick={setActiveState}
                    />
                    <TabButton
                        activeState={activeState}
                        title="Всі колекції"
                        name = "allCollections"
                        onClick={setActiveState}
                    />
                    <TabButton
                        activeState={activeState}
                        title="Знижки"
                        name = "discount"
                        onClick={setActiveState}
                    />
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