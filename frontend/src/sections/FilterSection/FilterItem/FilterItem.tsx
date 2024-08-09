import ArrowForwardIos from "@mui/icons-material/ArrowForwardIos"
import styles from './FilterItem.module.scss'
import clsx from "clsx"
import { ButtonHTMLAttributes, DetailedHTMLProps } from "react"


interface FilterItemProps extends DetailedHTMLProps<ButtonHTMLAttributes<HTMLButtonElement>, HTMLButtonElement>{
    title: string
    isActive?: boolean
}

export const FilterItem = ({
    title,
    isActive,
    ...props
}: FilterItemProps) => {
    return (
      <button 
        {...props}
        className={clsx(styles.container, props.className, {
        [styles.active]: isActive
      })}>
        <span className={styles.title}>{title}</span>
        <ArrowForwardIos className={styles.icon}/>
      </button>  
    )
}