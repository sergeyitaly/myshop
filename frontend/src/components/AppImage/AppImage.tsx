import { useEffect, useState } from 'react'
import clsx from 'clsx'
import style from './AppImage.module.scss'
import {motion} from 'framer-motion'
import defaultPhoto from '../../assets/default.png'


interface AppImageProps {
    className?: string
    src: string | null
    alt: string
}

export const AppImage = ({
    alt,
    src,
    className
}: AppImageProps) => {

    const [isLoading, setIsLoading] = useState<boolean>(true)

    useEffect(() => {
        console.log(src);
        console.log(defaultPhoto);
        
        const img = new Image()
        img.src = src ? src : defaultPhoto
        img.onload = () => {
            setIsLoading(false)
        }
    }, [src]) 



    return (
            <div className={clsx(style.imgWrapper, className)}>
                {
                    isLoading ?
                    // <Skeleton
                    //     className={style.skeleton}
                    // />
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
                        src={src ? src : defaultPhoto}
                        alt={alt}
                        loading="lazy"
                    />
                }
            </div>
    )
}