import { ButtonHTMLAttributes, DetailedHTMLProps } from 'react'
import { AppIcon } from '../../../../components/SvgIconComponents/AppIcon'
import styles from './HeaderIconButton.module.scss'
import clsx from 'clsx'

interface HeaderButtonProps extends DetailedHTMLProps<ButtonHTMLAttributes<HTMLButtonElement>, HTMLButtonElement>{
    className?: string
}

export const HeaderIconButton = ({
    className,
    ...props
}: HeaderButtonProps) => {
    return (
        <button className={clsx(styles.button, className) } {...props}>
            <AppIcon iconName='cart'/>
        </button>
    )
}