import clsx from 'clsx'
import { AppImage } from '../../AppImage/AppImage'
import style from './PreviewCard.module.scss'


interface PreviewCardProps {
    className?: string
    photoSrc: string
    title: string
    subTitle?: string 
    loading?: boolean
    onClick?: () => void  
}


export const PreviewCard = ({
    className,
    photoSrc,
    title,
    loading,
    subTitle,
    onClick
}: PreviewCardProps) => {

    const handleClick = () => {
        onClick && onClick()
    }



    return (
        <div 
            className={clsx(style.card, className, {
                [style.loading] : loading
            })}
            onClick={handleClick}
        >
              <AppImage
                className={style.imageSize}
                src={photoSrc}
                alt={title}

              />
            <p className={style.title}>{title}</p>
            <p className={style.subTitle}>{subTitle}</p>
        </div>
    )
}