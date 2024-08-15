import { BestSellersSection } from '../../sections/BestSellersSection/BestSellersSection'
import { FilterSection } from '../../sections/FilterSection/FilterSection'
import styles from './FilterPage.module.scss'


export const FilterPage = () => {
    return (
        <main className={styles.main}>
            <FilterSection/>
            <BestSellersSection/>
        </main>
    )
}