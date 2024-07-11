import { AppIcon } from '../../SvgIconComponents/AppIcon'
import styles from './SearchInput.module.scss'

interface SearchInputProps {
    id: string
}

export const SearchInput = ({
    id
}: SearchInputProps) => {
    return (
        <div className={styles.container}>
            <label 
                htmlFor={id}
                className={styles.sign}
            >
                <AppIcon iconName='search'/>
            </label>
            <input 
                id={id}
                autoComplete='off'
                className={styles.input}
                type="text" 
            />
            <button>
                <AppIcon iconName='cross'/>
            </button>
            <span className={styles.underline}/>
        </div>
    )
}