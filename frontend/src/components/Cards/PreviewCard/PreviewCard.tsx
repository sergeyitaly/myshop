import clsx from 'clsx'
import { AppImage } from '../../AppImage/AppImage'
import style from './PreviewCard.module.scss'
import { Currency } from '../../../models/entities'
import { formatPrice } from '../../../functions/formatPrice'


interface PreviewCardProps {
    className?: string
    photoSrc: string | null
    discount?: string
    currency?: Currency
    price?: string
    title: string
    subTitle?: string 
    loading?: boolean
    onClick?: () => void  
}


export const PreviewCard = ({
    className,
    photoSrc,
    title,
    discount,
    price,
    loading,
    currency,
    subTitle,
    onClick
}: PreviewCardProps) => {

    const handleClick = () => {
        onClick && onClick()
    }

    const transformedDicount = discount ? Math.ceil(+discount) : null;

    let newPrice = null

    if(price && transformedDicount){
        newPrice = +price - +price*transformedDicount/100
    }

    console.log(price, newPrice);
    
    

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
            {subTitle && <p className={style.subTitle}>{subTitle}</p>}
            {
                price && currency &&
                <div className={style.priceContainer}>
                    <p 
                        className={clsx(style.subTitle, {[style.crossText]: !!newPrice} )}
                    >
                        {formatPrice(price, currency)}
                    </p>
                    {newPrice && 
                        <p 
                            className={clsx(style.subTitle, style.currentPrice)}
                        >
                            {formatPrice(newPrice, currency)}
                        </p>}
                </div>
            }
        </div>
    )
}