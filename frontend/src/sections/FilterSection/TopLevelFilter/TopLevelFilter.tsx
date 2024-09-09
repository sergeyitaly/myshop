import clsx from "clsx"
import { MouseEvent } from "react"
import styles from './TopLevelFilter.module.scss' 

interface TopLevelFilterProps {
    isActive: boolean
    title: string
    onClick: (event: MouseEvent<HTMLButtonElement>) => void
}

export const TopLevelFilter = ({
    isActive,
    title,
    onClick
}: TopLevelFilterProps) => {

    

    return (
        <button
            className={clsx(styles.button, {[styles.active]: isActive})}
            onClick={onClick}
        >
            {title}
        </button>
    )
}