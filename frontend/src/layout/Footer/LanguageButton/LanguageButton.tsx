import clsx from 'clsx'
import { AppIcon } from '../../../components/SvgIconComponents/AppIcon'
import { Language } from '../LanguageDropDown/LanguageDropDown'
import styles from './LanguageButton.module.scss'

interface LanguageButtonProps {
    className?: string
    language: Language
    onClick?: (lang: string) => void
}

export const LanguageButton = ({
    className,
    language,
    onClick
}: LanguageButtonProps) => {

    const {icon, lang,  title} = language
    
    const handleClick = () => {
        onClick && onClick(lang)
    }

    return (
        <button
            className={clsx(styles.button, className)}
            onClick={handleClick}
        >
            <AppIcon 
                className={styles.flag}
                iconName={icon}
            />
            <span>{title}</span>
        </button>
    )
}