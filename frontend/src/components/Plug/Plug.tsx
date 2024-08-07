import clsx from 'clsx'
import style from './Plug.module.scss'

interface PlugProps {
    className?: string
    title?: string
}

export const Plug = ({
    title = 'Sale',
    className
}: PlugProps) => {
    return (
        <div className={clsx(style.plug, className)}>
           {title}
        </div>
    )
}