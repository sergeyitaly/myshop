
import { useState } from 'react'
import ArrowForward from '@mui/icons-material/ArrowForwardIos'
import clsx from 'clsx'
import style from './DropDown.module.scss'

interface DropDownProps {
    title: string
    content?: string
    className?: string
}

export const DropDown = ({
    title,
    content,
    className
}: DropDownProps) => {

    const [active, setActive] = useState<boolean>(false)

    return (
        <div className={clsx(style.container, className)}>
            <button 
                className={style.head}
                onClick = {() => {setActive(!active)}} 
            >
                <span>{title}</span>
                <span className={clsx(style.arrow, {
                    [style.active]: active
                })}>
                    <ArrowForward />
                </span>
            </button>
            <div className={clsx(style.drop, {
                [style.active]: active
            })}>
                <p className={style.content}>

                    {content ? content : `Опис поки що відсутній`}
                </p>
            </div>
        </div>
    )
}