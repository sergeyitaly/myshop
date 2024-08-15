import ArrowForwardIos from "@mui/icons-material/ArrowForwardIos"
import styles from './FilterItem.module.scss'
import clsx from "clsx"
import { ButtonHTMLAttributes, DetailedHTMLProps } from "react"
import { useTranslation } from 'react-i18next'; // Import the hook


interface FilterItemProps extends DetailedHTMLProps<ButtonHTMLAttributes<HTMLButtonElement>, HTMLButtonElement>{
    title: string
    isActive?: boolean
}

export const FilterItem = ({
    title,
    isActive,
    ...props
}: FilterItemProps) => {
  const { t } = useTranslation(); // Use the translation hook

    return (
      <button 
        {...props}
        className={clsx(styles.container, props.className, {
        [styles.active]: isActive
      })}>
        <span className={styles.title}>{t(title)}</span>
        <ArrowForwardIos className={styles.icon}/>
      </button>  
    )
}