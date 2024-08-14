import { ReactNode, useState } from "react"
import ArrowForwardIos from "@mui/icons-material/ArrowForwardIos"
import styles from './FilterDropDown.module.scss'
import clsx from "clsx"


interface FilterDropDownProps {
    title: string
    children: ReactNode
}

export const FilterDropDown = ({
    children,
    title
}: FilterDropDownProps) => {

    const [open, setOpen] = useState<boolean>(false)

    const handleClick = () => {
        setOpen(!open)
    }

    return (
        <div className={styles.container}>
            <button 
                className={styles.button}
                onClick={handleClick}
            >
                <span>{title}</span>
                <span className={clsx(styles.arrow,{[styles.active]: open})}>
                    <ArrowForwardIos/>
                </span>
            </button>
            {
                open &&
                <div className={styles.contentContainer}>{children}</div>
            }
        </div>
    )
}