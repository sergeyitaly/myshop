import { useEffect, useState } from 'react'
import { Skeleton } from '../Skeleton/Skeleton'
import clsx from 'clsx'
import style from './AppImage.module.scss'


interface AppImageProps {
    className?: string
    src: string
    alt: string
}

export const AppImage = ({
    alt,
    src,
    className
}: AppImageProps) => {

    const [isLoading, setIsLoading] = useState<boolean>(true)

    useEffect(() => {
        const img = new Image()
        img.src = src
        img.onload = () => {
            setIsLoading(false)
        }
    }, [src]) 

    console.log(className);
    

    return (
        <div className={style.container}>
            <div className={clsx(style.imgWrapper, className)}>
                {
                    isLoading ?
                    <Skeleton
                        className={style.skeleton}
                    />
                    :
                    <img
                        src={src}
                        alt={alt}
                        loading="lazy"
                    />
                }
            </div>
        </div>
    )
}