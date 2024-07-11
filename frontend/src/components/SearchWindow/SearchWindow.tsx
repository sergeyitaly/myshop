import { SearchInput } from './SearchInput/SearchInput'
import styles from './SearchWindow.module.scss'

export const SearchWindow = () => {
    return (
        <div className={styles.container}>
            <SearchInput id='search'/>
        </div>
    )
}