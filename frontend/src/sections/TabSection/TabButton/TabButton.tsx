
import clsx from 'clsx'
import styles from './TabButton.module.scss'
import { FilterConstantStates } from '../TabSection'

interface TabButtonProps  {
    activeState: string
    className?: string
    title: string
    name: FilterConstantStates
    onClick: (name: FilterConstantStates) => void
}

export const TabButton = ({
    activeState,
    className,
    title,
    name,
    onClick
}: TabButtonProps) => {

    const handleClick = () => {
        onClick(name)
    }

    return (
        <button
            className={clsx(styles.button, className, {[styles.active]: activeState === name})}
            onClick={handleClick}
        >
            {title}
        </button>
    )
}