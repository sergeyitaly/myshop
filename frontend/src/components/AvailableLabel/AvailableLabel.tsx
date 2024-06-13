
import clsx from 'clsx'
import style from './AvailableLable.module.scss'


interface AvailableLableProps {
    isAvailable: boolean
    className?: string
}

export const AvailableLable = ({
    isAvailable,
    className
}: AvailableLableProps) => {



    return (
        <div className={clsx( style.label, {[style.available]: isAvailable}, className )}>
                {
                    isAvailable ? 'в наявності' : 'відсутній'
                }
        </div>
    )
}