import { DetailedHTMLProps, InputHTMLAttributes } from 'react'
import { AppIcon } from '../../SvgIconComponents/AppIcon'
import styles from './SearchInput.module.scss'

interface SearchInputProps extends DetailedHTMLProps<InputHTMLAttributes<HTMLInputElement>, HTMLInputElement> {
    id: string
    onClickClose: () => void
}

export const SearchInput = ({
    id,
    onClickClose,
    ...props
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
                {...props}
            />
            <button onClick={onClickClose}>
                <AppIcon iconName='cross'/>
            </button>
            <span className={styles.underline}/>
        </div>
    )
}