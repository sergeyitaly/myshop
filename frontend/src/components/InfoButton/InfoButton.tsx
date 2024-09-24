import clsx from 'clsx'
import styles from './InfoButton.module.scss'

interface InfoButtonProps {
    className?: string
    onClick: () => void
}

export const InfoButton = ({
    className,
    onClick
}: InfoButtonProps) => {



    return (
        <button 
            className={clsx(styles.button, className)}
            onClick={onClick}
        >
            Оцінити сайт
        </button>
    )
}