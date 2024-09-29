import clsx from 'clsx'
import styles from './InfoButton.module.scss'
import { useAppTranslator } from '../../hooks/useAppTranslator'

interface InfoButtonProps {
    className?: string
    onClick: () => void
}

export const InfoButton = ({
    className,
    onClick
}: InfoButtonProps) => {

    const {t} =useAppTranslator()


    return (
        <button 
            className={clsx(styles.button, className)}
            onClick={onClick}
        >
            {t('rate_us')}
        </button>
    )
}