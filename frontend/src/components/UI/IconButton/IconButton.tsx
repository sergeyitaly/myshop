import { DetailedHTMLProps } from 'react'
import { AppIcon } from '../../SvgIconComponents/AppIcon'
import styles from './IconButton.module.scss'
import clsx from 'clsx'
import { AppIconNames } from '../../../constants'
import { Badge } from '../Badge/Badge'

interface IconButtonProps extends DetailedHTMLProps<React.ButtonHTMLAttributes<HTMLButtonElement>, HTMLButtonElement> {
    iconName: AppIconNames
    badgeValue?: number
}


export const IconButton = ({
    iconName,
    badgeValue,
    className,
    ...props
}: IconButtonProps) => {
    return (
        <button className={clsx(styles.button, className)} {...props}>
            <AppIcon iconName={iconName}/>
            {
                !!badgeValue &&
                <Badge
                    className={styles.badge}
                    value={badgeValue}
                />
            }
        </button>
    )
}