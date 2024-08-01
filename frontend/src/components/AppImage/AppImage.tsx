import { useEffect, useState } from 'react'
import clsx from 'clsx'
import style from './AppImage.module.scss'
import {motion} from 'framer-motion'
import defaultPhoto from '../../assets/default.png'
import { transformURL } from '../../functions/transformURL'


interface AppImageProps {
    className?: string
    src: string | null
    previewSrc?: string | null
    alt: string
}

export const AppImage = ({
    alt,
    src,
    previewSrc,
    className
}: AppImageProps) => {

    const [isLoading, setIsLoading] = useState<boolean>(true)

    useEffect(() => {
        const img = new Image()
        img.src =  src ? transformURL(src) : defaultPhoto
        img.onload = () => {
            setIsLoading(false)
        }
    }, [src]) 


    return (
            <div className={clsx(style.imgWrapper, className)}>
                {
                    isLoading ?
                    previewSrc ?
                    <motion.img
                        initial= {{
                            opacity: 0
                        }}
                        animate = {{
                            opacity: 1
                        }}
                        transition={{
                            duration: 2
                        }}
                        src={transformURL(previewSrc)}
                        alt={alt}
                    />
                    :
                    null
                    :
                    <motion.img
                        initial= {{
                            opacity: 0
                        }}
                        animate = {{
                            opacity: 1
                        }}
                        transition={{
                            duration: 2
                        }}
                        src={src ? transformURL(src) : defaultPhoto}
                        alt={alt}
                    />
                }
            </div>
    )
}