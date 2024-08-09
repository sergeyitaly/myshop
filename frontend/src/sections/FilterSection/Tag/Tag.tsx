import { IconButton } from "../../../components/UI/IconButton/IconButton"
import styles from './Tag.module.scss'


interface TagProps {
    title: string
    onClickClose: () => void
}

export const Tag = ({
    title,
    onClickClose
}: TagProps) => {
    return (
        <div className={styles.tag}>
            <span>{title}</span>
            <IconButton 
                iconName="cross"
                onClick={onClickClose}
            />
        </div>
    )
}