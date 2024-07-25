
import { useEffect, useState } from 'react'
import ArrowForward from '@mui/icons-material/ArrowForwardIos'
import clsx from 'clsx'
import style from './DropDown.module.scss'
import { splitText } from '../../../../functions/splitText'

interface DropDownProps {
    title: string
    content?: string
    className?: string
    changebleParam?: string | number
}

export const DropDown = ({
    title,
    content,
    className,
    changebleParam
}: DropDownProps) => {

    const [active, setActive] = useState<boolean>(false)

    useEffect(() => {
        setActive(false)
    }, [changebleParam])

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
                <div className={style.content}>

                    {content ? 
                        splitText(content).map((paragraph, i) => {
                            if(!paragraph) return <br key={i}/>
                            return <p key={i}>{paragraph}</p>
                        }
                    )
                     : 
                     <p>Опис поки що відсутній</p>
                    }
                </div>
            </div>
        </div>
    )
}