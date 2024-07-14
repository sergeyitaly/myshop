import clsx from 'clsx'
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
            <div className={style.imgWrapper}>
                <img
                    src={photoSrc}
                    alt={title}
                    loading="lazy"
                />
            </div>
            <p className={style.title}>{title}</p>
            <p className={style.subTitle}>{subTitle}</p>
        </div>
    )
}