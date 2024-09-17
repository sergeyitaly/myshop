import clsx from "clsx"
import { AppImage } from "../../AppImage/AppImage"
import style from './CategoryCard.module.scss'
import { MouseEvent } from "react"

interface CategoryCardProps {
    title: string
    photoSrc: string | null
    previewSrc: string | null
    className?: string
    onClick?: (e: MouseEvent<HTMLDivElement>) => void
}

export const CategoryCard = ({
    title,
    photoSrc,
    previewSrc,
    className,
    onClick
}: CategoryCardProps) => {

    return (
        <div 
            className={clsx(style.card, className)}
            onClick = {onClick}
        >
            <AppImage
                className={style.imageSize}
                src={photoSrc}
                previewSrc={previewSrc}
                alt={title}
              />
              <h1>{title}</h1>
        </div>
    )
}