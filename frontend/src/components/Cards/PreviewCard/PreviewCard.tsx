import style from './PreviewCard.module.scss'


interface PreviewCardProps {
    photoSrc: string
    title: string
    subTitle?: string 
    onClick?: () => void  
}


export const PreviewCard = ({
    photoSrc,
    title,
    subTitle,
    onClick
}: PreviewCardProps) => {

    const handleClick = () => {
        onClick && onClick()
    }

    return (
        <div 
            className={style.card}
            onClick={handleClick}
        >
            <div className={style.imgWrapper}>
                <img
                    src={photoSrc}
                    alt={title}
                    // style={{ maxWidth: '100%' }}
                    loading="lazy"
                />
            </div>
            <p className={style.title}>{title}</p>
            <p className={style.subTitle}>{subTitle}</p>
        </div>
    )
}